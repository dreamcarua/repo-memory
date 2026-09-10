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

The file is self-contained: all the templates are in Appendix A.

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
  Dropbox folder, an Obsidian vault, documents that are not code at all. The format and all five
  procedures work; where one leans on git it carries the no-git clause in the same line (Entry
  reads `docs/changelog.md` and file dates instead of recent commits; Exit writes its records
  before reporting). Install no workflows and no hook, and say so.
- **Tier 2 — git, any remote or none.** Commits, branches, "records in the same commit", the
  concurrency check in Entry, the `memory-v8` rule in step 6: plain git, so GitLab, Gitea, Forgejo,
  a bare repo over SSH or no remote at all all work.
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

Two more files go in at level 0, both about keeping the memory safe and current:

- `.github/workflows/memory-secret-scan.yml` (A.11) where there is CI to run it — the capability is "run a check on push", so elsewhere it is that host's CI, and with none it is a `pre-commit` hook or a manual pass — plus `*.local.md` in `.gitignore`. `tooling.md` says how to get into every system, which makes it the one memory file worth attacking; the scan stops a credential value being committed there, and `docs/tooling.local.md` takes anything that must not be committed at all. Read the top of A.5 first.
- `scripts/verify-install.py` and, where there is CI to run it,
  `templates/.github/workflows/memory-verify-install.yml` — both copied from this kit, never one
  without the other: the script is the check and the workflow is only its runner. Neither is in
  Appendix A for that reason. It re-runs step 6 point 2 on every push, so the memory cannot rot
  quietly after the install; advisory findings are printed and do not fail the build. No CI, or
  tier 1 — install neither, and run the script by hand or from a `pre-commit` hook.
- `.claude/hooks/memory-exit-reminder.sh` (A.12), registered in `.claude/settings.json` as its header shows. Exit and Checkpoint are instructions in a file the agent may or may not follow; the hook is where forgetting them stops being silent. The prose stays the substance — the hook cannot write memory, only notice that none was written. **Claude Code only, and git only**: `Stop`/`PreCompact` are Claude Code hook events and the script reads `git status`. For Cursor, Codex or Copilot, and for a tier-1 folder, there is no equivalent — the instruction in `AGENTS.md` is all there is. Install it where it works and say plainly where it does not.

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
the whole of the mechanism — there is nothing else to build. How the agent reads the other
`AGENTS.md` + `tasks.md`, by kind:

- a path on the same machine (`../other-project`, `/srv/projects/x`, `~/Documents/Client A`) — read the files; no network, no credentials;
- a git remote (`https://gitlab.com/org/repo.git`, `https://gitea.example.tld/org/repo`, or the SSH form) — `git clone --depth 1 --filter=blob:none` into a temp directory, read, delete it;
- a readable file tree over HTTP (a raw-file base URL) — one fetch per file;
- a host with an API (`github.com/<org>/<repo>`) — its MCP or CLI (`gh api`, `glab api`), no clone.

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
2. Verify with a machine, not by eye. Fetch `scripts/verify-install.py` from this kit and run it
   against the carrier root: `python3 verify-install.py <carrier path>`. Standard library, no
   network, no host, so it runs at tier 1 too. It reads the install you just made and checks what
   this step used to ask you to check by hand: the line budget, every path named in the Map and in
   Entry and Exit, unanswered `<?>`, a `traps.md` left as an empty skeleton, a Related carriers
   table holding only the placeholder, a workflow whose secrets are recorded nowhere, every file
   against its rotation budget, and a credential value anywhere in the memory folder. Fix
   everything it prints under BLOCKING, run it again until it exits 0, and give the user its
   closing line in step 7. Cannot fetch it? Say so in the summary and check those by hand — but do
   **not** grep for the words `token`, `secret` or `password`: `tooling.md`'s own threat-model prose
   contains them about twenty times on a correct install, and a check that cries wolf on a good
   install gets ignored on a bad one.
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
4. What is left for the human: any unset secrets; the HARVEST of the old chats (`HARVEST.md`, the
   highest-value thing left undone); every `<?>` still open, by question number.
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

## Appendix A. Templates

Copy them verbatim, replace the `<angle brackets>`, delete the lines you do not need. The English in the templates is deliberate (principle 3).

### A.1 · `AGENTS.md`

