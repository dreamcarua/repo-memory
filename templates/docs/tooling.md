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
