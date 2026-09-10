# Project memory system installer · v8

**For a human. Read this part before you hand the file to an agent.**

Installing is a conversation of about ten minutes, not a prompt you start and walk away from. The
agent works through the block below with you, and those answers are most of what makes the memory
worth reading later: an install where nobody answered produces a file full of `<?>` that every later
session treats as fact.

Fill in what you can, paste it into the chat together with this file, and write: "Install the memory
system into project <name>. My answers are at the top." Open that chat somewhere with the project
folder connected, or with a host MCP, or with an authenticated CLI in a shell. A plain folder with no
version control is a supported target: see the three tiers at the top of step 0.

Everything the install has to fill in is in Appendix A. The five files it only copies and runs — the
verifier, two workflows and two hooks — are named in Appendix C with the URL to fetch each from.

## The answers — before the install starts

    1. WHAT IT IS. What the project is, for whom, what state it is in. Three lines.
    2. PEOPLE. Who owns it. Who confirms a task is really done. Who decides when two people
       want opposite things.
    3. AUTONOMY. What the agent may do on its own. What it must always ask about first. What it
       must never do.
    4. TOOLS AND ACCESS. Which MCPs, connectors, servers, databases and panels this project's
       sessions use, and where the secrets live - the NAME and the PLACE, never the value.
    5. REPORTS. Where should a finished task be reported: Telegram, Slack, Discord, e-mail, an
       internal webhook, an existing mechanism you already have, or nowhere. "Nowhere" is a real
       answer and means no reporting workflow is installed at all.
    6. TRACKER. Is there a task tracker? Link. If there is, the memory holds only what it does not.
    7. OPEN NOW. What is open right now, in your own words, with who asked for each.
    8. ONE TRAP. One thing here that has already cost somebody an afternoon.
    9. HOW TO TALK TO YOU. Which language, which date format, which timezone.

**If you will not be in the session at all**, replace the whole block with exactly this line:

    UNATTENDED: the agent decides, blanks are real blanks.

The agent then infers what it can, leaves `<?>` where it cannot, and records the unattended install
in `AGENTS.md`. A worse install, supported because a thin memory beats none — not because it is
equivalent.

---

## For Claude: the answer gate, before anything else

Create nothing and commit nothing until one of these is true:

- the human has given you the answer block with at least **2, 3, 5 and 9** answered; or
- the human has written `UNATTENDED: the agent decides, blanks are real blanks`.

If neither is true, stop and ask, once, in one message, quoting the block. Do not begin "to save
time", and do not read silence as permission. Those four block because the repository cannot supply
them: who decides, what you may do unasked, whether a reporting channel is installed at all, and how
you speak to the user. The rest can be inferred well enough to be worth a guess.

When the human chose the unattended line, put this immediately under the `Owner:` line of
`AGENTS.md`, with the date filled in, and carry it through every later edit until somebody removes
it:

    Install: UNATTENDED on <DD.MM.YYYY>. Nobody answered the install questions. Every `<?>` in
    these files is a missing answer, not a settled fact - ask the owner before relying on one.

## For Claude: what you do and what you do not do

You create **layer 1 of memory** in the project: the index file `AGENTS.md` (read at start), `CLAUDE.md` (a one-line import) and the `docs/` folder (read on demand). This is not project documentation. It is what is **not visible from the code**: traps, agreements, open tasks, how to get into the tools, where to send the report.

Five principles that are not up for discussion:

1. **Assume nothing was loaded automatically.** With a folder connected, `CLAUDE.md` is read on its own; in a chat without one, or in a cloud session, it is not. Hence the fetch instruction at the top of `AGENTS.md` → Entry, and the BOOTSTRAP line the install hands over.
2. **Budget.** `AGENTS.md` ≤ 150 lines (aim for ~100). Our number, not the convention's, which specifies no size at all: it sits under the 200-line ceiling Anthropic documents for `CLAUDE.md` and well under the 32 KiB Codex reads from `AGENTS.md` by default. Every line is paid for by every session; anything not needed in **every** task goes into `docs/`.
3. **System files in English, content in the user's language.** `AGENTS.md`, the templates and the headings are in English (Cyrillic costs about 2× the tokens for the same content). The text of traps, decisions and tasks in `docs/` is in the language the user writes in.
4. **No secrets in the repository.** `docs/tooling.md` says **where** a secret lives, not what it is.
5. **A file is created when there is something to write in it.** Level 0 is six files. The rest of the templates (Appendix A) come when there is a first entry.

