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
3. `docs/traps.md` — before the first edit of code or config. Always. A trap that then changes what you do earns `Memory-Used: traps.md#<slug>` in that commit's message — see Rotation.
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

## Surprise — write the moment an expectation turns out wrong

A trigger, not a phase: it fires mid-task, whenever a system behaves differently from how you were confident it would behave. Write it to `docs/traps.md` **now**, before you finish the thought. This is the one place where writing beats finishing: the symptom is still there at Exit, the reason is not, and the reason is the half worth having.

The bar is the expectation, not the error. A command that fails is ordinary work and is not this: `npm ci` exits 1 on a missing peer dependency, you install it, nothing to write. An expectation that was wrong is this: the deploy reports success and the site still serves the old bundle, because the CDN keys its cache on a path you did not change — you were certain a green deploy meant a live change, and it does not.

Same shape as any trap — symptom, cause, what to do, date — and the cause is the point: **why** it happened, not only what you saw. About a tool as well as the code, it goes in `docs/tooling.md` too.

## Rotation — the other half of writing

Automatic, like Checkpoint and Exit. Nobody asks for it.

A memory file that is read on every entry has a budget. Over budget, you rotate BEFORE adding
the new entry, in the same commit — with no git, in the same sitting, before you report:

| File | Budget | What moves out | Where it goes |
|---|---|---|---|
| `traps.md` | 25 KB in a code repo · 50 KB in a project hub — **keep the one that matches this carrier, delete the other** | entries older than 90 days that describe a one-off incident | `traps/archive-<YYYY>-Q<n>.md`, one summary line left behind |
| `tasks.md` | 10 KB in a code repo · 25 KB in a project hub — **keep the one that matches this carrier, delete the other** | items whose author confirmed them done | `tasks/done-<YYYY>-MM.md`, verbatim, with the closing date |
| `handoff.md` | 2 KB | anything at all, on Exit | nowhere: it is emptied, and what survives becomes a line in `tasks.md` |

An item waiting on a person, a partner or money is not a task: it belongs in `docs/open-questions.md`. `tasks.md` is for what someone can act on now.

A trap that describes a permanent property of the system is evergreen: it stays regardless of age.
A trap that describes one incident, already fixed and unlikely to repeat, is a candidate to archive.
When in doubt keep it: archiving is cheap, losing a trap is not.

**Usefulness ratchets over age.** An entry that ever changed what a session did is never archived, whatever its age. When a trap you read changes what you then do, put `Memory-Used: traps.md#<slug of its heading>` in that commit's message — in the message, never in the file, because a mark written into `traps.md` would be erased by the very rotation it governs, and would churn the file on every read. Before archiving an entry, ask git: `git log --format='%(trailers:key=Memory-Used,valueonly)' | grep -qx 'traps.md#<slug>'`, or `git log --grep='^Memory-Used: traps.md#<slug>$' -1`. A hit means keep. No mark is not evidence the entry is dead, only that nobody has said otherwise — so among unmarked entries the 90-day rule decides exactly as before. **No git, no commit log, no ratchet:** at tier 1 age is all there is, and that is the whole of what tier 1 loses here.

The budget is a signal, not a licence to break the eligibility rule above. Over budget with nothing
eligible: archive nothing, write one line in `docs/open-questions.md` — file, size, budget, nothing
eligible under the 90-day rule, needs a human decision — and carry on with the task.

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
