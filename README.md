# repo-memory

**Project memory for coding agents that lives with the project, not on one laptop.**

An always-loaded index under 150 lines, the detail in `docs/`, size budgets that archive instead of
deleting, and a session-end hook that speaks up when the code moved and the memory did not.

- **In the project, not in a home directory.** The memory is files that live next to the work. Put
  them in git and they are reviewed in pull requests, survive a new machine, and read the same for
  every agent and teammate with access; keep them in a plain folder and they still work. Editor-native
  memory is per machine by design: Claude Code documents its own auto memory as "not shared across
  machines or cloud environments."
- **Budgets that archive rather than delete.** Each memory file has a byte budget. Over budget, the
  eligible entries move to a dated archive file verbatim and a searchable index line stays behind, in
  the same commit as the change. Nothing is summarised away.
- **The write is the agent's job, not yours.** Entry, Checkpoint, Exit, Pre-flight and Rotation run
  unprompted, because the user will not remember that these files exist. A `Stop` hook is included as
  a partial backstop; it is Claude Code specific and it needs git, every other agent gets the
  instruction and nothing enforced, and you should read what it cannot see before you rely on it.

---

## What it is

A convention plus an installer. `AGENTS.md` is the index every session loads. `CLAUDE.md` is one
line that imports it. Everything else lives in `docs/`, read on demand:

| File | Created | What it holds | Read when |
|---|---|---|---|
| `tasks.md` | at install | what is open, what is handed over and waiting | every entry |
| `handoff.md` | at install | mid-task state of the last session | entry; after context loss |
| `traps.md` | at install | the ways this project has already bitten someone | before the first edit |
| `tooling.md` | at install | how to get in, where each secret lives (never its value), entry patterns, fallbacks | before using any tool |
| `decisions.md` | on first entry | why it is the way it is | before changing something agreed |
| `architecture.md` | on first entry | sources of truth, ownership, logs, fallbacks | before touching a shared resource |
| `measurement.md` | on first entry | how this project measures things and where numbers come from | before the first measurement |
| `changelog.md` | on first entry | changes git does not show — with no git, every change | after any change outside git |
| `open-questions.md` | on first entry | blocked until a human decides | before talking about plans |
| `personal.md` | on first entry | who sets tasks, how they accept results | before handing over a result |

A fresh install writes six files: `AGENTS.md`, `CLAUDE.md` and the four marked "at install". The other
six appear the first time there is something to put in them. An empty file that exists is a file a
later session reads, finds nothing in, and stops trusting.

`AGENTS.md` is capped at 150 lines. That is our number, not the convention's: the AGENTS.md
convention specifies no size at all. We set it under the 200-line ceiling Anthropic documents for
`CLAUDE.md`, and well under the 32 KiB Codex reads from `AGENTS.md` by default.

## What it needs to run — three tiers

**Tier 1 — a folder.** The memory is Markdown files in a directory. A folder on a desktop, a share
on your own server, a Dropbox folder, an Obsidian vault, a folder of documents that are not code at
all. No version control, no remote, no account, no CI. The format and all five procedures work here.
Two of them lean on git for one step each and carry the alternative in the same line: Entry reads
`changelog.md` and the file dates where it would read recent commits, and Exit writes its records
before reporting instead of in the same commit. Reporting has a no-CI path too — the agent writes
the report file and delivery is whatever you already have, including nothing, in which case the
report is the commit message and the reply in the chat.

**Tier 2 — git, any remote or none.** Commits, branches, "records in the same commit as the change",
the concurrency check in Entry, the branch rule at install. All of that is plain git: GitLab, Gitea,
Forgejo, a bare repo over SSH on your own machine, or a local repo with no remote at all. Where this
kit says GitHub it means GitHub; everywhere else it says git and means git.

**Tier 3 — a host with automation.** Three capabilities, named rather than abstracted: **run a check
on push** (the secret scan, the INSTALL build check), **hold a secret** (the reporting token), and
**fetch a file from a related carrier** (hub to spoke and back). GitHub Actions, GitHub repo secrets
and the GitHub MCP are the worked implementations shipped here, because one that has been run beats
four that have not. The same three on GitLab are CI, CI/CD variables and the Files API; on Gitea or
Forgejo, Actions, repo secrets and the API; on your own server, a `post-receive` hook, an env file
only the CI user can read, and `git clone --depth 1`. There are no vendor adapters in this kit and
there will not be: write down which capability you use in `docs/tooling.md`, and the next session
knows what it has.