Do not: describe architecture visible from the code; rewrite the rules "more softly"; create empty level 1–2 files; ask permission for every step — ask once (step 2) and do it.

---

## Step 0. Environment and carrier — one table

**Three tiers. Establish which one this install is on and name it in the closing summary.**

- **Tier 1 — a folder.** Markdown files in a directory: a desktop, the owner's own server, a
  Dropbox folder, an Obsidian vault, documents that are not code at all. The format and all six
  procedures work; where one leans on git it carries the no-git clause in the same line (Entry
  reads `docs/changelog.md` and file dates instead of recent commits; Exit writes its records
  before reporting). Install no workflows, no hooks and no commit guard, and say so — and say the
  one thing tier 1 loses outright: Rotation's usefulness ratchet reads the commit log, and there
  is no commit log here, so age alone decides what is archived.
- **Tier 2 — git, any remote or none.** Commits, branches, "records in the same commit", the
  concurrency check in Entry, Rotation's usefulness ratchet, the commit guard of step 3 and the
  `memory-v8` rule in step 6: plain git, so GitLab, Gitea, Forgejo, a bare repo over SSH or no
  remote at all all work.
- **Tier 3 — a host with automation.** Exactly three capabilities: **run a check on push**, **hold
  a secret**, **fetch a file from a related carrier**. GitHub Actions, repo secrets and the GitHub
  MCP are written out below because they are the ones that have been run; elsewhere the same three
  are GitLab CI + CI/CD variables + Files API, Gitea/Forgejo Actions + repo secrets + API, or a
  `post-receive` hook + a root-only env file + `git clone --depth 1`. Write no adapter: name the
  capability in `docs/tooling.md` and leave the implementation to the operator.

Work this out and show the user a three-row table:

| What | How to check | Consequence |
|---|---|---|
| Is a folder connected? Is it a git repo? Is there a remote? | `ls`, `git remote -v` (through whatever file or shell tool is available) | where the memory will live, and which tier this is |
| How can you write to the carrier: a host MCP, an authenticated CLI (`gh`, `glab`, …), a plain git remote, or nothing but the filesystem? What file and shell tools are there? | the session's tool list; the CLI's own auth check; `git remote -v` | what to write files with; what to record in `tooling.md`. Any one is enough — a CLI is not a downgrade, and the filesystem alone is tier 1, not a failure |
| What already exists: `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.cursor/rules/`, `.github/copilot-instructions.md`, `docs/`, `CHANGELOG`, `TODO` | search the root | what to merge instead of duplicating |

**The memory folder.** `docs/` by default. If `docs/` holds `CNAME`, `index.html` or `.nojekyll` it is a published site (GitHub Pages and every equivalent): the memory goes into `memory/`, and `docs/` becomes `memory/` in every template. Verified 03.09.2026 on a pilot.

Choosing the carrier:

- **a repo exists** → the memory goes in it: `AGENTS.md` in the root, `docs/` next to it;
- **a folder with no git** → offer `git init` and a private remote on the owner's host (ask in step 2); if they decline, or there is no host, the folder itself is the carrier — tier 1;
- **no files at all** (the project lives in chats) → a private carrier `<project>-memory` on the owner's host, or a folder on the machine that will hold it; `AGENTS.md` in its root.

## Step 1. Collect what is already known, before asking anything

For an existing project, read without asking:

- `README*`, the structure to depth 2, the manifests (`package.json`, `composer.json`, `pyproject`, `wp-config`…);
- any existing agent instruction files — in full;
- the last 30 commits: messages with `fix`, `hotfix`, `revert`, `again`, `finally` are candidates for `traps.md`;
- `TODO`/`FIXME` in the code and, if the host has an issue tracker, its open issues — candidates for `tasks.md`;
- the workflows in `.github/workflows/`, `supabase/`, `wrangler.toml`, `vercel.json` — candidates for `tooling.md` → Entry patterns;
- mentions of a bot, a webhook, `sendMessage`, `TELEGRAM` — an existing reporting mechanism.

Draft the filled-in version and **ask only about what you could not work out**.

Do not take an existing `CLAUDE.md` or `README.md` at face value: check them against the file tree. On the pilot both described a different repository and `docs/README.md` named a folder that did not exist. A document that contradicts the code goes into `traps.md` and onto the rewrite list, not into `AGENTS.md`.

## Step 2. Interview — close the gaps in the answer block

The nine answers are at the top of this file and the human has already given them to you. This step
is only about what is still missing after step 1. Ask in one message, using the question tool if
there is one, otherwise a numbered list. Quote the number from the block so the human can see what
they are answering.

Ask only the numbers still unanswered, in the wording of the block above, plus what step 1 could not
settle: for **4**, each MCP, connector, server, database and panel, and where each secret lives — the
name and the place, never the value; for **5**, whether a delivery mechanism already exists and which
one (a file picked up by CI, a webhook, a function, a command the agent runs itself, or nothing); for
**6**, the tracker link, after which `tasks.md` holds only what the tracker does not; for **7**, the
open items verbatim with the author of each.

If the user says "decide for yourself" for a particular question, fill it in from step 1, mark what
stays unknown with `<?>`, and put one line in `docs/open-questions.md` naming the question number, so
it is answerable later. That is per-question. It is not the same as the unattended install, which is
declared once, up front, and recorded in `AGENTS.md`.

## Step 3. Create the level 0 files

If step 0 chose `memory/` rather than `docs/` (a repo that publishes `docs/` as a site), substitute it now, in every path of every template you copy: the templates all say `docs/`.

| File | Template | What to fill in |
|---|---|---|
| `AGENTS.md` | A.1 | name, three lines about the project, carrier locator, owner, Rules, `<arbiter>`, and the language, date format and timezone from question 9; then obey the delete-me notes inside the template itself (Map rows, Related carriers, the Rotation budget, Overrides); the `Install: UNATTENDED` line only if it was |
| `CLAUDE.md` | A.2 | unchanged |
| `docs/tasks.md` | A.3 | the open tasks from question 7, as quotes |
| `docs/traps.md` | A.4 | the trap from question 8 and the candidates from the commits. No trap to record? Leave the "nothing recorded yet" line in place rather than a blank entry skeleton |
| `docs/tooling.md` | A.5 | everything from question 4 and step 1; the Reporting block after step 4 |
| `docs/handoff.md` | A.6 | unchanged (the "idle" state is the comment alone) |

Merge rules, if the project already has instruction files:

- out of the contents of an existing `CLAUDE.md` / `.cursorrules` / `copilot-instructions.md` you carry into `AGENTS.md` **only what is not visible from the code**: exceptions, traps, agreements; descriptions of the structure and build commands you remove, or keep as a single line;
- you move the original into `docs/archive/<file>.<date>.md` and write about that in `docs/changelog.md` (create the file — now there is something to write);
- `.cursor/rules/*.mdc` with `globs:` you leave as they are — that is conditional loading, it does not compete for the budget;
- the new `CLAUDE.md` is one line, `@AGENTS.md` — Anthropic's own documented recommendation, because Claude Code reads `CLAUDE.md` and not `AGENTS.md`, so the import stops two copies drifting apart. Cursor, Codex and Copilot read `AGENTS.md` directly.

Then the machinery: five files that are copied, not filled in. Appendix C has the path of each in
this kit; fetch them from there rather than retyping them. Prose does not hold, and each of these
turns one written rule into something that runs.