```markdown
# <Project name>

<What it is, for whom, current state — three lines max.>
Memory carrier: `<locator>` (this carrier) — a repo URL, a git remote, or a path on disk; see Related carriers for the kinds. `docs/` is the project's memory; this file is its index.
Project hub: `<hub locator>` — project-level memory (strategy, marketing, people, decisions). Delete this line if this IS the hub. `docs/` here is about this carrier only.
Owner: <name>. Tasks are closed by whoever set them; we hand over.
`<?>` marks a question nobody has answered yet, not a fact — here and anywhere in `docs/`. Ask the owner when it blocks the task; replace it in the same commit as the answer.

## Rules

- Talk to the user in <language> (or the language they write in). Dates <date format>, time <timezone>.
- Do on your own: <code edits, deploys, migrations, ...>
- Always ask first: money, irreversible actions, other people's resources, <...>
- Never: <...>
- Secrets never go into this repo. `docs/tooling.md` says where they live, not what they are.

## Entry — before the first action that changes project state

Chat without a folder? Nothing was loaded automatically: fetch this file and `docs/` from the carrier first.

1. `docs/tasks.md` — what is open, what is handed over and waiting, where the next move is ours.
2. `docs/handoff.md` — not empty means a previous session stopped mid-task. Continue, do not restart.
3. `docs/traps.md` — before the first edit of code or config. Always.
4. `docs/tooling.md` — before using any tool, MCP, server or account of this project.
5. Recent commits — is someone else working here right now? No git here: `docs/changelog.md` and the modification times under `docs/` answer the same question, less well.
6. Related carriers (below) — the task touches another carrier of this project, or knowledge that lives at project level: read its `AGENTS.md` and `tasks.md` too, before deciding anything. The Locator column says how to reach it; nothing here assumes an API.

Say one sentence: how many tasks are open, which are on us, what you start with. If a move is ours, say that first, even if asked about something else.

A task you were just given goes into `docs/tasks.md` now, verbatim, with the author's name. Before starting it, check it is not already done in the code.

## Context loss — when you can no longer quote the original task verbatim

You detect this yourself; nobody will tell you. Your context was compacted. Before the next action re-read `docs/handoff.md` and `docs/tasks.md`. Do not trust the summary for paths, numbers or what is already done; re-read the file.

## Checkpoint — during long tasks

Automatic. The user never asks for a checkpoint and is never reminded to.

After each completed step of a multi-step task and before any long operation: rewrite `docs/handoff.md` (task verbatim, done, not done, next action, numbers with sources). Rewrite, do not append. Empty it when the task is handed over.

## Rotation — the other half of writing

Automatic, like Checkpoint and Exit. Nobody asks for it.

A memory file that is read on every entry has a budget. Over budget, you rotate BEFORE adding
the new entry, in the same commit — with no git, in the same sitting, before you report:

| File | Budget | What moves out | Where it goes |
|---|---|---|---|
| `traps.md` | 25 KB | entries older than 90 days that describe a one-off incident | `traps/archive-<YYYY>-Q<n>.md`, one summary line left behind |
| `tasks.md` | 10 KB in a code repo · 25 KB in a project hub — **keep the one that matches this carrier, delete the other** | items whose author confirmed them done | `tasks/done-<YYYY>-MM.md`, verbatim, with the closing date |
| `handoff.md` | 2 KB | anything at all, on Exit | nowhere: it is emptied, and what survives becomes a line in `tasks.md` |

A hub's open tasks wait months on people, partners and money; a code repo's close when the code is written — hence the wider hub budget.
An item waiting on a person, a partner or money is not a task: it belongs in `docs/open-questions.md`. `tasks.md` is for what someone can act on now.

A trap that describes a permanent property of the system is evergreen: it stays regardless of age.
A trap that describes one incident, already fixed and unlikely to repeat, is a candidate to archive.
When in doubt keep it: archiving is cheap, losing a trap is not.

The archive is never read on entry. It is read when a question points at it: "has this happened
before", "why is it done this way". The index line left in the live file is what makes that possible,
so write it as a searchable sentence, not as a file name.

## Pre-flight — before an irreversible action, money, or a shared resource

Answer out loud in the reply. No answer to a line = no action.

1. WHOSE. Who else changes this? Are there commits in the last hours that are not mine?
2. SOURCE. Number · source · date. Primary source or a convenient sample?
3. WHOLE. The population or the first N rows? Did I ask the system for the total?
4. WORST. Which single check, if it came out differently, would cancel this? Do it first.
5. ROLLBACK. Exact command. Backup made and verified.

## Exit — automatic, before the word "done"

You run this unasked, every time a task changed project state — the user does not say "Exit" and does not remember these files exist. Also run it when the user says the task is finished, changes subject, or leaves; a task interrupted mid-way gets a Checkpoint instead.

1. What did I learn about this project? → `docs/traps.md`, `docs/tooling.md`
   Learned about the business rather than this carrier (market, a partner, a decision of the owner's) → the project hub, reached the way its locator says. One fact lives in one place.
2. What did I decide and why? → `docs/decisions.md` (create it on the first decision)
3. What is left open, including side findings nobody asked for? → `docs/tasks.md`
4. Can the owner see the result without effort? If not: screenshot, preview or link with the handover.
5. Report through the project channel → `docs/tooling.md` → Reporting.

Records go in the same commit as the change; with no git, write them before you report and log anything you changed outside `docs/` in `docs/changelog.md`. Hand over now, in this reply. A line leaves `tasks.md` when its author confirms, not when the work is done.
Two people ask for opposite things: pick one, name the conflict, tell <arbiter>.

## Map

| File | What | Read when |
|---|---|---|
| `docs/tasks.md` | open tasks, handed-over-and-waiting | entry. Always |
| `docs/handoff.md` | mid-task state of the last session | entry; after context loss |
| `docs/traps.md` | traps of this project | before the first edit. Always |
| `docs/tooling.md` | tools, access, entry patterns, reporting channel | before using any tool |
| `docs/decisions.md` | why it is this way | before changing something agreed |
| `docs/architecture.md` | sources of truth, ownership, logs, fallbacks | before touching a shared resource; when diagnosing |
| `docs/measurement.md` | how to measure, where numbers come from | before the first measurement |
| `docs/changelog.md` | changes git does not show; with no git, every change | after any change outside git |
| `docs/open-questions.md` | blocked until a human decides | before talking about plans |
| `docs/personal.md` | who sets tasks, how they accept results, how much autonomy is expected | before handing a result over; when two people want opposite things |
| `docs/traps/archive-<YYYY>-Q<n>.md` | traps rotated out of the live file, verbatim | never on entry; only when a question points back in time |
| `docs/tasks/done-<YYYY>-MM.md` | tasks confirmed closed, verbatim, with the closing date | never on entry; only when you need the history of a task |

## Related carriers — the same project, other carriers

**If this project is a single carrier, delete this whole section.** A table holding nothing but a
placeholder row is a lie the next session believes.

One project = one hub (`<project>-memory`: strategy, marketing, people, decisions) + N code carriers, each with its own memory about its own code. A fact lives in exactly one of them; this table says where to look for the rest.

| Carrier | Locator | What it is | Read its `AGENTS.md` + `tasks.md` when |
|---|---|---|---|
| <short name> | `<locator>` | <what it is> | <when the task touches it> |

The locator's kind is the whole of the mechanism, and one kind needs no network at all:
- a path on this machine — `../other-project`, `/srv/projects/x`, `~/Documents/Client A` — read the files;
- a git remote — `https://gitlab.com/org/repo.git`, `https://gitea.example.tld/org/repo`, or the SSH form — `git clone --depth 1 --filter=blob:none` into a temp directory, read, delete it;
- a readable file tree over HTTP — a raw-file base URL — one fetch per file;
- a host with an API — `github.com/<org>/<repo>` — its MCP or CLI, no clone.

