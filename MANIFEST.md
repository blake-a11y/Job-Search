# Job Search Repository — File Manifest

## Directory Structure

```
Job-Search/
├── .github/
│   └── workflows/
│       ├── daily-scout.yml          # Runs daily 07:00 MST
│       ├── weekly-analyst.yml       # Runs Monday 08:00 MST
│       └── on-apply.yml             # Fires when Blake clicks Apply
├── scripts/
│   ├── job_scout.py             # Scraper, scorer, Notion writer
│   ├── resume_tailor.py         # Adapts resume to each JD
│   ├── interview_prep.py        # Generates prep doc
│   ├── funnel_analyst.py        # Weekly metrics
│   ├── apply_logger.py          # Logs applications
│   ├── digest_emailer.py        # Sends email reports
│   └── notion_writer.py         # Standalone Notion utility
├── sources/
│   ├── linkedin_urls.txt        # LinkedIn saved search URLs
│   ├── greenhouse_boards.txt    # Greenhouse company boards
│   ├── lever_boards.txt         # Lever company boards
│   ├── wellfound_filters.txt    # Wellfound filters
│   └── company_pages.txt        # Direct career pages
├── workflows/
│   └── weekly.md                # Weekly runbook
├── reports/                     # Auto-populated by scripts
├── prompts/                     # Bot prompts (6 files)
├── resume-variants/             # 3 resume variants
├── .env.example
├── .gitignore
├── SETUP.md
├── requirements.txt
├── README.md
├── CONFIG.md
├── evidence-bank.md
├── master-resume.md
└── role-definitions.md
```

## What Does What

| Script | When | What |
|--------|------|------|
| `job_scout.py` | Daily 07:00 MST | Scrapes boards, scores, writes to Notion |
| `resume_tailor.py` | Triggered by Blake | Adapts resume to specific JD |
| `interview_prep.py` | Triggered by Blake | Generates interview prep doc |
| `funnel_analyst.py` | Monday 08:00 MST | Weekly conversion metrics |
| `apply_logger.py` | On apply click | Logs application to Notion + reports/ |
| `digest_emailer.py` | Called by other scripts | Sends email digests |

## To Get Started

1. Add GitHub Secrets (see SETUP.md)
2. Add job board URLs to sources/
3. Run Daily Job Scout manually from Actions tab to test