- `.githooks/commit-msg` + `git config core.hooksPath .githooks` + `*.local.md` in `.gitignore`.
  The guard refuses a commit whose staged files change the project and change nothing in the memory
  folder — the case the `Stop` hook structurally cannot see, and the one Exit's own rule ("records
  in the same commit as the change") makes ordinary. It is the only enforcement in the kit that
  works at tier 2 with no host at all. **Two things to say out loud to the user, not to skip.**
  First: hooks are not versioned, so the file is committed under `.githooks/` and the setting that
  runs it is per clone — a fresh clone, a second machine and every colleague start without it.
  Run the config command yourself now, and put it in the Entry patterns table of `tooling.md`;
  `verify-install.py` reports an unset `core.hooksPath` as BLOCKING, which is what keeps the
  omission from being silent. Second: the one escape is `Memory-Skip: <why>` in the commit message
  — the refusal message names it, so the user learns it at the moment they need it, and
  `git log --grep='^Memory-Skip:'` says how often the project reaches for it. Do not install it in
  a repo that has hooks in `.git/hooks` without moving those into `.githooks/` first:
  `core.hooksPath` replaces that directory wholesale. No git at all — skip it and say so.
- `scripts/verify-install.py` and, where there is CI to run it,
  `.github/workflows/memory-verify-install.yml` — never one without the other: the script is the
  check and the workflow is only its runner. It re-runs step 6 point 2 on every push, so the memory
  cannot rot quietly after the install; advisory findings are printed and do not fail the build.
  No CI, or tier 1 — install the script alone and run it by hand.
- `.github/workflows/memory-secret-scan.yml` where there is CI to run it. `tooling.md` says how to
  get into every system, which makes it the one memory file worth attacking; the scan stops a
  credential value being committed there, and `docs/tooling.local.md` takes anything that must not
  be committed at all. Read the top of A.5 first. Set `MEM` to `memory` if step 0 chose that folder.
- `.claude/hooks/memory-exit-reminder.sh`, registered in `.claude/settings.json` as its header
  shows. **Claude Code only, and git only**: `Stop`/`PreCompact` are Claude Code hook events and
  the script reads `git status`. For Cursor, Codex or Copilot there is no equivalent — the
  instruction in `AGENTS.md` and the commit guard above are all there is. Set `MEMORY_DIR` the same
  way. Install it where it works and say plainly where it does not.

File-level technical warnings (edit both copies, change the owner after copying) do not go into `AGENTS.md`: they go into `.claude/rules/<topic>.md` with `paths:` (template A.7) **and** a header comment in the file itself, because a conditional rule does not survive compaction and a file header does.

## Step 3a. A project that already has some memory layout — migration without losses

A `notes/` or `wiki/` folder, a hand-rolled `docs/`, a `CLAUDE.md` grown over months, a `.cursorrules` nobody has opened in a year — whatever a human or an earlier agent already wrote down is memory, and it is worth more than the empty templates you are about to add. Three rules, not up for discussion:

1. **No existing memory file is overwritten.** What is there stays, same content, same path — including a file that shares a name with a template, such as `tasks.md` or `traps.md`. Create only what is missing (usually `tooling.md` and an empty `handoff.md`) and merge into an existing file, never over it. Notes living elsewhere (`notes/`, `wiki/`, a single `NOTES.md`) stay where they are and get pointed at from the map in `AGENTS.md`; moving them is the owner's separate task.
2. **The old `CLAUDE.md` is not deleted, it moves.** A verbatim copy → `docs/archive/CLAUDE.md.<date>.md` in the same commit; its blocks that do the work of Entry, a checklist, Exit, a map or overrides move into `AGENTS.md` (in English, template A.1), and its project rules and traps into `AGENTS.md` → Rules or `traps.md` — **nothing is thrown away**. The new `CLAUDE.md` is `@AGENTS.md`. Per-system subfolders (`docs/<system>/`) stay where they are; the map points at them.
3. **The installation goes into the `memory-v8` branch, not into `main`.** The owner sees the diff and merges it themselves; the rollback is deleting the branch. The first line in `tasks.md` is "merge `memory-v8`".

Check before committing: the memory folder's file list is the same plus the new ones; no pre-existing file's `wc -l` went down; the old `CLAUDE.md` is in `docs/archive/`.

## Step 3b. A project made of several repositories — hub and spokes

