# Daily Runbook

## 07:00 MST — Automated (GitHub Action `daily-scout.yml`)

1. Run `scripts/job_scout.py`
   - Pulls new postings from all sources in CONFIG.md
   - Applies hard filters, dedupes against Notion DB
   - Scores each posting 0–100, writes rows to Notion
   - Flags ≥85 as Priority=True
2. For each Priority row, dispatch `scripts/resume_tailor.py`
   - Selects best resume variant
   - Tailors Summary + top 5 bullets to JD language
   - Runs Authenticity Guard — rewrites if FAIL
   - Saves 4 artifacts to Google Drive, links to Notion row
   - Sets Status=Ready for Blake Review
3. Commit `reports/YYYY-MM-DD-digest.md` with top 10 ranked postings
4. Send email digest via SendGrid
   - Subject: `[Job Scout] YYYY-MM-DD — N Priority roles ready`
   - Body: top 10 table + direct link to Notion Priority view

## Blake's Daily Action (~15 min, any time)

1. Open Notion **"🔥 Priority Apply Today"** view
2. Per row:
   - Open tailored resume link (Google Drive)
   - Skim for accuracy — edit if needed
   - Click **Approve & Apply** button in Notion
3. Notion button fires `repository_dispatch` event `apply-clicked`
   - GitHub Action `on-apply.yml` triggers
   - Updates Notion row: Status=Applied, Applied Date=today
   - Logs to `reports/applications.md`
4. Submit application externally (ATS, LinkedIn Easy Apply, or email)
   - Paste tailored resume from Google Drive
   - Paste cover note
5. Mark Notion row Status=Submitted

## Status=Screen Scheduled? (any time)

- Move Notion row to Status=Screen Scheduled
- GitHub Action auto-triggers `scripts/interview_prep.py`
- Prep doc attached to Notion row within ~5 minutes
- Block 30 min in calendar for rehearsal before the call

## End-of-Day (Optional, <5 min)

- Scan Notion for any Response or Rejection rows that arrived
- Update Status accordingly — funnel data compounds over time
- Note any compensation intel in the row's Notes field (never in resume artifacts)
