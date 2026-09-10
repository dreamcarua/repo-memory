# HARVEST — pull the memory out of an old chat

**For a human.** The most valuable thing in the project has already happened — and it lives in chats that will be closed soon. HARVEST gets it out while the chat still opens.

The order:

1. Open a long old chat of the project. Priority goes to the one with the most rework, argument and correction; that is where the traps are.
2. Paste the **prompt** into it (below, from the line `PROMPT ↓` to `↑ END`). Change nothing.
3. Wait for the answer, then copy all of it.
4. In a new chat write: `Here is a HARVEST from an old chat of <project>. Merge it into the memory.` and paste what you copied.

One chat, one HARVEST. The three longest chats of a project cover most of its history. Where each thing goes is the agent's decision: business knowledge into the hub `<project>-memory`, knowledge about code into the code repo it belongs to.

If the chat is nearly full and the answer breaks off, write in the same chat: `Continue from section N.`

---

PROMPT ↓

This session will be closed soon, and it holds knowledge about the project that exists nowhere else. Extract it in the format below — this is a handover to the next agent, who starts from nothing.

Rules you do not break:
- Write **only what is not visible from the code and the documentation**. Descriptions of structure, file names, standard commands — skip them.
- Every fact carries a reliability mark: `✅` verified in this session · `🔬` assumption · `⏳` was true as of a date.
- Every number comes with its source and its date. If you do not remember the source, put `🔬`, but keep the number.
- Invent nothing and smooth nothing over. An empty section is better than a plausible one.
- Mark every item `[BUSINESS]` or `[CODE]` — the first goes into the project memory, the second into the repository memory.
- Language: the one we have been speaking in. Format: markdown, in a single message.

If space is short, sections 2, 4 and 9 are mandatory; shorten the rest.

**1. The project — three lines.** What it is, for whom, in what state as of this chat.

**2. Traps.** Everything that cost more than fifteen minutes of surprise, and everything that had to be fixed twice. For each:
```
### <short name>
**Symptom:** what was visible from outside.
**Cause:** the real cause.
**Do:** what to do next time.
**Seen:** DD.MM.YYYY · ✅/🔬 · [CODE] or [BUSINESS]
```

**3. Decisions.** What was decided and why this way; which options were rejected and with what number; which compromises were taken deliberately. Format: decision · why · on what data · consequence · date.

**4. Open tasks.** Everything that was asked for and not finished; done and not handed over; handed over and not confirmed; found by you and never mentioned to anybody. For each: a quote of the wording, who the author is, the date, the **next concrete step**, the state (not started / tail / handed over DD.MM waiting for <name>).

**5. Tools and access.** Which MCPs, connectors, scripts and panels were used; how you got onto the server, into the database, into the admin panel; where the secrets live — **the name and the place, never the value**; what was done as a workaround when a tool refused; where the reports were sent. **Do not write down identifiers either** - project refs, zone ids,
bucket names, account and tenant ids, chat ids, internal hostnames and webhook URLs all let somebody
aim at the right target, and this text is going to be committed to a repository. Name the kind of
identifier and where it is kept, the way you do for a secret.

**6. Structure that is not visible from the code.** The source of truth for the main data; which process overwrites what; **all** the trigger channels of every recurring process (cron in a workflow, a scheduler in the database, an external service); who else changes those resources; where the logs are and what never lands in them; the fallback paths.

**7. People.** Who sets tasks, in what form they accept a result, what has already been explained and should not be explained a second time, with whom to settle a conflict of requirements. Work only.

**8. The numbers the decisions stood on.** `number · source · date`, or with a `🔬`.

**9. What went wrong in this chat.** Mistakes that had to be redone; where exactly you misunderstood the project; what should have been said to you in the first sentence. This is the most valuable section — do not skip it and do not soften it.

**10. One sentence for the next session.** The state of the project as it would be said at entry: how many tasks are open, which are on us, what to start with.

↑ END

---

## What the agent in the new chat does with this

| Section | Where | Rule |
|---|---|---|
| 2 traps | `traps.md` of the carrier named by the `[CODE]`/`[BUSINESS]` mark | duplicates merge into one entry; without a symptom it is history, not a trap |
| 3 decisions | `decisions.md` | with no "on what data", mark it `🔬 source unknown` |
| 4 tasks | `tasks.md` | as a quote, with the author; first check whether it is already done |
| 5 tools | `tooling.md` | names and places only: no secret values and no identifiers. Read the threat model at the top of `tooling.md` before merging and drop anything that does not pass it |
| 6 structure | `architecture.md` | only what is not visible from the code |
| 7 people | `personal.md` | nothing outside work |
| 8 numbers | wherever they are needed | a number with no source gets a `🔬`, but is not thrown away |
| 9 what went wrong | `traps.md` + `handoff.md` | this is the main source of rules for the future |

A contradiction between two HARVESTs — do not choose silently: both versions into `open-questions.md` and one question to the owner.
