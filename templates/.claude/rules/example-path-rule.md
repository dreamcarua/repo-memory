---
paths:
  - "src/generated/**"
---

# Editing generated files (example — replace with a rule of your own, or delete this file)

Everything below is an illustration of the shape, not a rule about your project.

- Files under `src/generated/` are produced by `<generator command>`. Edit the source under
  `<path to the source>` instead; an edit made here is silently reverted by the next run.
- After changing the source, re-run `<generator command>` and commit the source and the
  regenerated output in the same commit, or the two drift apart.

<!--
Path-scoped rules load only when the agent reads a matching file, and cost nothing otherwise.
Use one for a warning that is true of a few files and would be dead weight in AGENTS.md:
"this file has a second copy, edit both", "run X after touching this", "never edit the output".
Two or three lines is the right size. A rule that is true of every task belongs in AGENTS.md.

They do NOT survive context compaction unless the matching file is re-read afterwards, so a warning
that must never be lost also goes into a header comment of the file itself.
Equivalents for other agents:
  Cursor:  .cursor/rules/<name>.mdc  with frontmatter  globs: ["src/generated/**"]  alwaysApply: false
  Copilot: .github/instructions/<name>.instructions.md  with frontmatter  applyTo: "src/generated/**"
Keep the three in sync or use only this one plus header comments in the files.
-->
