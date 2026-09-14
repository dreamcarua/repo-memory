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

Write the file as **plain UTF-8 JSON — the literal text above, starting with `{`**. Whatever commits it
does its own encoding; encoding is never a step you perform. This matters because a model cannot compute
base64: every ASCII run survives, so numbers and Latin words come back looking right, while everything
else is silently corrupted — and base64 of a corrupted string is still valid base64, so nothing downstream
can catch it. If the content you are about to commit starts with `eyJ`, or is one unbroken run of letters
and digits ending in `=`, it is already destroyed; write the JSON again as text.

A report that does not parse is skipped, named in the run log and announced on the channel. It never stops
the other reports in the same push, and it is never deleted — the file stays in `reports/` so it can be
read and re-committed.

Send when a task changed project state. Do not send for questions, reading, estimates.
