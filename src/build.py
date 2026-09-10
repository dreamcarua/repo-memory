#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""repo-memory - build: assembles INSTALL.md from src/INSTALL-head.md and templates/.

INSTALL.md is a BUILD ARTEFACT, not a source. Do not edit it by hand: the next run of
build.py overwrites the edit. The sources are:
  src/INSTALL-head.md  - the whole text of the instruction, up to Appendix A
  templates/*          - the templates themselves, verbatim, in the code blocks of Appendix A

Why this exists: in v8.3 the Rotation section appeared in templates/AGENTS.md and did NOT
appear in INSTALL.md. Every installation after that point set up a carrier without the
rotation rule - that is exactly how 13 of 16 carriers ended up without one.

  python3 src/build.py           - assemble and write INSTALL.md
  python3 src/build.py --check   - do not write; exit 1 if INSTALL.md has drifted

--check runs in CI (.github/workflows/install-build-check.yml) so that the drift is caught
by a machine, not by an agent who happened to notice.
"""
import argparse
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEAD = os.path.join(ROOT, "src", "INSTALL-head.md")
OUT = os.path.join(ROOT, "INSTALL.md")

BOOTSTRAP = (
    "Project: <name>. Memory carrier: <locator>.\n"
    "Before the first action that changes project state: read AGENTS.md from the carrier "
    "- a file read, a shallow clone, or a host API call, whichever the locator kind calls for "
    "- and run its Entry (tasks.md, handoff.md, traps.md, tooling.md, recent commits), then say "
    "the one-sentence state. Write back to the carrier at Exit. Reply in <language>.\n"
)

# (appendix heading, path under templates/ or None, fence language, fence)
APPENDICES = [
    ("A.1 · `AGENTS.md`",                              "AGENTS.md",                              "markdown", "```"),
    ("A.2 · `CLAUDE.md`",                              "CLAUDE.md",                              "markdown", "```"),
    ("A.3 · `docs/tasks.md`",                          "docs/tasks.md",                          "markdown", "```"),
    ("A.4 · `docs/traps.md`",                          "docs/traps.md",                          "markdown", "```"),
    ("A.5 · `docs/tooling.md`",                        "docs/tooling.md",                        "markdown", "```"),
    ("A.6 · `docs/handoff.md`",                        "docs/handoff.md",                        "markdown", "```"),
    ("A.7 · `.claude/rules/example-path-rule.md`",     ".claude/rules/example-path-rule.md",     "markdown", "```"),
    ("A.8 · `.github/workflows/report-to-telegram.yml`", ".github/workflows/report-to-telegram.yml", "yaml", "```"),
    # A.9 contains its own ``` inside, so its fence is one character longer
    ("A.9 · `reports/README.md`",                      "reports/README.md",                      "markdown", "````"),
    ("A.10 · BOOTSTRAP - the line for a chat with no folder", None,                              "text",     "```"),
    ("A.11 · `.github/workflows/memory-secret-scan.yml`",     ".github/workflows/memory-secret-scan.yml", "yaml", "```"),
    ("A.12 · `.claude/hooks/memory-exit-reminder.sh`",        ".claude/hooks/memory-exit-reminder.sh",    "bash", "```"),
    ("__SPLIT__", None, None, None),
    ("A.13 · `docs/decisions.md`",                     "docs/decisions.md",                      "markdown", "```"),
    ("A.14 · `docs/changelog.md`",                     "docs/changelog.md",                      "markdown", "```"),
    ("A.15 · `docs/open-questions.md`",                "docs/open-questions.md",                 "markdown", "```"),
    ("A.16 · `docs/architecture.md`",                  "docs/architecture.md",                   "markdown", "```"),
    ("A.17 · `docs/measurement.md`",                   "docs/measurement.md",                    "markdown", "```"),
    ("A.18 · `docs/personal.md`",                      "docs/personal.md",                       "markdown", "```"),
]

SPLIT = "### Levels 1-2 - created when there is a first entry to put in them\n"


def read(path):
    with io.open(path, encoding="utf-8") as fh:
        return fh.read()


def build():
    parts = [read(HEAD).rstrip("\n") + "\n"]
    for title, rel, lang, fence in APPENDICES:
        if title == "__SPLIT__":
            parts.append("\n" + SPLIT)
            continue
        body = BOOTSTRAP if rel is None else read(os.path.join(ROOT, "templates", rel))
        if not body.endswith("\n"):
            body += "\n"
        if fence in body:
            raise SystemExit("build: fence %r occurs inside %s" % (fence, rel))
        parts.append("\n### %s\n\n%s%s\n%s%s\n" % (title, fence, lang, body, fence))
    return "".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="do not write; exit 1 if INSTALL.md does not match the build")
    args = ap.parse_args()

    built = build()
    current = read(OUT) if os.path.exists(OUT) else ""

    if args.check:
        if built == current:
            print("INSTALL.md matches the build from src/INSTALL-head.md + templates/.")
            return 0
        import difflib
        diff = list(difflib.unified_diff(current.splitlines(True), built.splitlines(True),
                                         "INSTALL.md (in the repo)", "INSTALL.md (rebuilt)"))
        sys.stdout.write("".join(diff[:200]))
        print("\nINSTALL.md has drifted from templates/. Run: python3 src/build.py")
        return 1

    if built == current:
        print("INSTALL.md unchanged.")
        return 0
    with io.open(OUT, "w", encoding="utf-8") as fh:
        fh.write(built)
    print("INSTALL.md assembled (%d bytes)." % len(built.encode("utf-8")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
