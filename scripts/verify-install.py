#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""repo-memory - verify-install: checks an INSTALLED memory folder, not this kit.

Every other check in this repository validates the KIT: that INSTALL.md still matches its
templates, that no real name leaked, that the YAML parses. None of them ever looked at an
installed carrier. That is how an unattended install could produce a folder full of unanswered
questions, a Map pointing at files that do not exist, a workflow with no secrets and a
contradiction between two memory files, while every check in the kit stayed green.

This one looks at the result. Point it at an installed project:

    python3 verify-install.py                  # the current directory
    python3 verify-install.py ../some-project

Standard library only, no network, no host. It runs at tier 1 - a plain folder with no version
control and no host at all - and adds three git checks only where there is a git repository. It
never asks a host whether a secret exists, because it cannot; where it says a secret is missing it
means the install did not write the name down, and the message says so.

Exit codes:
    0   nothing blocking; advisories may still be printed
    1   at least one blocking problem
    2   a credential-shaped value is sitting in a memory file - the loudest failure here

BLOCKING is what makes the memory misleading to the next session: it is wrong, or it points at
something that is not there. ADVISORY is what makes it worse than it could be. Fix the blocking
ones before you tell anyone the install is finished.

KB below means 1024 bytes.
"""
from __future__ import print_function

import argparse
import io
import os
import re
import subprocess
import sys
import textwrap

KB = 1024

# The four files a level-0 install always writes, plus the six that appear on first entry.
LEVEL0_DOCS = ("tasks.md", "handoff.md", "traps.md", "tooling.md")
LATER_DOCS = ("decisions.md", "architecture.md", "measurement.md",
              "changelog.md", "open-questions.md", "personal.md")

# Defaults from AGENTS.md -> Rotation. Read from the installed file when it states a number, so
# that an owner who widened a budget on purpose is not nagged about it forever.
DEFAULT_BUDGET_KB = {"traps.md": 25, "handoff.md": 2}
TASKS_BUDGET_KB = {"code": 10, "hub": 25}

# The shapes from templates/.github/workflows/memory-secret-scan.yml. They are the same list on
# purpose - two checks that disagree about what a secret looks like are worse than one - with a
# three documented refinements. Two are shared with the template - a word boundary before sk-,
# so that "task-", "risk-" and "disk-" do not fire, and no angle bracket in a connection string's
# userinfo, so that a documented postgres://<user>:<password>@host template does not - and one is
# ASSET_HASH below: a 40-character hex run inside a URL or an
# asset filename is a content hash, not a credential. That was not a hypothesis. Run against a
# live carrier, the unrefined pattern fired four times on one OpenCart image filename in a public
# og:image URL, and this is the loudest check in the script: the first time it cries wolf is the
# last time anybody reads it.
ASSET_HASH = re.compile(
    r"^\.(?:png|jpe?g|webp|gif|svg|ico|js|css|map|html?|woff2?|mp4|pdf|zip)\b", re.IGNORECASE)

SECRET_PATTERNS = [
    ("github token",        re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}")),
    ("openai-style key",    re.compile(r"\bsk-[A-Za-z0-9]{20,}")),
    ("aws access key id",   re.compile(r"AKIA[0-9A-Z]{16}")),
    ("slack token",         re.compile(r"xox[abprs]-[A-Za-z0-9-]{10,}")),
    ("telegram bot token",  re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b")),
    ("jwt",                 re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.")),
    ("private key block",   re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("long hex blob",       re.compile(r"\b[0-9a-f]{40,}\b")),
    ("supabase-style key",  re.compile(r"\bsb[pous]?_[A-Za-z0-9]{20,}")),
    ("connection string with a password",
     re.compile(r"\b(?:postgres|postgresql|mysql|mongodb|redis|amqp)://[^:<>\s/]+:[^@<>\s]+@")),
    ("signed url",
     re.compile(r"[?&](?:X-Amz-Signature|X-Goog-Signature|sig|token)=[A-Za-z0-9%_-]{16,}")),
    # tooling.md's threat model forbids these two by name and nothing here used to look for
    # them. A chat id is matched BY CONTEXT and never as a bare number: a negative integer is
    # indistinguishable from any other negative integer, and a pattern that fires on every
    # measurement in the folder is a pattern somebody switches off. The key, then at most eight
    # non-alphanumeric characters (":", "=", a quote, a table cell wall, a URL parameter), then
    # the digits. A Secrets table row naming TELEGRAM_CHAT_ID has no digits in it and is safe.
    ("chat, channel or group id",
     re.compile(r"(?:chat|channel|group|peer)[ _-]?id[^A-Za-z0-9]{1,8}-?\d{6,}", re.IGNORECASE)),
    # The one id shape that identifies itself: a Telegram supergroup or channel id is literally
    # -100 followed by ten to thirteen digits.
    ("telegram chat id",
     re.compile(r"(?<![0-9A-Za-z_.-])-100\d{10,13}(?!\d)")),
    # A webhook URL, by host and shape. Holding one is the ability to post into somebody's
    # channel; it is not less of a credential for having no field called "token" in it.
    ("webhook url", re.compile(
        r"hooks\.slack\.com/(?:services|workflows|triggers)/[A-Za-z0-9+/_-]{16,}"
        r"|discord(?:app)?\.com/api/webhooks/\d{15,}/[A-Za-z0-9_-]{20,}"
        r"|api\.telegram\.org/bot\d{8,10}:[A-Za-z0-9_-]{35}"
        r"|webhook\.office\.com/webhookb2/[A-Za-z0-9@/_-]{20,}"
        r"|outlook\.office(?:365)?\.com/webhook/[A-Za-z0-9@/_-]{20,}"
        r"|https?://[^\s<>]+/webhooks?/[A-Za-z0-9_-]{24,}")),
]

# A line that explains what the unanswered-question marker means is not itself an unanswered
# question. Both shipped templates phrase it one of these ways.
MARKER_META = re.compile(
    r"marks a question|means a question|is a missing answer|missing answer, not a settled fact",
    re.IGNORECASE)

# An entry skeleton copied out of the traps template and left standing as if it were a trap.
TRAP_SKELETON = (
    "what you will see",
    "why it happens",
    "the concrete action",
    "short name of the trap",
)

PLACEHOLDER = re.compile(r"<[^<>\n]{1,70}>")

# Markdown carries angle brackets that are not unfilled placeholders: inline HTML, autolinks,
# a URL path segment, and date patterns like YYYY-MM-DD. A check that flags those is a check
# that gets switched off.
HTML_TAGS = set((
    "a b br code pre em strong i u p ul ol li div span img hr sub sup kbd small "
    "details summary table thead tbody tr td th h1 h2 h3 h4 h5 h6 blockquote "
    "figure figcaption input label form nav main header footer script style"
).split())
DATE_PATTERN = re.compile(r"YYYY|HHMM|MM-DD|-MM\b|-DD\b")


def placeholders_in(line):
    """The <angle bracket> tokens on this line that really are unfilled template slots."""
    out = []
    for m in PLACEHOLDER.finditer(line):
        tok = m.group(0)
        inner = tok[1:-1].strip()
        if tok == "<?>" or not inner:
            continue
        if inner[0] in "/!" or "://" in inner:
            continue                                   # closing tag, comment, autolink
        if re.split(r"[\s/]", inner)[0].lower() in HTML_TAGS:
            continue                                   # inline HTML
        if "://" in line and m.start() and line[m.start() - 1] == "/":
            continue                                   # https://host/<path>
        if DATE_PATTERN.search(inner):
            continue                                   # a filename pattern, not a blank
        out.append(tok)
    return out


def is_pattern_path(tok):
    """docs/tasks/done-YYYY-MM.md names a shape, not a file. Nothing to check."""
    return ("<" in tok or ">" in tok or "*" in tok or DATE_PATTERN.search(tok) is not None)


def locate(root, mem, name):
    """A memory file at the top of the memory folder, or in a per-system subfolder under it."""
    if not mem:
        return None
    direct = os.path.join(root, mem, name)
    if os.path.isfile(direct):
        return os.path.join(mem, name)
    base = os.path.join(root, mem)
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = sorted(d for d in dirnames if d != ".git")
        if name in filenames:
            return os.path.relpath(os.path.join(dirpath, name), root)
    return None


def read(path):
    try:
        with io.open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except (IOError, OSError):
        return ""


def live(text):
    """[(lineno, text-with-HTML-comments-blanked)]. Comments hold format notes, not content."""
    out = []
    inside = False
    for n, raw in enumerate(text.splitlines(), 1):
        line = re.sub(r"<!--.*?-->", "", raw)
        if inside:
            if "-->" in line:
                line = line.split("-->", 1)[1]
                inside = False
            else:
                line = ""
        if "<!--" in line:
            line = line.split("<!--", 1)[0]
            inside = True
        out.append((n, line))
    return out


def split_sections(pairs):
    """(preamble, {lowercased '## heading': [(lineno, line)]}) over a live() list."""
    pre, cur, buf, out = [], None, [], {}
    for n, line in pairs:
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            if cur is None:
                pre = buf
            else:
                out[cur] = out.get(cur, []) + buf
            cur, buf = m.group(1).lower(), []
        else:
            buf.append((n, line))
    if cur is None:
        pre = buf
    else:
        out[cur] = out.get(cur, []) + buf
    return pre, out


def section(sections, prefix):
    for key in sections:
        if key.startswith(prefix):
            return sections[key]
    return None


class Report(object):
    """Three buckets. A secret is its own bucket because it is not one problem among several."""

    def __init__(self):
        self.secrets = []
        self.blocking = []
        self.advisory = []
        self.facts = []

    def secret(self, where, problem, fix):
        self.secrets.append((where, problem, fix))

    def block(self, where, problem, fix):
        self.blocking.append((where, problem, fix))

    def advise(self, where, problem, fix):
        self.advisory.append((where, problem, fix))

    def fact(self, line):
        self.facts.append(line)


# --- locating the install -----------------------------------------------------------------

def find_memory_dir(root, forced):
    if forced:
        return forced
    best, best_score = None, -1
    for name in ("docs", "memory"):
        d = os.path.join(root, name)
        if not os.path.isdir(d):
            continue
        score = sum(1 for f in LEVEL0_DOCS + LATER_DOCS if os.path.isfile(os.path.join(d, f)))
        # docs/ that publishes a site is not the memory folder; the kit moves memory to memory/.
        if any(os.path.exists(os.path.join(d, x)) for x in ("CNAME", "index.html", ".nojekyll")):
            score -= 5
        if score > best_score:
            best, best_score = name, score
    return best


CORE_NAMES = set(LEVEL0_DOCS + LATER_DOCS)


def core_files(files):
    """The memory files proper: the index, and the ten documents the kit defines - at the top of
    the memory folder or in a per-system subfolder under it. Everything else that happens to live
    in docs/ (an audit, a dated archive, a copy of somebody's spec) is not this kit's to police,
    and treating it as such buries the findings that matter."""
    return [f for f in files
            if f in ("AGENTS.md", "CLAUDE.md") or os.path.basename(f) in CORE_NAMES]


def all_files_under_memory(root, mem):
    """Every file under the memory folder, whatever its extension, plus the two index files.
    Only the secret scan uses this: a credential in a committed .json is still a credential."""
    out = [n for n in ("AGENTS.md", "CLAUDE.md") if os.path.isfile(os.path.join(root, n))]
    base = os.path.join(root, mem) if mem else None
    if base and os.path.isdir(base):
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = sorted(d for d in dirnames if d != ".git")
            for fn in sorted(filenames):
                out.append(os.path.relpath(os.path.join(dirpath, fn), root))
    return out


def memory_files(root, mem):
    """Every .md under the memory folder, plus AGENTS.md and CLAUDE.md, as relative paths."""
    out = []
    for name in ("AGENTS.md", "CLAUDE.md"):
        if os.path.isfile(os.path.join(root, name)):
            out.append(name)
    base = os.path.join(root, mem) if mem else None
    if base and os.path.isdir(base):
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = sorted(d for d in dirnames if d != ".git")
            for fn in sorted(filenames):
                if fn.endswith(".md"):
                    full = os.path.join(dirpath, fn)
                    out.append(os.path.relpath(full, root))
    return out


def carrier_kind(root, agents_text, sections):
    """'hub' or 'code'. The Rotation table asks the installer to keep one budget and delete the
    other; where that was not done we have to infer, and we say so in the header."""
    for _, line in live(agents_text):
        if line.strip().lower().startswith("project hub:"):
            return "code", "AGENTS.md carries a Project hub line, so this is a code carrier"
    rel = section(sections, "related carriers")
    real_rows = False
    if rel:
        for _, line in rel:
            if line.strip().startswith("|") and not re.match(r"^\|[\s|:-]+\|?\s*$", line.strip()):
                if not PLACEHOLDER.search(line) and "carrier" not in line.lower():
                    real_rows = True
    if os.path.basename(os.path.abspath(root)).endswith("-memory") or real_rows:
        return "hub", "no Project hub line, and this looks like the hub itself"
    return "code", "no Project hub line and nothing marking this as a hub"


# --- the checks ---------------------------------------------------------------------------

def check_index_files(root, rep, agents_text):
    agents = os.path.join(root, "AGENTS.md")
    claude = os.path.join(root, "CLAUDE.md")

    if not os.path.isfile(agents):
        rep.block("AGENTS.md",
                  "There is no AGENTS.md. Nothing is loaded at the start of a session, so none "
                  "of the five procedures ever run.",
                  "Create AGENTS.md in the carrier root from template A.1 of INSTALL.md and fill "
                  "in the name, the carrier locator, the owner and the Rules.")
    else:
        n = len(agents_text.splitlines())
        rep.fact("AGENTS.md: %d lines (budget 150)" % n)
        if n > 150:
            rep.block("AGENTS.md:%d" % n,
                      "AGENTS.md is %d lines, over the 150-line budget. Every line is paid for by "
                      "every session." % n,
                      "Move whatever is not needed in EVERY task into the memory folder and link "
                      "it from the Map. Aim for about 100 lines.")
        elif n > 130:
            rep.advise("AGENTS.md:%d" % n,
                       "AGENTS.md is %d lines. The budget is 150 and the aim is about 100, so "
                       "there is little room left for what this project actually knows." % n,
                       "Before adding anything else, move a section into the memory folder and "
                       "leave a Map row pointing at it.")

    if not os.path.isfile(claude):
        rep.block("CLAUDE.md",
                  "There is no CLAUDE.md. Claude Code reads CLAUDE.md and not AGENTS.md, so this "
                  "install is invisible to it.",
                  "Create CLAUDE.md containing the single line @AGENTS.md (template A.2).")
    else:
        text = read(claude)
        if "@AGENTS.md" not in text:
            rep.block("CLAUDE.md",
                      "CLAUDE.md does not import AGENTS.md, so Claude Code reads one file and "
                      "every other agent reads another. They drift apart from the first edit.",
                      "Put @AGENTS.md on its own line at the top of CLAUDE.md. Claude-specific "
                      "additions go below it, nothing else.")


def check_level0(root, mem, rep):
    if not mem:
        rep.block(".",
                  "No memory folder found: neither docs/ nor memory/ holds tasks.md, traps.md, "
                  "tooling.md or handoff.md.",
                  "Run the installer, or pass --memory-dir if this project keeps its memory "
                  "somewhere else.")
        return
    for name in LEVEL0_DOCS:
        if locate(root, mem, name) is None:
            rep.block("%s/%s" % (mem, name),
                      "%s is missing. It is one of the four files a level-0 install always "
                      "writes, and Entry reads it every time." % name,
                      "Create it from the matching template in Appendix A of INSTALL.md and put "
                      "this project's content in it.")


def paths_in(lines):
    """Backticked tokens that look like a path inside the carrier, with the line they sit on."""
    found = []
    for n, line in lines:
        for tok in re.findall(r"`([^`]+)`", line):
            tok = tok.strip()
            if is_pattern_path(tok):
                continue          # docs/traps/archive-<YYYY>-Q<n>.md names a shape, not a file
            if not tok.endswith(".md"):
                continue
            if tok.startswith("/") or "://" in tok:
                continue
            found.append((tok, n, line))
    return found


def check_named_paths(root, mem, rep, sections):
    """Every path the index promises - in the Map, in Entry, in Exit - must be there.

    Reported once per path, with the first place that names it: the same file is named in two
    procedures on a normal install, and one problem should read as one problem."""
    named = {}
    for label, prefix in (("The Map", "map"), ("Entry", "entry"), ("Exit", "exit")):
        for tok, n, line in paths_in(section(sections, prefix) or []):
            named.setdefault(tok, []).append((label, n, line))

    for tok in sorted(named):
        mentions = named[tok]
        # A line that talks about the hub or another carrier names ITS files, not ours.
        if all(re.search(r"\bhub\b|\bcarrier\b", m[2], re.IGNORECASE) for m in mentions):
            continue
        # In a memory/ install every docs/ mention belongs to check_folder_naming, which
        # reports the cause once instead of once per path.
        if mem == "memory" and tok.startswith("docs/"):
            continue
        label, n, _ = mentions[0]
        # One "(create it when …)" anywhere in the index covers every mention of that file.
        if any(re.search(r"\bcreate\b", m[2], re.IGNORECASE) for m in mentions):
            continue
        candidates = [os.path.join(root, tok)]
        if "/" not in tok and mem:
            # AGENTS.md writes `tasks.md` for a file that lives in the memory folder.
            candidates.append(os.path.join(root, mem, tok))
        if any(os.path.exists(c) for c in candidates):
            continue
        base = os.path.basename(tok)
        loc = "AGENTS.md:%d" % n
        if base in LATER_DOCS:
            rep.advise(loc,
                       "%s names %s, which does not exist. It is one of the files the kit creates "
                       "on first entry, so this is expected - but nothing here says so, and a "
                       "session that follows the index finds nothing and stops trusting it."
                       % (label, tok),
                       "Add \"(create it when there is a first entry)\" on that line, or drop the "
                       "mention until the file exists.")
        else:
            rep.block(loc,
                      "%s names %s, and there is no such file. This is the failure the whole "
                      "check exists for: memory that points at nothing still reads as memory."
                      % (label, tok),
                      "Create the file, or delete the mention, or mark it \"(create it when …)\" "
                      "if it is genuinely deferred.")


def check_unresolved_markers(root, rep, files, unattended):
    hits = []
    for rel in core_files(files):
        for n, line in live(read(os.path.join(root, rel))):
            if "<?>" not in line or MARKER_META.search(line):
                continue
            hits.append((rel, n, line.strip()[:90]))
    if not hits:
        return
    where = "%s:%d" % (hits[0][0], hits[0][1])
    listing = "; ".join("%s:%d" % (r, n) for r, n, _ in hits[:12])
    if len(hits) > 12:
        listing += " (+%d more)" % (len(hits) - 12)
    if unattended:
        rep.advise(where,
                   "%d unanswered question(s) left as <?>: %s. The install declared itself "
                   "unattended, so these are honest blanks rather than a broken install - but "
                   "every one of them is a question nobody has answered yet."
                   % (len(hits), listing),
                   "Give the owner this list by question number and replace each marker in the "
                   "same commit as the answer. Drop the UNATTENDED line when the last one goes.")
    else:
        rep.block(where,
                  "%d unresolved <?> marker(s) in an install that does not declare itself "
                  "unattended: %s. A later session reads an unanswered question as a fact."
                  % (len(hits), listing),
                  "Answer them, or - if nobody was in the session - put the UNATTENDED line "
                  "under Owner: in AGENTS.md so the blanks are labelled as blanks.")


def check_traps(root, mem, rep):
    p = os.path.join(root, mem, "traps.md")
    if not os.path.isfile(p):
        return
    text = read(p)
    lines = live(text)
    body = [(n, l) for n, l in lines if l.strip()]
    skeleton = []
    for n, l in body:
        low = l.lower()
        for frag in TRAP_SKELETON:
            if frag in low:
                skeleton.append((n, l.strip()[:80]))
                break
    if skeleton:
        rep.block("%s/traps.md:%d" % (mem, skeleton[0][0]),
                  "traps.md holds the entry skeleton from the template as if it were a trap "
                  "(line %d: %s). An abandoned entry is worse than an empty file: it reads as a "
                  "trap somebody started writing down."
                  % (skeleton[0][0], skeleton[0][1]),
                  "Either fill it in with a real trap - symptom, cause, what to do, date - or "
                  "delete the entry and leave the \"nothing recorded yet\" line standing.")
        return
    has_entry = any(re.match(r"^###\s+\S", l) for _, l in lines)
    if not has_entry:
        rep.advise("%s/traps.md" % mem,
                   "traps.md records no traps at all. Question 8 of the install block asks for "
                   "one thing that has already cost somebody an afternoon; an empty traps.md "
                   "usually means nobody was asked.",
                   "Ask the owner for one trap and write it down. One real entry is what makes "
                   "the next session open this file at all.")


def check_related_carriers(rep, sections):
    rel = section(sections, "related carriers")
    if rel is None:
        return
    rows = []
    for n, line in rel:
        s = line.strip()
        if not s.startswith("|"):
            continue
        if re.match(r"^\|[\s|:-]+\|?$", s):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if cells and cells[0].lower().startswith("carrier"):
            continue
        rows.append((n, s, cells))
    if not rows:
        rep.block("AGENTS.md",
                  "The Related carriers section is present but its table has no rows at all.",
                  "Delete the whole section if this project is a single carrier, or add one row "
                  "per carrier: name, locator, what it is, when to read it.")
        return
    real = [r for r in rows if not PLACEHOLDER.search(r[1])]
    if not real:
        rep.block("AGENTS.md:%d" % rows[0][0],
                  "The Related carriers table holds nothing but the template's placeholder row. "
                  "The template says it plainly: a table holding only a placeholder is a lie the "
                  "next session believes - it will try to read a carrier called <short name>.",
                  "Delete the whole Related carriers section if this project is a single "
                  "carrier. Otherwise replace the row with the real carriers and their locators.")


def workflow_files(root):
    d = os.path.join(root, ".github", "workflows")
    if not os.path.isdir(d):
        return []
    return [os.path.join(d, f) for f in sorted(os.listdir(d))
            if f.endswith(".yml") or f.endswith(".yaml")]


def check_reporting(root, mem, rep, mem_texts):
    wfs = workflow_files(root)
    if not wfs:
        return
    haystack = "\n".join(mem_texts.values())
    for wf in wfs:
        rel = os.path.relpath(wf, root)
        text = read(wf)
        names = sorted(set(re.findall(r"secrets\.([A-Za-z_][A-Za-z0-9_]*)", text)))
        names = [n for n in names if n != "GITHUB_TOKEN"]
        if not names:
            continue
        missing = [n for n in names if n not in haystack]
        if not missing:
            continue
        # Only the kit's own reporting workflow is installed BY the install, and only for that one
        # can this script honestly claim the red-build failure. Any other workflow in the repo
        # predates the memory and demonstrably runs; there the finding is that tooling.md does not
        # say where its secrets live, which is worth saying and is not worth blocking on.
        is_reporter = ("report" in os.path.basename(rel).lower()
                       or "reports/" in text)
        if not is_reporter:
            rep.advise(rel,
                       "%s reads %s, and %s recorded nowhere in the memory folder. A session that "
                       "has to re-run or fix this workflow will not know where those live, which "
                       "is the whole job of the Secrets table."
                       % (rel, ", ".join(missing),
                          "that name is" if len(missing) == 1 else "those names are"),
                       "Add each one to the Secrets table in %s/tooling.md - the name and where "
                       "it lives, never the value. `grep -h 'secrets\\.' "
                       ".github/workflows/*.yml | sort -u` lists them all." % mem)
            continue
        if missing:
            rep.block(rel,
                      "%s reads %s, and %s recorded nowhere in the memory folder. This check "
                      "cannot see the host's secret store, so what it proves is narrower and "
                      "just as damning: nobody wrote down that these exist. A workflow committed "
                      "before its secrets are set fails on the first push, and a memory kit whose "
                      "first act is a red build does not get a second try."
                      % (rel, ", ".join(missing),
                         "that name is" if len(missing) == 1 else "those names are"),
                      "Set the secrets in the host, then add each one to the Secrets table in "
                      "%s/tooling.md - the name and where it lives, never the value. Cannot set "
                      "them now? Delete the workflow and put \"set the secrets, then add the "
                      "workflow\" in %s/tasks.md." % (mem, mem))

    tooling = mem_texts.get("%s/tooling.md" % mem, "")
    reporters = [os.path.relpath(w, root) for w in wfs
                 if re.search(r"secrets\.(?!GITHUB_TOKEN)", read(w))]
    if reporters and re.search(r"no reporting channel", tooling, re.IGNORECASE):
        rep.block("%s/tooling.md" % mem,
                  "tooling.md says there is no reporting channel, and %s is committed and "
                  "reads a secret. Two memory files contradicting each other is exactly the "
                  "state a session cannot resolve on its own." % ", ".join(reporters),
                  "Decide which is true. Either delete the workflow and keep \"Exit ends at the "
                  "commit\", or describe the channel in tooling.md -> Reporting and remove that "
                  "sentence.")

    if reporters and not os.path.isfile(os.path.join(root, "reports", "README.md")):
        rep.advise("reports/README.md",
                   "A reporting workflow is installed but reports/README.md is missing, so "
                   "nothing says what a report file must contain. Every later report is copied "
                   "from that file.",
                   "Add reports/README.md from template A.9 and fill in this project's name, "
                   "timezone and example values before committing it.")


def budgets_from_agents(sections, kind, rep):
    """Read the Rotation table of the installed AGENTS.md; fall back to the kit's defaults."""
    budgets = dict(DEFAULT_BUDGET_KB)
    budgets["tasks.md"] = TASKS_BUDGET_KB[kind]
    source = {k: "kit default" for k in budgets}

    rot = section(sections, "rotation")
    if not rot:
        return budgets, source
    for n, line in rot:
        s = line.strip()
        if not s.startswith("|"):
            continue
        m = re.search(r"`([a-z-]+\.md)`", s)
        if not m:
            continue
        name = m.group(1)
        figures = sorted(set(int(x) for x in re.findall(r"(\d+)\s*KB", s)))
        if len(figures) == 1:
            budgets[name] = figures[0]
            source[name] = "AGENTS.md -> Rotation"
        elif len(figures) > 1 and name == "tasks.md":
            rep.advise("AGENTS.md:%d" % n,
                       "The Rotation row for tasks.md still offers both budgets (%s KB). The "
                       "template says to keep the one that matches this carrier and delete the "
                       "other; leaving both means no session knows when to rotate."
                       % " and ".join(str(f) for f in figures),
                       "Delete the half that does not apply. This carrier looks like a %s "
                       "carrier, so keep %d KB." % (kind, TASKS_BUDGET_KB[kind]))
    return budgets, source


def check_budgets(root, mem, rep, budgets, source, kind):
    for name, kb in sorted(budgets.items()):
        p = os.path.join(root, mem, name)
        if not os.path.isfile(p):
            continue
        size = os.path.getsize(p)
        limit = kb * KB
        rep.fact("%s/%s: %.1f KB of %d KB (%s%s)"
                 % (mem, name, size / float(KB), kb, source.get(name, "kit default"),
                    "" if name != "tasks.md" else ", %s carrier" % kind))
        if size > limit:
            rep.block("%s/%s" % (mem, name),
                      "%s is %.1f KB, over its %d KB rotation budget. Rotation is not optional "
                      "housekeeping: over budget, entry stops being cheap and the file stops "
                      "being read." % (name, size / float(KB), kb),
                      "Rotate BEFORE the next entry, in the same commit: move the eligible "
                      "entries verbatim into the archive file named in the Rotation table and "
                      "leave one searchable sentence behind for each. Nothing is summarised away.")
        elif size > limit * 0.8:
            rep.advise("%s/%s" % (mem, name),
                       "%s is %.1f KB of its %d KB budget. The next few entries will push it "
                       "over." % (name, size / float(KB), kb),
                       "Rotate at the next Exit rather than at the one where it starts blocking.")


def check_identity_placeholders(rep, pre, sections):
    """The header block and Rules of AGENTS.md are where the install's identity lives: project,
    carrier, hub, owner, autonomy, language. A placeholder left standing there is a blank owner."""
    scope = list(pre)
    rules = section(sections, "rules")
    if rules:
        scope += rules
    for n, line in scope:
        for tok in placeholders_in(line):
            rep.block("AGENTS.md:%d" % n,
                      "The identity block still carries the template placeholder %s (%s). "
                      "A session reads this as the project's name, owner or rules."
                      % (tok, line.strip()[:70]),
                      "Replace it with this project's answer, or delete the line if the question "
                      "does not apply here. If nobody can answer it, write <?> instead, which "
                      "the whole memory folder already defines as an open question.")


def check_other_placeholders(root, mem, rep, files):
    hits = []
    for rel in core_files(files):
        if rel == "AGENTS.md":
            continue
        for n, line in live(read(os.path.join(root, rel))):
            for tok in placeholders_in(line):
                hits.append((rel, n, tok))
    if hits:
        listing = "; ".join("%s:%d %s" % h for h in hits[:8])
        if len(hits) > 8:
            listing += " (+%d more)" % (len(hits) - 8)
        rep.advise("%s:%d" % (hits[0][0], hits[0][1]),
                   "%d template placeholder(s) left unfilled outside AGENTS.md: %s. Each one is "
                   "an example row the installer was told to replace or delete."
                   % (len(hits), listing),
                   "Replace each with this project's own content, or delete the row. A row left "
                   "unedited is a lie the next session believes.")


def check_folder_naming(root, mem, rep, files, mem_texts):
    if mem != "memory":
        return
    rx = re.compile(r"docs/(?:%s)" % "|".join(re.escape(f) for f in LEVEL0_DOCS + LATER_DOCS))
    hits = []
    for rel in files:
        for n, line in live(mem_texts.get(rel, "")):
            if rx.search(line) and not re.search(r"\bhub\b|\bcarrier\b", line, re.IGNORECASE):
                hits.append("%s:%d" % (rel, n))
    if not hits:
        return
    listing = ", ".join(hits[:10]) + (" (+%d more)" % (len(hits) - 10) if len(hits) > 10 else "")
    rep.block(hits[0],
              "This project keeps its memory in memory/, but %d line(s) of the installed files "
              "still point at docs/: %s. Every one of those paths is a file that does not exist, "
              "and this is the whole reason the other findings above name docs/."
              % (len(hits), listing),
              "Replace docs/ with memory/ in every installed file - step 3 of INSTALL.md says to "
              "substitute it everywhere, and the templates all ship saying docs/.")


def check_secrets(root, rep, files):
    """The loudest check. A value here is compromised the moment it is committed."""
    binary = (".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".ico", ".woff", ".woff2")
    for rel in files:
        if rel.endswith(".local.md"):
            continue          # gitignored by the kit, and the shipped scan skips it too
        if rel.lower().endswith(binary):
            continue
        for n, raw in enumerate(read(os.path.join(root, rel)).splitlines(), 1):
            for name, rx in SECRET_PATTERNS:
                m = rx.search(raw)
                if not m:
                    continue
                if name == "long hex blob":
                    before = raw[:m.start()]
                    after = raw[m.end():]
                    if ASSET_HASH.match(after) or before.endswith("/"):
                        continue          # a content hash in a filename or a URL path
                shown = m.group(0)
                shown = shown[:6] + "..." if len(shown) > 6 else "..."
                rep.secret("%s:%d" % (rel, n),
                           "A %s is committed in a memory file (starts %s). tooling.md's own "
                           "rule is names and places, never values - and this file is readable "
                           "by everyone who can read the carrier, now and for as long as it "
                           "exists." % (name, shown),
                           "Rotate the secret FIRST, then remove the text. Removing it alone "
                           "changes nothing: git keeps history, and the value is already in it. "
                           "Then put the name and where it lives in the Secrets table instead.")
                break


def check_hook(root, rep):
    hook = os.path.join(root, ".claude", "hooks", "memory-exit-reminder.sh")
    if not os.path.isfile(hook):
        return
    if not os.access(hook, os.X_OK):
        rep.advise(".claude/hooks/memory-exit-reminder.sh",
                   "The Exit reminder hook is installed but not executable, so it never runs.",
                   "chmod +x .claude/hooks/memory-exit-reminder.sh")
    settings = read(os.path.join(root, ".claude", "settings.json"))
    if "memory-exit-reminder" not in settings:
        rep.advise(".claude/settings.json",
                   "The Exit reminder hook is installed but not registered in "
                   ".claude/settings.json, so nothing ever calls it. The only backstop this kit "
                   "has for a session that forgets Exit is silently absent.",
                   "Register it under Stop and PreCompact as the header of the hook shows. "
                   "Merge into an existing hooks block, do not replace it.")


def in_ci():
    return bool(os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS"))


def check_commit_guard(root, rep):
    """.githooks/commit-msg refuses a commit that changes the project and records nothing.

    The hook is committed - that is the point of .githooks/ - but the setting that makes git run
    it, core.hooksPath, lives in .git/config and is per clone. It is not committed, not inherited
    by a clone, and nothing tells you it is missing: the guard is simply absent and every commit
    goes through. So this check is the thing that says so out loud. It is BLOCKING on a real
    clone, because step 6 of the installer will not finish while a blocking finding stands, and
    ADVISORY under CI, where a runner can never have the setting and a red build over it would
    only teach somebody to delete the workflow."""
    if not os.path.isdir(os.path.join(root, ".git")):
        return                      # tier 1: no git, no hooks, nothing to say
    hook = os.path.join(root, ".githooks", "commit-msg")
    if not os.path.isfile(hook):
        rep.advise(".githooks/commit-msg",
                   "The commit guard is not installed. The Stop hook reads the working tree, so "
                   "a session that commits code and memory-nothing in the same commit passes it "
                   "unnoticed - and Exit's own rule, records in the same commit as the change, "
                   "makes that the normal path rather than a rare one.",
                   "Copy templates/.githooks/commit-msg from the kit to .githooks/commit-msg, "
                   "chmod +x it, commit it, and run: git config core.hooksPath .githooks")
        return
    if not os.access(hook, os.X_OK):
        rep.advise(".githooks/commit-msg",
                   "The commit guard is committed but not executable, so git skips it silently.",
                   "chmod +x .githooks/commit-msg and commit the mode change.")
    configured = (git(root, "config", "--get", "core.hooksPath") or "").strip()
    if configured.rstrip("/") in (".githooks", "./.githooks",
                                  os.path.join(root, ".githooks").rstrip("/")):
        return
    problem = ("core.hooksPath is %s in this clone, so .githooks/commit-msg never runs here. The "
               "hook is committed; the setting that runs it is not, and it does not travel - a "
               "fresh clone, a second machine and every colleague start without it. Nothing else "
               "reports its absence, which is why this line exists."
               % ("unset" if not configured else "set to %r" % configured))
    fix = ("Run: git config core.hooksPath .githooks - once per clone. If this project already "
           "keeps hooks in .git/hooks, move them into .githooks/ first: core.hooksPath replaces "
           "that directory wholesale. Record the command in the Entry patterns table of "
           "tooling.md so the next session in a fresh clone just runs it.")
    if in_ci():
        rep.advise(".githooks/commit-msg", problem + " Reported as advisory because this is a CI "
                   "checkout, where the setting cannot exist.", fix)
    else:
        rep.block(".githooks/commit-msg", problem, fix)


def git(root, *args):
    try:
        out = subprocess.check_output(["git", "-C", root] + list(args),
                                      stderr=subprocess.STDOUT)
    except (subprocess.CalledProcessError, OSError):
        return None
    return out.decode("utf-8", "replace")


def check_git(root, mem, rep, files):
    """Tier 2 only. Absent .git, none of this runs and nothing is reported as missing."""
    if not os.path.isdir(os.path.join(root, ".git")):
        return False
    listing = git(root, "ls-files")
    if listing is None:
        rep.advise(".git",
                   "There is a .git directory but git would not answer, so the three git checks "
                   "were skipped.",
                   "Run the script again where git works, or ignore this at tier 1.")
        return True
    tracked = set(p for p in listing.splitlines() if p)

    if not tracked:
        rep.block(".",
                  "The repository has no committed files at all. The memory exists on this "
                  "machine and nowhere else, which is the one thing this kit exists to prevent.",
                  "git add the memory files and commit them: "
                  "chore(memory): install agent memory system v8")
        return True

    untracked = [f for f in files if f.replace(os.sep, "/") not in tracked]
    if untracked:
        rep.block(untracked[0],
                  "%d memory file(s) exist but are not tracked by git: %s. They survive nothing: "
                  "not a new machine, not a clone, not review."
                  % (len(untracked), ", ".join(untracked[:6])),
                  "git add them and commit. If one of them is deliberately local, it belongs in "
                  "tooling.local.md, which .gitignore already excludes.")

    leaked_local = sorted(p for p in tracked if p.endswith(".local.md"))
    if leaked_local:
        rep.block(leaked_local[0],
                  "%s is tracked by git. The .local.md suffix is the kit's promise that a file "
                  "is never committed; this one was." % leaked_local[0],
                  "git rm --cached it, confirm *.local.md is in .gitignore, and treat anything "
                  "sensitive that was in it as compromised: rotate first, then remove the text.")

    if "*.local.md" not in read(os.path.join(root, ".gitignore")):
        rep.advise(".gitignore",
                   "*.local.md is not in .gitignore, so the one place the kit offers for a fact "
                   "that must not be committed is not actually protected.",
                   "Add the line *.local.md to .gitignore.")
    return True


# --- output -------------------------------------------------------------------------------

def emit(heading, items):
    print("%s (%d)" % (heading, len(items)))
    print("")
    for where, problem, fix in items:
        print("  %s" % where)
        for line in textwrap.wrap(problem, 92):
            print("      %s" % line)
        wrapped = textwrap.wrap(fix, 88)
        for i, line in enumerate(wrapped):
            print("      %s %s" % ("->" if i == 0 else "  ", line))
        print("")


def main():
    ap = argparse.ArgumentParser(
        description="Check an installed repo-memory carrier and say what to do about what is "
                    "wrong. Standard library only, no network, no host.")
    ap.add_argument("target", nargs="?", default=".",
                    help="the carrier root - the folder holding AGENTS.md (default: .)")
    ap.add_argument("--memory-dir", default=None, metavar="NAME",
                    help="force the memory folder name instead of auto-detecting docs/ or memory/")
    args = ap.parse_args()

    root = os.path.abspath(args.target)
    if not os.path.isdir(root):
        print("verify-install: %s is not a directory." % root)
        return 1

    rep = Report()
    mem = find_memory_dir(root, args.memory_dir)
    agents_text = read(os.path.join(root, "AGENTS.md"))
    pre, sections = split_sections(live(agents_text))
    kind, kind_why = carrier_kind(root, agents_text, sections)

    files = memory_files(root, mem)
    mem_texts = dict((rel, read(os.path.join(root, rel))) for rel in files)
    unattended = re.search(r"install:\s*unattended", agents_text, re.IGNORECASE) is not None

    check_index_files(root, rep, agents_text)
    check_level0(root, mem, rep)
    check_named_paths(root, mem, rep, sections)
    check_unresolved_markers(root, rep, files, unattended)
    if mem:
        check_traps(root, mem, rep)
    check_related_carriers(rep, sections)
    if mem:
        check_reporting(root, mem, rep, mem_texts)
    budgets, source = budgets_from_agents(sections, kind, rep)
    if mem:
        check_budgets(root, mem, rep, budgets, source, kind)
    check_identity_placeholders(rep, pre, sections)
    check_other_placeholders(root, mem, rep, files)
    if mem:
        check_folder_naming(root, mem, rep, files, mem_texts)
    check_secrets(root, rep, all_files_under_memory(root, mem))
    check_hook(root, rep)
    check_commit_guard(root, rep)
    has_git = check_git(root, mem, rep, files)

    tier = "1 - a folder: no git, no host, no automation"
    if has_git:
        tier = "2 - git, no automation found"
    if workflow_files(root):
        tier = "3 - a host with automation (workflows are committed here)"

    print("")
    print("verify-install  %s" % root)
    print("  memory folder : %s" % (mem + "/" if mem else "NOT FOUND"))
    print("  tier          : %s" % tier)
    print("  carrier       : %s (%s)" % (kind, kind_why))
    if unattended:
        print("  install       : declared UNATTENDED")
    for line in rep.facts:
        print("  %s" % line)
    print("")

    if rep.secrets:
        print("=" * 96)
        emit("SECRET-SHAPED VALUE IN THE MEMORY - fix this before anything else on this list",
             rep.secrets)
        print("=" * 96)
        print("")
    if rep.blocking:
        emit("BLOCKING - the memory is wrong or points at something that is not there",
             rep.blocking)
    if rep.advisory:
        emit("ADVISORY - the memory works, and it could be trusted more", rep.advisory)

    if not (rep.secrets or rep.blocking or rep.advisory):
        print("Nothing to report. Every path named in the index exists, no question is left "
              "unanswered,")
        print("no file is over budget and no credential-shaped value is committed.")
        print("")

    print("%d secret-shaped value(s), %d blocking, %d advisory."
          % (len(rep.secrets), len(rep.blocking), len(rep.advisory)))
    if rep.secrets:
        print("Exit 2: rotate the secret first, remove the text second.")
        return 2
    if rep.blocking:
        print("Exit 1: fix the blocking findings before you call this install finished.")
        return 1
    print("Exit 0: nothing blocking.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
