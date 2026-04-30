# Setup Guide

## Prerequisites

- GitHub repository: `blake-a11y/Job-Search`
- Python 3.11+
- Notion workspace with Job Search Tracker database
- OpenAI API key (GPT-4 access)
- SendGrid account (free tier works)

## Required GitHub Secrets

Go to: Settings > Secrets and variables > Actions > New repository secret

| Secret Name | Where to Get It |
|-------------|----------------|
| `NOTION_API_KEY` | notion.so/my-integrations |
| `NOTION_DB_ID` | Database URL (the long ID after the workspace name) |
| `OPENAI_API_KEY` | platform.openai.com/api-keys |
| `SENDGRID_API_KEY` | app.sendgrid.com/settings/api_keys |
| `BLAKE_EMAIL` | Your email address |

## Notion Database Schema

Your Job Search Tracker Notion DB needs these properties:

| Property | Type | Notes |
|----------|------|-------|
| Title | Title | Job title |
| Company | Rich Text | Company name |
| URL | URL | Job posting URL |
| Source | Select | LinkedIn, Greenhouse, Lever, etc. |
| Location | Rich Text | Location or Remote |
| Match Score | Number | 0-100 |
| Score Breakdown | Rich Text | Scoring details |
| Status | Select | New, Applied, Screen Scheduled, etc. |
| Priority | Checkbox | Auto-set when score >= 85 |
| Posted Date | Date | When job was posted |
| Applied Date | Date | When Blake applied |

## Testing Workflows

### Test daily scout manually:
1. Go to Actions tab in GitHub
2. Click "Daily Job Scout"
3. Click "Run workflow"
4. Watch the logs

### Test weekly analyst:
1. Go to Actions tab
2. Click "Weekly Funnel Analyst"
3. Click "Run workflow"

## Troubleshooting

**Notion auth error:** Check NOTION_API_KEY is correct and the integration has access to your database

**OpenAI error:** Check OPENAI_API_KEY and that you have GPT-4 access

**Empty job results:** LinkedIn scraping requires auth — add your saved search URLs manually to Notion or use the Greenhouse/Lever boards first

**Email not arriving:** Check SendGrid sender verification and spam folder