A project almost never lives in one repo: there is marketing and strategy (not code) and there are one or more code systems. The model:

- **the hub** — `<project>-memory`, private: strategy, marketing, sales, partnerships, people, business-level decisions;
- **the spokes** — the code carriers of the project: memory about their own code, their own deploys, the traps of their own system.

The link is made by two insertions, both at installation time:

1. In the hub — a `## Related carriers` section (template A.1) with one row per spoke: name · locator · what it is · when to look there.
2. In every spoke — the line `Project hub: <hub locator>` under the carrier line, point 6 in Entry, and a line in Exit: "learned about the business rather than about this code → write it to the hub".

**How a carrier points at another carrier.** A locator is whatever addresses it, and its kind is
the whole of the mechanism — there is nothing else to build. The four kinds, and how the agent
reads the other `AGENTS.md` + `tasks.md` from each, are written out in template A.1 under Related
carriers: copy that list into the carrier rather than paraphrasing it here, so one wording governs.
Write the locator in the form the agent will actually use, record in `docs/tooling.md` what it needs
to use it, and report a carrier you cannot reach rather than guessing at it.

The one-place rule: **a fact lives in exactly one carrier** — business in the hub, code in the spoke. An agent working in the dashboard that learns something about the market writes it to the hub, not to itself. A task touching both gets one line in each `tasks.md`, each pointing at the other.

Check: in every carrier the "hub" line or the "Related carriers" table leads to the rest; no fact is in two files.

## Step 4. Reports

The pattern is channel-agnostic: the agent writes a small JSON report, and something delivers it.

Question 5 decides this step, and one of its answers is "nowhere".

- **"Nowhere", or no answer in an unattended install** → no workflow, no `reports/` folder, one line
  under `docs/tooling.md` → Reporting: "No reporting channel. Exit ends at the commit." Skip to step
  5. A supported outcome, not a degraded one.
- **A mechanism already exists** → describe it in `docs/tooling.md` → Reporting: what to commit or
  call, where, in what format, when. Install no workflow. Done.
- **A channel is wanted and there is CI to run it** → create
  `.github/workflows/report-to-telegram.yml` (A.8) and `reports/README.md` (A.9), under the rule
  below. The capabilities are "run on push" and "hold a secret"; on another host use that host's
  two and change nothing else in the pattern.
- **A channel is wanted and there is no CI** (tier 1, or tier 2 with no host) → `reports/README.md`
  (A.9), no workflow. The agent writes the report file at Exit and delivers it with whatever
  exists: a `curl` it runs itself, a `post-receive` hook or cron that picks up new files under
  `reports/`, a watched folder — or nothing, in which case the report is the commit message and the
  reply in the chat. Name which one in `docs/tooling.md` → Reporting. A desktop project with no CI
  is not a project this kit cannot report from.

**Do not commit the workflow until its secrets are set.** Committed without them it fails on the
first push and the project's first experience of this kit is a red build. Cannot set them now?
Install no workflow: describe the channel in `docs/tooling.md` → Reporting and put "set the two
secrets, then add A.8" in `docs/tasks.md`.

`reports/README.md` (A.9) ships with placeholders. Fill `<project>`, `<timezone>`, `<person>` and the
example values in with this project's before committing it: every later report is copied from it.

  **Find the real secret names in this carrier** rather than taking them from `.env.example`: on the pilot the host held `TG_BOT_TOKEN`/`TG_CHAT_ID` against `TELEGRAM_*` in `.env.example` and the workflow failed with an empty variable. `grep -h 'secrets\.' .github/workflows/*.yml | sort -u` and `gh secret list -R <org>/<repo>` say what each side actually uses; reuse those names and set the missing ones yourself, **always with `--body`** (`gh secret set TG_CHAT_ID -R <org>/<repo> --body "<value>"`) — interactive `gh secret set` waits for a paste and Enter writes an empty secret. The bot id is not the chat id: send one message in the target chat, then read `getUpdates`. A command, or nothing — never "go into the settings and press".
