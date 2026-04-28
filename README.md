# Blake's Job Search Operating System — Bot README

> Canonical source of truth. Every bot must read this file first on every invocation. If anything in this README conflicts with another instruction, this README wins.

## 0. Where To Look (Always, In This Order)
1. This README → rules, logic, prompts, schemas.
2. Notion Board → https://www.notion.so/Teamspace-Home-7d575328eef78387a24181e0878c82fa — live job tracker + the 19-section Job Search Operating System page.
3. GitHub Repo → https://github.com/blake-a11y/Job-Search — evidence bank, resumes, prompts, scripts, reports.

## 1. Mission
Land a **remote-first or hybrid, AI-enabled systems/operations role** at **$225k+ total comp** (floor $175k cash; $150k base acceptable only with strong sign-on / equity / performance-paying bonus). Position Blake as a **Systems Intelligence Architect** — turning messy operational data into predictive, AI-driven operating systems.

## 2. Search Criteria v2 (Locked)
See `CONFIG.md` for the live tunable version. High-weight rules:
- Company stage Series A → Enterprise; **no Seed**.
- No roles requiring active security clearance (SECRET is Blake's, but not preferred as a gate).
- Equity-only comp = hard block.
- Preferred specializations: AI observability, AI GTM ops, AI program management, AI product ops, AI-for-internal-ops, AI safety/eval ops, AI customer success engineering.

## 3. Autonomous Loop (How Blake Sees Daily Jobs)
```
07:00 MST daily → job_scout.py (GitHub Action) → Notion DB + reports/YYYY-MM-DD-digest.md + email
↳ for each score ≥85 → resume_tailor.py → attaches resume to Notion row → status = Ready for Blake Review
Blake (~15 min) → opens Notion "🔥 Priority Apply Today" view → clicks Approve & Apply
↳ Notion button → repository_dispatch → logs apply, status = Applied
On Screen Scheduled → interview_prep.py → prep doc attached to row
Monday 08:00 MST → funnel_analyst.py → reports/weekly/YYYY-Www.md + email
```

## 4. Repo Files (read in this order when onboarding a new bot)
1. `README.md` (this file)
2. `CONFIG.md` — tunable thresholds, sources, scoring weights
3. `role-definitions.md` — the full target-role spec
4. `evidence-bank.md` — the only approved claims
5. `master-resume.md` + `resume-variants/*.md`
6. `prompts/*.md` — one prompt per bot
7. `workflows/*.md` — step-by-step runbooks
8. `scripts/*.py` — executable code

## 5. Communication Contract
Every bot output to Blake ends with exactly one line:
> **Next action for Blake:** `<one concrete thing, or "none — waiting on X">`

## 6. Authenticity Guard — Non-Negotiable
- Only pull claims from `evidence-bank.md`.
- Banned phrases: spearheaded, synergy, leveraged cross-functional, drove strategic alignment, thought leader, passionate, world-class, best-in-class, 10x, rockstar, ninja.
- Every claim must be defensible live in an interview.
- Preserve Blake's operator tone: plain, measurement-first, slightly dry.

## 7. Secrets
GitHub Actions secrets only. Never commit. Required:
`NOTION_API_KEY`, `NOTION_DB_ID`, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `SENDGRID_API_KEY`, `LINKEDIN_COOKIE` (or SerpAPI key).