## The five procedures

**Entry.** Before the first action that changes project state: read `tasks.md`, `handoff.md`,
`traps.md`, `tooling.md` and the recent commits — with no git, `changelog.md` and the file dates
instead — then say in one sentence what is open and what you are starting with. A chat with no
folder connected fetches these first.

**Checkpoint.** After each completed step of a long task and before any long operation, rewrite
`handoff.md`: the task verbatim, what is done, what is not, the next action, numbers with their
sources. Rewrite, never append. This is Manus's "recitation" applied to a file that survives
compaction.

**Pre-flight.** Before anything irreversible, before money, before a shared resource, five questions
answered out loud: who else writes here; what is the source of this number and its date; is this the
whole population or a convenient sample; which single check, if it came out differently, would
cancel this, and have you run it; what is the exact rollback command. No answer to a line means no
action.

**Exit.** Whenever a task changed project state, or the user says it is finished, or changes subject,
or leaves: write what was learned to `traps.md` and `tooling.md`, the decisions to `decisions.md`,
what is still open to `tasks.md`, then report. Records go in the same commit as the change; with no
git, they go in before the report, and anything changed outside the memory folder gets a line in
`changelog.md`.

**Rotation.** Files have budgets: `handoff.md` 2 KB; `traps.md` 25 KB in a code repo and 50 KB in a
project hub, because a hub accumulates traps across a whole business rather than one codebase;
`tasks.md` 10 KB in a code repo and 25 KB in a project hub, because a hub's open items wait months
on people and money while a code task closes when the code is written. Over budget, rotate before
adding, archive verbatim, leave one searchable sentence behind. A budget is a signal, not a licence
to break the eligibility rule: over budget with nothing eligible, the agent archives nothing and
writes one line in `open-questions.md` instead.

## Hub and spokes

A project that spans repositories gets one hub, `<project>-memory`, holding business-level memory,
plus N code carriers each holding memory about its own code. Every `AGENTS.md` carries a
"Related carriers" table naming the others. A carrier is addressed by a locator, and the locator's
kind decides how it is read: a path on the same machine is a file read, a git remote is a shallow
clone into a temp directory, a raw-file base URL is one fetch per file, a host with an API is an API
call. Only the last of the four needs a vendor. A fact lives in exactly one of them: business facts in
the hub, code facts in the repo they describe. A task that spans two gets one line in each, each
pointing at the other.

This is single source of truth with a link table. It is not clever. It is the part that stops the
same number being written down twice and drifting.

## Install

This is a ten-minute conversation, not a prompt you start and walk away from. The agent works
through nine questions with you — who owns this, what it may do unasked, where a finished task gets
reported, what is open right now, what language to speak to you in — and those answers are most of
what makes the memory worth reading six months later. The block is at the top of `INSTALL.md`. Fill
it in first.

Then point an agent at the installer:

```
Install project memory in <locator: a repo, a git remote, or a folder>, following the
installer at https://github.com/dreamcarua/repo-memory/blob/main/INSTALL.md — read that
file in full before you start. My answers to the block at the top of it follow. If the
project has a hub, add the Project hub line to AGENTS.md and a row for this repo in the
hub's Related carriers table.

<your answers here>
```

If you truly cannot be in the session, write `UNATTENDED: the agent decides, blanks are real blanks`
where the answers go. You get a thinner install, and the installed `AGENTS.md` says so near the top,
so a later session can tell a missing answer from a settled fact.

Before the install reports back, it runs `scripts/verify-install.py`. It is the only check in this repo that
reads an *installed* carrier rather than the kit: every path `AGENTS.md` names exists, no install
question was left unanswered, `traps.md` is not an abandoned skeleton, no file has grown past its
rotation budget, no credential value is committed. Standard library, no network, no host, so it runs
on a tier-1 folder; a template workflow re-runs it on every push where there is CI, and advisory
findings do not fail the build.

`INSTALL.md` is generated from `src/INSTALL-head.md` plus `templates/` by `src/build.py`. Do not edit
it by hand: a CI check fails the build when the committed file and the templates disagree. That check
exists because on my own estate the templates moved and the installer did not, and thirteen of the
sixteen repositories that had memory installed by then ended up without a rotation rule as a
result. One anecdote, but a
cheap check.

## Bringing over what already happened