- The first report is about the installation itself and it is the test of the channel. Name it
  exactly as A.9 defines: `reports/YYYY-MM-DD-HHMM-memory-installed.json`. No channel, no first
  report — say so in the closing summary. If the install went to the `memory-v8` branch the workflow
  will not fire (A.8 triggers on `main`), so do not commit a report that cannot be delivered: put
  "send the install report after merging" in `docs/tasks.md`. If the default branch is not `main`,
  change the workflow's `branches:` line first.

## Step 5. Carry the history over from the old chats

The most valuable thing in the project has already happened, in chats that will be closed soon. Give the user `HARVEST.md` from this kit: "Paste it into every old chat of this project and forward the result back here." Merge what comes back:

| From HARVEST | Where | Rule |
|---|---|---|
| traps | `docs/traps.md` | duplicates merge into one entry; without a symptom it is not a trap, it is history |
| decisions | `docs/decisions.md` (create it) | with no "on what data", mark it `🔬 source unknown` |
| open tasks | `docs/tasks.md` | as a quote, with the author; check whether it is already done in the code |
| tools, access, entry patterns | `docs/tooling.md` | secrets — only "where it lives" |
| structure: sources of truth, what overwrites what, logs | `docs/architecture.md` (create it) | only what is not visible from the code |
| numbers | wherever they are needed | a number with no source gets a `🔬`, it is not thrown away |

A contradiction between two chats is not settled silently: both versions into `open-questions.md`, one question to the owner.

## Step 6. Commit and check

