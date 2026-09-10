#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""repo-memory - check-placeholders: fails the build if anything private leaked in.

The templates in this repo are placeholders. A placeholder that quietly turns back into a real
name, a real host or a real secret is the failure mode this repo cannot recover from, because
once the repo is public the leak is in the git history forever. This check runs on every push
and fails on five classes:

  1. Cyrillic characters outside an allowlisted path
  2. a forbidden proper noun (people, brands, hosts) - see NOTE below
  3. an e-mail address
  4. a credential-shaped string (nine patterns)
  5. a real-looking absolute home path: /Users/<someone> or /home/<someone>

NOTE on class 2: the forbidden nouns are stored as truncated SHA-256 hashes, not as text. A
denylist written out in plain text would publish, in a public repo, exactly the names it exists
to keep out. This is obfuscation, not secrecy: anyone who guesses a name can confirm the guess
by hashing it. That is fine - the goal is only that the names are not readable here and not
indexable, not that they are unrecoverable. Matching is by whole word, and by adjacent word pairs joined with "." or "-" so that a
host like "example.tld" or a handle like "some-bot" is caught too. That is what proper nouns
are, so whole-word matching is enough.
To add a term:  python3 scripts/check-placeholders.py --hash "the term"
Non-Latin names need no entry at all: class 1 already rejects every Cyrillic character.

  python3 scripts/check-placeholders.py          - check the tree, exit 1 on any violation
  python3 scripts/check-placeholders.py --hash X - print the line to paste into FORBIDDEN