Most of what a project knows is sitting in chats that are about to be closed. `HARVEST.md` is a
prompt you paste into each old one; it returns traps, decisions, open tasks and numbers in a fixed
shape, marked for reliability and for whether they belong to the business or to the code, and the
installer merges the result into the right files. It is the highest-value ten minutes in this kit and
it is the step everyone skips.

## Before you commit `tooling.md`

`tooling.md` is a map of how to get into your systems, written by a model and committed to git. Read
the threat model at the top of the template before you let an agent fill it in. The short version:
names of secrets and where they live, never values, and "value" includes chat ids, webhook URLs,
connection strings and account or project identifiers. A gitignored `tooling.local.md` is available
for facts that should not be committed at all. If a value was already committed, rotate it first and
remove the text second: removing it alone changes nothing, because git keeps history.

A template secret-scan workflow is included and runs on every push to the memory folder, where there
is CI to run it. With no CI, the same patterns belong in a `pre-commit` hook or in a manual pass
before you commit; the capability is "run a check on push", not "GitHub Actions".

## What this builds on

The `AGENTS.md` file name and the cross-vendor convention come from
[agents.md](https://agents.md/), stewarded since December 2025 by the Agentic AI Foundation under the
Linux Foundation. The one-line `CLAUDE.md` containing `@AGENTS.md` is Anthropic's own documented
recommendation, not an invention of this kit.

The design leans on published work and says so: Manus on
[context engineering](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
for recitation and for keeping failures in context; Anthropic on
[effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
for just-in-time retrieval and structured note-taking; Karpathy's
[LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) for the raw → wiki →
schema layering and for the idea of linting a knowledge base; MemGPT and Letta for the older and more
rigorous version of paging memory against a budget; Cline's Memory Bank for showing what a
file-based memory bank looks like in practice.

## Alternatives, named properly

If you want memory that needs no setup at all, your editor probably already has it; the tradeoff is
that it lives on one machine.

The closest thing to this kit is [mex](https://github.com/mex-memory/mex): also repo-local, also
shared through git, with a stronger drift checker than anything here. If you are choosing between
them, `mex check` validates more, and this kit says more about what happens when a memory file grows
too large and about what an agent may write down concerning your access paths.
[mainline](https://github.com/mainline-org/mainline) is git-native memory for coding agents and is
worth a look too.

What is left for this kit is a narrow case: several repositories belong to one project, the memory
has to be reviewable by people, and the failure you are actually afraid of is the agent quietly
stopping to write.

## Honest limits

This has been running on seventeen repositories belonging to one owner across five businesses. That
is n=1 on the operator, and every observation in the kit comes from that estate.

The byte budgets are chosen, not derived. 150 lines is argued above against Anthropic's documented
200. The 50 KB, 25 KB, 10 KB and 2 KB figures are judgement calls that produced reasonable behaviour
on one estate; treat them as defaults to change, and change them when rotation starts evicting
entries you still needed, or when entry stops feeling cheap.

The traps figure has already been changed once, and how it failed is worth copying. A hub's
`traps.md` reached 46.7 KB against a 25 KB budget while its oldest entry was 65 days old, so no
entry was eligible under the 90-day rule: the budget said rotate and the eligibility rule said you
may not. A session resolved the contradiction by archiving evergreen traps to hit the number, and
the file was back over budget the next morning — the rule had produced exactly the loss it exists
to prevent. Raising the hub budget was the smaller half of the fix. The other half is that a budget
now states plainly what it is: a signal, not a licence to break the eligibility rule. If your
budgets never collide with your eligibility rules, you have not run them long enough yet.

The version says v8 because the design went through eight revisions in private before this release.
Versions 1 through 7 are not published and are not coming.

The procedures are prose in a file the agent reads. Anthropic states plainly that instruction files
are "delivered as a user message after the system prompt" with "no guarantee of strict compliance."
That is why the `Stop` hook exists, and why it is honest about what it cannot see: it reads the
working tree, so a session that commits code and omits memory in the same commit passes unnoticed.
It is also Claude Code only, and it needs git.

Tier 1 is real, and it is not equal. In a folder with no git there is no diff to review, no commit
to bind a record to, no cheap answer to "is somebody else editing this right now", and the `Stop`
hook is inert because it reads `git status`. Checkpoint and Rotation are unaffected; Entry loses its
concurrency check and falls back to `changelog.md` and file dates; Pre-flight loses the first of its
five questions and its rollback becomes a copy of the folder; Exit keeps every word of its content
and loses only the atomicity of the write. That is the whole cost, and it is why `changelog.md`
exists.

## Licence

MIT.