A carrier you cannot reach: say so in the reply and do not guess what is in it.
A task that spans two carriers: one line in each `tasks.md`, each pointing at the other.

## Overrides of global rules

| Global rule | Here | Why | Since |
|---|---|---|---|
| <none yet> | | | |
```

### A.2 · `CLAUDE.md`

```markdown
@AGENTS.md

<!-- The line above is Anthropic's documented way to point Claude Code at an existing
     AGENTS.md: Claude Code reads CLAUDE.md, not AGENTS.md, so the import makes both read one
     file. See code.claude.com/docs/en/memory.
     Claude-specific additions only below. Everything shared with other agents lives in
     AGENTS.md. -->
```

### A.3 · `docs/tasks.md`

```markdown
# <Project> — open tasks

Updated: DD.MM.YYYY
Tracker: <link or "none">. This file holds only what the tracker does not: agent findings, own tech debt, handed-over-and-waiting, blocked.

🔴 breaks production · 🟡 unfinished tail · ⚪ queued · ⏸ waiting for a human decision

## 🔴 Breaks production

- **<symptom in one line>** — <next concrete step>. <where exactly: file:line, URL, table>

## 🟡 Tails — started, not finished

- <what was started> · <what remains> · [handed over DD.MM, waiting for <name>]

## ⚪ Queue

- **<task>** — <author>, DD.MM, via <who forwarded>: «<verbatim quote>». Next step: <one action>.

## ⏸ Waiting for a decision

| Task | Why it waits | Whose call | Since |
|---|---|---|---|

<!--
Rules (see AGENTS.md → Entry/Exit):
- A task is written the moment it is received, verbatim, with the author's name.
- Each line is a next concrete step, not the name of a problem.
- A line is deleted when its author confirms, not when the work is done. Deleted, not struck through.
- Sections by urgency, not by topic.
- Over ~80 lines is a signal that unfinished work accumulates, not a reason to split the file.
-->
```

### A.4 · `docs/traps.md`

```markdown
# <Project> — traps

Read before the first edit of code or config. Add an entry whenever something cost more than 15 minutes of surprise, in the same commit as the fix.

<!--
Format:
### Short name of the trap
**Symptom:** what you will see.
**Cause:** why it happens.
**Do:** the concrete action.
**Seen:** DD.MM.YYYY

Twelve classes worth looking for on purpose: several layers of the same thing (cache, copies, mirrors) · hidden execution order · a whole that breaks when a part is removed · silent loss in a named-field list · identifier without uniqueness guarantee · value without its unit · two implementations of the same logic · a default that points elsewhere · deploy resets what you did not mention · empty result of a narrowed filter · cache whose key does not contain what you changed · dormant defect woken by a change in data shape.
-->

_Nothing recorded yet._

Delete that line when you add the first trap; the format is in the comment above. An empty entry
skeleton is worse than an empty file, because a later session reads it as a trap somebody started
writing down and abandoned.
```

### A.5 · `docs/tooling.md`

```markdown
# <Project> — tooling, access, reporting