"""
from __future__ import print_function
import hashlib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- the tiny allowlist -------------------------------------------------------------------
# Keep this as short as it is. Every entry is a hole in the check, so every entry is justified.
ALLOW = {
    # The MIT licence has to name the copyright holder. That is the one place a real name belongs.
    "LICENSE": {"terms"},
    # This file carries the regexes for classes 3-5, which are themselves credential-shaped and
    # path-shaped; it cannot scan itself for them without matching its own source. The term list
    # is hashed, so this file needs no exemption from class 2, and none from class 1.
    os.path.join("scripts", "check-placeholders.py"): {"email", "cred", "homepath"},
}
# The one legitimate appearance of a denylisted term: this kit's own canonical URL in README.md,
# which is the URL an adopter actually fetches INSTALL.md from. It is stored as a hash like every
# other term, so the owner's account name still appears nowhere in this file.
#
# The exemption is as narrow as it can be made. It applies only in README.md, only to this one
# term, and only on a line that also contains both halves of the canonical URL. A denylisted name
# anywhere else in README.md, or on a line that is not that URL, still fails the build.
SELF_URL_TERMS = {"fa4b4839ee870635"}
SELF_URL_PATHS = {"README.md"}
SELF_URL_MARKS = ("github.com/", "/repo-memory")

# Paths where Cyrillic (or any non-Latin script) is allowed because the text is *about* it.
# Empty on purpose: nothing in this repo needs it yet. Add a path here only together with a
# comment saying which example needs the non-Latin characters and why.
ALLOW_CYRILLIC = set()

FORBIDDEN = {
    "fa4b4839ee870635",
    "74c8299d0efedd2a",
    "8a67ce8e72698bf9",
    "c59a5c7610a89758",
    "d10f66b34e1acd28",
    "b1d8295b89ebe1c0",
    "bbaaf72c1ae4fe49",
    "eb91dc6b508d90d9",
    "ae47dcc81e048fcb",
    "183442d6a886c5e2",
    "a0804ccc7179f750",
    "ffb622df7e9926a3",
    "10b66e2bd553d4f4",
    "d3efa607c9de76ce",
    "32bb8f75dfd8fe03",
    "711b951b39d3e6eb",
    "a463ce1e0c054ff7",
}

# Written as escapes, not literal characters, so this file does not trip its own class 1.
CYRILLIC = re.compile(u"[\u0400-\u04FF\u0500-\u052F\u2DE0-\u2DFF\uA640-\uA69F]")
WORD = re.compile(r"[A-Za-z0-9]+")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# The home directory of a real account. Placeholders such as /home/<user> stay legal.
HOMEPATH = re.compile(r"/(?:Users|home)/(?!<)[A-Za-z0-9._-]+")

CREDENTIALS = [
    ("github token",       re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}")),
    ("openai key",         re.compile(r"sk-[A-Za-z0-9]{20,}")),
    ("aws access key id",  re.compile(r"AKIA[0-9A-Z]{16}")),
    ("slack token",        re.compile(r"xox[abprs]-[A-Za-z0-9-]{10,}")),
    ("telegram bot token", re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b")),
    ("jwt",                re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.")),
    ("private key block",  re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("long hex blob",      re.compile(r"\b[0-9a-f]{40,}\b")),
    ("supabase-style key", re.compile(r"\bsb[pous]?_[A-Za-z0-9]{20,}")),
]

SKIP_DIRS = set([".git"])


def candidates(line):
    """Whole words, plus adjacent pairs joined by '.' and '-' (hosts, handles)."""
    words = [w.lower() for w in WORD.findall(line)]
    out = set(words)
    for i in range(len(words) - 1):
        out.add(words[i] + "." + words[i + 1])
        out.add(words[i] + "-" + words[i + 1])
    return out


def walk():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for fn in sorted(filenames):
            full = os.path.join(dirpath, fn)
            yield full, os.path.relpath(full, ROOT)


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--hash":
        term = sys.argv[2].strip().lower().encode("utf-8")
        print('    "%s",' % hashlib.sha256(term).hexdigest()[:16])
        return 0

    violations = []
    scanned = 0

    for full, rel in walk():
        allowed = ALLOW.get(rel, set())
        try:
            with io.open(full, encoding="utf-8") as fh:
                lines = fh.read().splitlines()
        except (UnicodeDecodeError, IOError):
            continue  # binary or unreadable: nothing text-shaped to leak
        scanned += 1

        for n, line in enumerate(lines, 1):

            if "cyrillic" not in allowed and rel not in ALLOW_CYRILLIC:
                hits = CYRILLIC.findall(line)
                if hits:
                    violations.append(("cyrillic", rel, n,
                                       "%d Cyrillic character(s)" % len(hits)))

            if "terms" not in allowed:
                self_url_line = (rel in SELF_URL_PATHS
                                 and all(m in line for m in SELF_URL_MARKS))
                for cand in candidates(line):
                    ch = hashlib.sha256(cand.encode("utf-8")).hexdigest()[:16]
                    if ch not in FORBIDDEN:
                        continue
                    if self_url_line and ch in SELF_URL_TERMS:
                        continue
                    violations.append(("forbidden term", rel, n,
                                       "a denylisted proper noun"))
                    break

            if "email" not in allowed:
                for m in EMAIL.findall(line):
                    violations.append(("e-mail address", rel, n, m))

            if "cred" not in allowed:
                for name, rx in CREDENTIALS:
                    m = rx.search(line)
                    if m:
                        violations.append(("credential (%s)" % name, rel, n,
                                           m.group(0)[:20] + "..."))

            if "homepath" not in allowed:
                for m in HOMEPATH.findall(line):
                    violations.append(("absolute home path", rel, n, m))

    if violations:
        print("check-placeholders: FAILED - %d violation(s), %d files scanned\n"
              % (len(violations), scanned))
        for cls, rel, n, detail in violations:
            print("  %-26s %s:%d  %s" % (cls, rel, n, detail))
        print("\nThese must not reach a public repo. Replace them with placeholders.")
        return 1

    print("check-placeholders: OK - %d files scanned; no leaked names, addresses, "
          "secrets or paths." % scanned)
    return 0


if __name__ == "__main__":
    sys.exit(main())