1. One commit: `chore(memory): install agent memory system v8`.

   **How to write it.** A host MCP → its batch push in a single call. An authenticated CLI or a git
   remote in a shell → stage, commit, `git push` as normal; that is a first-class path, not a
   fallback. Git with no remote → commit locally and say so. No git at all (tier 1) → write the
   files, and the install itself is the first line of `docs/changelog.md`; there is nothing to push
   and nothing is missing. The GitHub MCP cannot delete files, so an old `CLAUDE.md` is overwritten
   by the import and its copy goes into `docs/archive/` in the same commit.

   **Where to commit.** No git at all: skip this paragraph — there are no branches, and the rollback
   is the copy of the folder you took first. Otherwise the default branch, unless one of these is
   true, in which case use a branch called `memory-v8` and make "merge `memory-v8`" the first line
   of `tasks.md`:

   - the repo is not the owner's, or it is public;
   - the default branch is protected, or your push is rejected;
   - **somebody else is working in it right now** — the newest commit on the default branch is by
     another author *and* under 24 hours old. Check both halves (`git log -1 --format='%an · %ar'`,
     or the MCP's commit list): a history that merely contains other authors does not qualify, and
     treating it as concurrent activity sends every install to a branch nobody asked for.
2. Verify with a machine, not by eye. Run `python3 scripts/verify-install.py <carrier path>`
   (Appendix C). Standard library, no network, no host, so it runs at tier 1 too. It reads the
   install you just made and checks by machine everything this step used to ask you to check by
   eye — the line budget, every path the index names, unanswered `<?>`, an empty trap skeleton, a
   placeholder-only carriers table, a workflow whose secrets are recorded nowhere, every file
   against its budget, an unset `core.hooksPath`, and a credential value anywhere in the memory
   folder. Fix everything it prints under BLOCKING, run it again until it exits 0, and give the
   user its closing line in step 7. Cannot fetch it? Say so in the summary and check by hand — but
   do **not** grep for the words `token`, `secret` or `password`: `tooling.md`'s own threat-model
   prose contains them about twenty times on a correct install, and a check that cries wolf on a
   good install gets ignored on a bad one.
3. Run Entry from `AGENTS.md` once, **out loud** — the first sentence of a session with memory. If
   it will not come out because `tasks.md` is empty, decide which empty it is: genuinely nothing
   open, say so and move on; question 7 never answered, write one line in `tasks.md` saying the
   open-task list was never collected, so the next session reads the silence as ignorance, not calm.
4. Send the first report (step 4).

## Step 7. What to tell the user at the end — five lines

1. What was created (the list of files), in which carrier, which of the three tiers this install is
   on and what that tier does not give them, and the verifier's closing line from step 6.
2. The starting budget: how many lines there are in `AGENTS.md`.
3. The BOOTSTRAP line for chats without a folder — ready to copy (template A.10, filled in).
4. What is left for the human: `git config core.hooksPath .githooks` in every other clone of this
   repo, on every machine, because that setting does not travel and the commit guard is inert
   without it; any unset secrets; the HARVEST of the old chats (`HARVEST.md`, the highest-value
   thing left undone); every `<?>` still open, by question number.
5. The first Entry sentence, the one you just said.

---

## Appendix B. Where to write what — one table for Claude

| Fact | Where |
|---|---|
| applies in **every** task of the project | `AGENTS.md` |
| applies only when certain files are edited | `.claude/rules/*.md` with `paths:` + a header comment in the file |
| a task just given, or done but not yet confirmed | `docs/tasks.md` |
| work broke off mid-task; every step of a long task | `docs/handoff.md` (rewrite it) |
| a surprise that cost more than 15 minutes | `docs/traps.md`, in the same commit |
| a system behaved differently from how you were sure it would | `docs/traps.md`, **now**, mid-task — cause first (AGENTS.md → Surprise) |
| a trap you read changed what you then did | `Memory-Used: traps.md#<slug>` in that commit's message — never in the file (AGENTS.md → Rotation) |
| this commit genuinely needs no memory | `Memory-Skip: <why>` in that commit's message |
| how to get into a tool, where a secret lives, how to send a report | `docs/tooling.md` |
| why this way and not another; a rejected idea with the number that rejected it | `docs/decisions.md` |
| a change made outside git (database, panel, CDN, manual run) | `docs/changelog.md` |
| waiting on a human decision | `docs/open-questions.md` + one line in `tasks.md` |
| source of truth, ownership, trigger channels, logs, fallback paths | `docs/architecture.md` |
| what to measure with and how, where a number comes from, the billing unit | `docs/measurement.md` |
| who asks for what, how they accept it, with whom to agree it | `docs/personal.md` |
| what is visible from the code | **nowhere** |

Budget: `AGENTS.md` ≤ 150 lines (argued under principle 2). `tasks.md` at around 80 lines is a signal, not a limit; the rest of `docs/` is unlimited, because it is read on demand.

---

## Appendix C. The five files that are copied, not filled in

Appendix A holds what you must **edit**: every template there has angle brackets in it that only
this project's answers can fill. These five you **copy and run**; at most you set one variable at
the top of each. Pasting them through this installer added 9.6 KB to a file whose size is its main
complaint, and gave them a way to drift — a copy here can be stale while the file it copies is not.
So they are fetched from the kit instead: the repository you took this file from, at the paths
below.

| Path in the kit | Install to | Needs | Set before committing |
|---|---|---|---|
| `templates/.githooks/commit-msg` | `.githooks/commit-msg`, `chmod +x` | git (tier 2) | nothing; then `git config core.hooksPath .githooks`, once per clone |
| `scripts/verify-install.py` | `scripts/verify-install.py` | nothing (tier 1) | nothing |
| `templates/.github/workflows/memory-verify-install.yml` | `.github/workflows/` | CI (tier 3) | nothing |
| `templates/.github/workflows/memory-secret-scan.yml` | `.github/workflows/` | CI (tier 3) | `MEM:` — `docs` or `memory` |
| `templates/.claude/hooks/memory-exit-reminder.sh` | `.claude/hooks/`, `chmod +x` | Claude Code + git | `MEMORY_DIR` — `docs` or `memory`; register it in `.claude/settings.json` |

Cannot fetch them — no network in this session, or the kit is unreachable? Install what you can,
say plainly in the closing summary which of the five are missing and what each would have caught,
and put a line in `docs/tasks.md` for the owner. Do not reconstruct one from memory: a guard that
is subtly wrong is worse than one that is absent, because the absent one is not trusted.

---

## Appendix A. Templates

Copy them verbatim, replace the `<angle brackets>`, delete the lines you do not need. The English in the templates is deliberate (principle 3).