Read before using any tool, MCP, server or account of this project.

## What this file is, and what it must never become

This file is a map of *how to get in*: enough for a session with no history to use this project's
tools without asking a human. That is what makes it the most sensitive file in the memory folder.
The rules below are not style preferences.

**Who can read it once it is committed.** Everyone who can read this repository, now and for as
long as it exists: every collaborator, every fork, every CI job and every agent with read access
to any of those — and everyone in the world if the repo is ever made public. Git keeps history, so
a value committed here and deleted in the next commit is still in the repository. If this repo is a
spoke of a project hub, assume these facts also end up aggregated next to every other system's.

**What it may contain:** the name of a tool and what it is used for; which mechanism authorises it;
the *name* of a secret and *where it lives*; the steps of a recurring action; what the agent
deliberately does not do.

**What it must never contain: any value that grants access or aims an attack.** Never, not "avoid
where possible". That includes tokens, API keys, passwords and passphrases; connection strings with
credentials in them; signed URLs, invite links and webhook URLs; chat, channel and group ids;
account, project, zone, tenant, bucket and instance identifiers; internal hostnames and IP
addresses; and recovery details or answers to security questions.

Write the *name* of the secret and where it lives. Nothing else. If a session cannot do its job
without a value, that value belongs in the operator's secret store, and at most in
`docs/tooling.local.md` — never here.

**If a value has already been committed here, it is compromised.** Rotate it first, then remove the
text. Removing it without rotating changes nothing.

## `tooling.local.md` — what a local session may know and the repository must not keep

`docs/tooling.local.md` is for what an operator wants a local session to have and the repository
never to hold: a host that is not public, a personal path, a scratch identifier. It is covered by
`*.local.md` in `.gitignore`, so it is never committed and no one else's session ever sees it. It
does not exist by default — create it only when there is something to put in it, and keep secret
*values* out of it as well: a gitignored file is still a plaintext file on a laptop.

One fact still lives in one place. This file is the one that is read by default; if a fact lives in
the local file instead, leave a line here saying that it does, without saying what it is.

## Tools and connectors

Every table below ships with example rows so the shape is visible. Replace them with what this
project actually uses and delete the rest — a row left unedited is a lie the next session believes.

| Tool / MCP / connector | Used for | How to get in | Quirks |
|---|---|---|---|
| <host MCP or CLI — GitHub MCP, `gh`, `glab`, or plain `git` over SSH> | read/write this carrier from any chat | <how this project authorises it — connector, token in `<place>`>; write access to `<org>/*` | <e.g. the GitHub MCP pushes via `push_files`, one commit per logical change> |
| <file / shell tool> | local files and shell on <which machine or environment> | <what must be connected or configured before it works> | <e.g. each call is a fresh shell; no deletes without permission> |
| <database / backend MCP> | <SQL, functions, logs> | project ref lives in the operator's store, not here | <e.g. schema changes go through the migration call, not raw DDL> |
| <hosting / CMS / ads / analytics / ...> | | | |

## Secrets — the name and the place, never the value

| Secret | Lives in | Who can rotate |
|---|---|---|
| `<SECRET_NAME>` | <GitHub repo secrets / server env file / password manager> | <who> |
| `<SECRET_NAME>` | <...> | <who> |

Write the name that is actually set, not the one you expect: the name in the host's secret store and
the name in a local `.env` are regularly different, and a job reading the wrong one fails with an empty
variable rather than an error. `grep -h 'secrets\.' .github/workflows/*.yml | sort -u` lists the
names the workflows read — names only, which is all that belongs here.

Example — a project using the bundled `.github/workflows/report-to-telegram.yml` needs exactly two,
`TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`, both in GitHub repo secrets, rotated by the owner. The
chat id is itself a value: it goes in the secret store, not in this file. Delete this paragraph if
this project reports some other way.

`.github/workflows/memory-secret-scan.yml` fails the build if a value ever lands in the memory
folder. The capability it needs is "run a check on push": on another host, the same script in that
host's CI; with no CI at all, the same script in a `pre-commit` hook or run by hand before you
commit. It is a backstop either way, not permission to be careless.

## Entry patterns — how a recurring action is actually done here

One row per action somebody repeats. The value is in the fallback column: the primary path is
usually guessable, the fallback never is.

| Action | Steps | Fallback if the tool is down |
|---|---|---|
| <deploy a backend function> | commit under `<functions path>` → <CI workflow> deploys | <vendor CLI> through <shell tool> |
| <apply a schema change on production> | file under `<migrations path>` → <CI workflow> applies | <migration call of the database MCP> |
| <publish a site change> | | |

## Reporting

If this project has no reporting channel, say exactly that here — "No reporting channel. Exit ends at the commit." — and delete the rest of this section. No workflow is installed in that case, and an Exit that stops at the commit is complete.

