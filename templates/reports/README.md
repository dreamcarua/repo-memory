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