Otherwise. Mechanism: commit a JSON file to `reports/YYYY-MM-DD-HHMM-<slug>.json` on the default branch → `.github/workflows/report-to-telegram.yml` sends it to the project chat. The workflow is installed only once its secrets are set; committed without them it fails on the first push. The channel is a choice: the commit-a-JSON-report half of the pattern is the same whether it is delivered to Telegram, Slack, Discord, e-mail or an internal webhook, and only the workflow's delivery step differs. If this project reports some other way, describe that here instead — what to commit or call, where, in what format.
**No CI, or no host at all.** The agent still writes `reports/YYYY-MM-DD-HHMM-<slug>.json`; delivery is whatever this project already has — a `curl` the agent runs itself at Exit, a `post-receive` hook or cron picking up new files under `reports/`, a folder somebody reads — or nothing, in which case the report is the commit message and the chat reply, and that Exit is complete. Say here which.
When: at Exit of every task that changed state (see AGENTS.md → Exit). Not for questions, reading, estimates.
Format: see `reports/README.md`. Plain text, no markup; the workflow escapes nothing.

## Access limits — what the agent deliberately does not do

| Action | Who does it | Why not the agent |
|---|---|---|
| Change repository visibility | owner | financial and security consequence, irreversible in seconds |
| Any payment | owner | always |
| Rotate a key in an external service | owner | agent cannot see consequences for other systems |
| Write a secret value into any memory file | nobody | see the top of this file |
```

### A.6 · `docs/handoff.md`

```markdown
# Handoff — mid-task state

<!--
IDLE. Nothing in flight. Only this comment = a previous session left no unfinished task.

When a task is in flight, replace everything below the title with this, and REWRITE it (do not append)
after each completed step and before any long operation. After a context compaction, re-read this first.

Updated: DD.MM.YYYY HH:MM

## Task verbatim
«author's wording, quoted» — author, DD.MM

## Constraints
what not to touch, with whom to agree

## Done
- what changed · where it lives · why

## Handed over, waiting
- to whom · when · answer?

## Did not work
- what was tried · result · why rejected

## Numbers and sources
- number · source · date

## State now
working system or not; what is broken; what is temporary and how to revert it

## Next single action
one concrete action, not a direction

When the task is handed over: put this comment back and delete the rest.
-->
```

### A.7 · `.claude/rules/example-path-rule.md`

```markdown
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
```

### A.8 · `.github/workflows/report-to-telegram.yml`

```yaml
name: report-to-telegram

# Agent commits reports/YYYY-MM-DD-HHMM-<slug>.json on main → this sends it to the project Telegram chat.
# Telegram is this kit's worked example, not a requirement. The pattern is: the agent commits a
# small JSON report, something delivers it. Slack, Discord, e-mail and internal webhooks are
# equally valid - replace the curl step below and leave the rest of the file as it is. The two
# capabilities are "run on push" and "hold a secret"; with no CI at all, the agent writes the same
# JSON file and runs the same curl itself, or the report is simply the commit message.
# Secrets required (repo → Settings → Secrets → Actions, or `gh secret set NAME`):
#   TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
# Install this file only once both secrets exist and are non-empty. Committed without them it fails
# on the very first push, and a memory kit whose first act is a red build does not get a second try.
# The trigger below says main: if this project's default branch is named something else, change it.
# Plain text on purpose. Telegram's markdown and HTML parse modes reject or mangle a message
# containing "<", ">" or an unbalanced "*" or "_", and a report is written by an agent that
# cannot know in advance which characters a summary will contain. A silently dropped report is
# worse than an ugly one, so nothing is escaped and no parse mode is set.

on:
  push:
    branches: [main]
    paths: ["reports/*.json"]

jobs:
  send:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Send new reports
        env:
          TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          CHAT: ${{ secrets.TELEGRAM_CHAT_ID }}
          BEFORE: ${{ github.event.before }}
          AFTER: ${{ github.sha }}
        run: |
          set -euo pipefail
          if [ -z "$TOKEN" ] || [ -z "$CHAT" ]; then
            echo "::error::TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is not set"; exit 1; fi
          if git cat-file -e "$BEFORE" 2>/dev/null; then
            FILES=$(git diff --name-only --diff-filter=A "$BEFORE" "$AFTER" -- 'reports/*.json')
          else
            FILES=$(git show --name-only --pretty= --diff-filter=A "$AFTER" -- 'reports/*.json')
          fi
          [ -z "$FILES" ] && { echo "no new reports"; exit 0; }
          for f in $FILES; do
            TEXT=$(jq -r '
              "📋 " + (.project // "project") + " · " + (.date // "") +
              "\n\n" + (.summary // "") +
              (if .breaks_if_not_done then "\n\n⚠ If not done: " + .breaks_if_not_done else "" end) +
              (if (.open_tasks // 0) > 0 then "\n\nOpen tasks: " + (.open_tasks|tostring) + ((.on_us // 0) as $u | if $u > 0 then " (" + ($u|tostring) + " on us)" else "" end) else "" end) +
              (if .waiting_for then "\n\nWaiting for: " + .waiting_for else "" end) +
              (if .link then "\n" + .link else "" end)
            ' "$f" | head -c 3900)
            RESP=$(curl -sS -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
              --data-urlencode "chat_id=${CHAT}" \
              --data-urlencode "text=${TEXT}" \
              --data-urlencode "disable_web_page_preview=true")
            echo "$RESP" | jq -e '.ok' >/dev/null || { echo "::error::Telegram refused $f: $RESP"; exit 1; }
            echo "sent $f"
          done
```

### A.9 · `reports/README.md`

````markdown
# reports/

One JSON file per report. Commit on `main` → `.github/workflows/report-to-telegram.yml` sends it. With no CI the file is written all the same and delivered by whatever this project has — including nothing, in which case it is the record and the chat reply is the delivery. Do not edit old reports; they are the delivery log.

File name: `YYYY-MM-DD-HHMM-<slug>.json` (<timezone>). Content, plain text only (no markdown, no `<` `>`):

```json
{
  "project": "<project>",
  "date": "03.09.2026 14:20",
  "summary": "Two or three sentences: what was done and what it changes for the owner. No list of steps.",
  "breaks_if_not_done": "One line: what would have broken or stayed broken.",
  "open_tasks": 6,
  "on_us": 2,
  "waiting_for": "<person> — <what you are waiting on them for>",
  "link": "https://…  (preview, screenshot, PR) — optional"
}
```

Send when a task changed project state. Do not send for questions, reading, estimates.
````

### A.10 · BOOTSTRAP - the line for a chat with no folder

```text
Project: <name>. Memory carrier: <locator>.
Before the first action that changes project state: read AGENTS.md from the carrier - a file read, a shallow clone, or a host API call, whichever the locator kind calls for - and run its Entry (tasks.md, handoff.md, traps.md, tooling.md, recent commits), then say the one-sentence state. Write back to the carrier at Exit. Reply in <language>.
```

### A.11 · `.github/workflows/memory-secret-scan.yml`

```yaml
name: memory secret scan

# Fails if a credential VALUE lands in the project's memory folder.
#
# docs/tooling.md tells an agent to write down how to get into every system. That file is useful
# exactly because it is specific, and dangerous for the same reason: it is model-authored, committed
# by default, copied into every fork, and kept in git history forever. The rule "names and places,
# never values" is prose, and prose is not enforcement. This is the enforcement.
#
# It is a backstop for the obvious shapes, not a secret scanner. It will not catch a hostname, an
# account id or a password that looks like a word. Read docs/tooling.md before writing, and treat a
# value that reaches this check as already compromised: rotate first, then remove the text.
#
# MEM is the memory folder. It is docs/ by default and memory/ on a GitHub Pages repo - set it to
# whichever this project uses.
#
# The capability is "run a check on push", not GitHub Actions: on another host run the same script
# in that host's CI, with no CI run it from a pre-commit hook or by hand. The patterns are portable.

on:
  push:
    paths: ["docs/**", "memory/**"]
  pull_request:
    paths: ["docs/**", "memory/**"]
  workflow_dispatch:

jobs:
  scan:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    env:
      MEM: docs
    steps:
      - uses: actions/checkout@v4
      - name: No credential values in the memory folder
        run: |
          set -uo pipefail
          if [ ! -d "$MEM" ]; then echo "no $MEM/ directory; nothing to scan"; exit 0; fi

          # Ten shapes that are a VALUE wherever they appear. Keep the list short and obvious;
          # a pattern that fires on ordinary prose gets ignored, which is worse than no check.
          PATTERNS='
          gh[pousr]_[A-Za-z0-9]{20,}
          \bsk-[A-Za-z0-9]{20,}
          AKIA[0-9A-Z]{16}
          xox[abprs]-[A-Za-z0-9-]{10,}
          [0-9]{8,10}:[A-Za-z0-9_-]{35}
          eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.
          -----BEGIN [A-Z ]*PRIVATE KEY-----
          sb[pous]?_[A-Za-z0-9]{20,}
          (postgres|postgresql|mysql|mongodb|redis|amqp)://[^:<>[:space:]]+:[^@<>[:space:]]+@
          [?&](X-Amz-Signature|X-Goog-Signature|sig|token)=[A-Za-z0-9%_-]{16,}
          '

          # Two of those carry a qualifier that was put there after running the list against real
          # carriers, and both are as narrow as the false positive they remove:
          #   \bsk-  - without the word boundary this fires on "task-", "risk-" and "disk-"
          #            followed by any 20 characters. A real key always starts at a boundary.
          #   <>     - a userinfo segment containing an angle bracket is a documented TEMPLATE
          #            (postgres://<user>:<password>@host), not a credential. A real password
          #            cannot carry a raw "<" in a URI anyway; it has to be percent-encoded.

          FOUND=0
          while IFS= read -r pat; do
            [ -z "$pat" ] && continue
            # Exclude the file that documents these shapes, if the project keeps one.
            # -e is required: a pattern starting with "-" (the PEM header) would otherwise
            # be parsed as options and that pattern would silently never run.
            if grep -rInE --exclude='*.local.md' -e "$pat" "$MEM" ; then
              FOUND=1
            fi
          done <<< "$PATTERNS"

          # The eleventh shape needs a step of its own. A run of 40 or more hex characters is what
          # several API keys look like - and equally what a content hash looks like in an asset
          # filename or a URL path. Unqualified, it fired four times on ONE image name inside a
          # public og:image URL in a real carrier's memory folder. A scan that goes red over a
          # picture is a scan somebody switches off, and then the other ten stop being read too.
          # So: match the whole whitespace-delimited token that contains the run, then drop that
          # token when the run is preceded by "/" or followed by an asset extension. A bare blob -
          # in a table cell, after "=", inside quotes - still fails the build.
          ASSETS='png|jpe?g|webp|gif|svg|ico|js|css|map|html?|woff2?|mp4|pdf|zip'
          if grep -rInoE --exclude='*.local.md' -e '[^[:space:]]*[0-9a-f]{40,}[^[:space:]]*' "$MEM" \
             | grep -vE "/[0-9a-f]{40,}|[0-9a-f]{40,}\.($ASSETS)" ; then
            FOUND=1
          fi

          if [ "$FOUND" = "1" ]; then
            echo "::error::A credential-shaped value is committed in $MEM/. Rotate it first, then remove the text - it is already in git history. See $MEM/tooling.md."
            exit 1
          fi
          echo "no credential-shaped values in $MEM/"
```

### A.12 · `.claude/hooks/memory-exit-reminder.sh`

```bash
#!/bin/sh
# memory-exit-reminder - the enforcement point for Exit and Checkpoint.
#
# CLAUDE CODE ONLY, AND GIT ONLY. Stop and PreCompact are Claude Code hook events, no other agent
# has them, and this reads `git status`, so outside a work tree it exits 0 and checks nothing. For
# Cursor, Codex or Copilot, and for a memory folder with no version control, the equivalent is the
# instruction in AGENTS.md (or .cursorrules) and nothing enforced - say so plainly rather than
# implying a backstop that is not there.
#
# WHY THIS EXISTS
# AGENTS.md asks the agent to run Exit before saying "done" and to rewrite handoff.md at every
# Checkpoint. Anthropic documents that instruction-file content is "delivered as a user message
# after the system prompt" and that "there's no guarantee of strict compliance", and says that
# anything which must run at a specific point should be a hook, because hooks "apply regardless
# of what Claude decides to do". The prose in AGENTS.md remains the substance: it says what to
# write and where. This script only makes forgetting it visible.
#   Hooks reference: https://code.claude.com/docs/en/hooks
#
# WHAT IT DOES
#   Stop        - if the session changed tracked files outside the memory folder and changed
#                 nothing inside it, exit 2. That blocks the stop and hands the message back to
#                 Claude, which can then write Exit or Checkpoint and stop normally.
#   PreCompact  - if anything is uncommitted, print a reminder that handoff.md is what survives
#                 compaction. Never blocks.
#
# WHAT IT DELIBERATELY DOES NOT DO
#   - It does not write memory. A hook cannot know what was learned; only the agent can.
#   - It does not run on SessionEnd. For that event the output and exit code are ignored, so a
#     SessionEnd hook cannot warn anyone about anything. Registering one would look like a
#     safety net and be nothing.
#   - It does not see work that was already committed. It reads the working tree, so a session
#     that commits code without memory in the same commit passes unnoticed. Catching that needs
#     a SessionStart companion that records HEAD - more moving parts than it is worth here.
#   - It does not block twice: the stop_hook_active guard lets the next stop through, so a
#     disagreement with the agent can never become a loop.
#
# INSTALL
# Copy to .claude/hooks/memory-exit-reminder.sh, chmod +x, and register it in
# .claude/settings.json. Merge these keys into an existing "hooks" block, do not replace it:
#
#   {
#     "hooks": {
#       "Stop": [
#         { "hooks": [ { "type": "command",
#                        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/memory-exit-reminder.sh" } ] }
#       ],
#       "PreCompact": [
#         { "hooks": [ { "type": "command",
#                        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/memory-exit-reminder.sh" } ] }
#       ]
#     }
#   }
#
# Set MEMORY_DIR below to memory if this project keeps its memory there instead of docs.
# POSIX sh and git only. No jq: it is not installed everywhere, and a hook that dies on a missing
# dependency fails silently, which is the one thing an enforcement point must not do.

MEMORY_DIR="docs"

INPUT=$(cat 2>/dev/null)

# Claude Code overrides a Stop hook that blocks repeatedly; it sets stop_hook_active once a hook
# has already continued the conversation. Honour it or risk looping until the cap.
case "$INPUT" in
  *'"stop_hook_active":true'*|*'"stop_hook_active": true'*) exit 0 ;;
esac

EVENT=$(printf '%s' "$INPUT" | sed -n 's/.*"hook_event_name"[[:space:]]*:[[:space:]]*"\([A-Za-z]*\)".*/\1/p')

# Outside a work tree there is nothing to compare; stay silent rather than guess.
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

CHANGED=$(git status --porcelain --untracked-files=all 2>/dev/null | cut -c4-)
[ -z "$CHANGED" ] && exit 0

IN_MEM=$(printf '%s\n' "$CHANGED" | grep -c "^$MEMORY_DIR/")
OUT_MEM=$(printf '%s\n' "$CHANGED" | grep -vc "^$MEMORY_DIR/")
[ -z "$IN_MEM" ] && IN_MEM=0
[ -z "$OUT_MEM" ] && OUT_MEM=0

if [ "$EVENT" = "PreCompact" ]; then
  echo "Checkpoint: this context is about to be compacted. $MEMORY_DIR/handoff.md is what survives it." >&2
  echo "If a task is in flight, rewrite handoff.md now: task verbatim, done, not done, next single action, numbers with sources." >&2
  exit 0
fi

if [ "$OUT_MEM" -gt 0 ] && [ "$IN_MEM" -eq 0 ]; then
  echo "Exit was not run. This session changed $OUT_MEM tracked file(s) and nothing in $MEMORY_DIR/." >&2
  echo "Before stopping, do one of these:" >&2
  echo "  - task finished  -> run Exit from AGENTS.md: traps.md, tooling.md, decisions.md, tasks.md, then report." >&2
  echo "  - task in flight -> rewrite $MEMORY_DIR/handoff.md (Checkpoint)." >&2
  echo "  - nothing was learned and nothing is left open -> say so in one line and stop; this will not ask again." >&2
  exit 2
fi

exit 0
```

### Levels 1-2 - created when there is a first entry to put in them

### A.13 · `docs/decisions.md`

```markdown
# <Project> — decisions

Newest on top. Old decisions are never deleted; they are marked superseded.
Three things people forget are decisions: a deliberate compromise by the owner; a rejected idea with the number that rejected it; a choice between conflicting requirements of two people.

## DD.MM.YYYY — <decision title>
**Decision:** what was decided.
**Why:** which options were considered and why this one.
**On what data:** number · source · date measured.
**Consequence:** what now works differently; what breaks if reverted.
**Status:** active | superseded by decision of DD.MM.YYYY | rejected
```

### A.14 · `docs/changelog.md`

```markdown
# <Project> — changes outside git

Only what git does not show: database edits, external service settings, CDN rules, manual runs, temporary changes. In a carrier with no git at all this file IS the commit log: every change gets a line, and Entry reads it where it would otherwise read recent commits. Last column is mandatory. Rotate to `docs/archive/<year>-Q<n>.md` quarterly.

| Date | What changed | How (script / command / UI) | Backup / how to revert |
|---|---|---|---|
| DD.MM.YYYY | | | |
```

### A.15 · `docs/open-questions.md`

```markdown
# <Project> — open questions

Blocked until a human decides. Answered → the item moves to `docs/decisions.md`. One-line pointer stays in `docs/tasks.md` (⏸ section); the full text lives here, not in both.

## <question in one line>
**Asked:** DD.MM.YYYY, to <name>
**Options:** A … / B …
**Recommendation:** …
**Blocked meanwhile:** what must not be done until answered.
```

### A.16 · `docs/architecture.md`

```markdown
# <Project> — architecture memory

Not a description of the code (the code shows that). Only what the code does not show.

## Sources of truth
| Data | Source of truth | Do NOT edit in | Note |
|---|---|---|---|

## What overwrites what
| Field | Written by | Overwritten by | Note (naming mismatches go here) |
|---|---|---|---|

## Trigger channels — everything that starts each recurring process
| Process | Channel 1 | Channel 2 | Which one is primary |
|---|---|---|---|

## Ownership
| Resource | Owner | Who else changes it | What I may do |
|---|---|---|---|

## Data boundaries
| Channel | Visibility | May carry | Must not carry |
|---|---|---|---|

## Logs — where each kind of failure lands
| Source | File / place | What is there | What will NOT be there |
|---|---|---|---|

## Fallback paths
| Action | Primary | Fallback | When it was needed |
|---|---|---|---|
```

### A.17 · `docs/measurement.md`

```markdown
# <Project> — measurement

Read before the first measurement. A number without source and date is a memory, not a fact.

## What we measure with
Tool, version, exact command.

## Method
What to warm up, how many runs, how to aggregate.

## Noise
Spread between identical runs; minimum meaningful difference.

## Baseline
Date · conditions · numbers · link to evidence.

## What the tool does NOT show

## Primary sources
| Metric | 🟢 Primary source | 🔴 Do NOT take from | Why |
|---|---|---|---|

## Billing unit
| Resource | Billed for | Rounding | Optimise this | Has NO effect |
|---|---|---|---|---|
```

### A.18 · `docs/personal.md`

```markdown
# <Project> — people

Only what changes the agent's next action. Nothing about people outside work.

## Who asks for what
| Person | Role | Sets tasks about | Accepts results as | Conflicts are settled by |
|---|---|---|---|---|

## Level of autonomy expected
Do without asking: …
Always ask: …

## Phrases that mean more than they seem
| They say | They mean |
|---|---|

## Already explained — do not ask again
- …
```
