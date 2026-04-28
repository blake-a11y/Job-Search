# Blake's Job Search Operating System — Bot README

> **Canonical source of truth.** Every bot (Job Scout, Resume Tailor, Interview Prep, Career Counselor, Funnel Analyst, Authenticity Guard) must read this file FIRST on every invocation before taking any action. If anything in this README conflicts with another instruction, this README wins.

---

## 0. Where To Look (Always, In This Order)

1. **This README** — `https://github.com/blake-a11y/Job-Search/blob/main/README.md` — rules, logic, prompts, schemas.
2. **Notion Board** — `https://www.notion.so/Teamspace-Home-7d575328eef78387a24181e0878c82fa` — live state, the Job Search Tracker database, and the 12-section Job Search Operating System page.
3. **GitHub Repo** — `https://github.com/blake-a11y/Job-Search` — evidence bank, resume variants, prompts, workflow scripts.

Any bot that cannot reach all three must halt and notify Blake.

---

## 1. Mission

Land a **remote-first, AI-enabled systems/operations leadership role** at **$225k+ total comp** (minimum $175k cash; $150k base acceptable only with significant sign-on, equity, or profit sharing). Position Blake as a **Systems Intelligence Architect** — the operator who turns messy operational data into predictive, AI-driven operating systems. Non-defense preferred.

---

## 2. Search Criteria (Locked v1 — do not change without Blake's approval)

| Category | Target |
|---|---|
| Role theme | AI-enabled systems, operations architecture, platform execution, performance measurement |
| Titles | Director of AI Operations; Head of AI Platform Operations; AI Strategy & Operations; AI Program Director; Director of Intelligent Systems; AI Transformation Lead; MLOps Program Director; AI Infrastructure Operations; Chief of Staff (AI/CEO); Product Ops for AI Platform |
| Industry | Non-defense. AI-native or AI-forward. Startup through mid-market. |
| Work setup | Remote-first strongly preferred. Hybrid Phoenix acceptable case-by-case. |
| Comp floor | $175k cash minimum |
| Comp target | $225k+ total comp |
| Comp flex | $150k base acceptable with strong sign-on, equity, or profit sharing |
| Clearance | SECRET (active, refreshing) — include only when it differentiates |
| Leadership fit | Open to people-management OR IC-strategic |

---

## 3. Daily Workflow (Job Scout Bot — runs 7 AM MST)

1. Pull new postings from LinkedIn Jobs, Greenhouse, Lever, Wellfound, remote aggregators, and target company career pages.
2. Dedupe by URL, company, and title.
3. Score each posting 0-100 using the rubric in §7.
4. Push top 5-10 scored postings to the **Job Search Tracker** Notion database with `Status = New`.
5. Generate morning digest: Title, Company, Match Score, Comp estimate, Apply Link, Why-it-fits (one sentence).
6. Flag any posting scoring **85+** as `Priority Apply Today`.
7. For each Priority, auto-invoke **Resume Tailor Bot** to produce a tailored resume + short cover note.
8. Notify Blake with the digest and one clear next action: "Blake, your next action is X."

---

## 4. Weekly Workflow (Funnel Analyst Bot — Mondays)

1. Compute funnel conversion at each stage (Surfaced → Applied → Response → Screen → Loop → Final → Offer).
2. Identify which sources produced interviews vs. dead ends. Rebalance sourcing weights.
3. Refresh search keywords based on recurring titles.
4. Update 2-3 resume variants if market language has shifted.
5. Run Career Counselor Bot on missed-fit roles to surface skill gaps.
6. Produce a Monday report that tells Blake the single most important thing to do that week.

---

## 5. Volume Strategy (Tiered Personalization)

| Tier | Fit Score | Action |
|---|---|---|
| High | 85-100 | Full tailor (title, summary, top bullets, skills). Send same day. |
| Medium | 65-84 | Role-family variant with light edits. Send within 48 hrs. |
| Low | < 65 | Skip unless comp and company quality are exceptional. |

---

## 6. Progress Metrics (tracked weekly)

Jobs surfaced · Jobs worth applying to · Applications sent · Response rate · Interview rate · Final-round rate · Offer rate · Median comp of viable roles.

---

## 7. Scoring Rubric (0-100)

- Remote-first (0-20)
- Comp likely ≥ $225k total (0-20)
- AI required in the role (0-15)
- Systems / performance measurement / ops architecture focus (0-15)
- Non-defense (0-10)
- Level fit — Director/Head/VP tier (0-10)
- Company quality (funded, traction, AI-native) (0-10)

---

## 8. Bot Stack & Triggers

| Bot | Purpose | Trigger |
|---|---|---|
| Job Scout | Search, dedupe, score, rank | Daily 7 AM MST |
| Resume Tailor | Adapt master resume to posting | On-demand per Priority |
| Interview Prep | Questions, story matches, mock answers | Status = Screen Scheduled |
| Career Counselor | Market gaps + short/long-term skill moves | Weekly |
| Funnel Analyst | Conversion tracking, process recommendations | Weekly Monday |
| Authenticity Guard | Prevent AI-written feel | Runs inside Resume Tailor |

---

## 9. Authenticity Guard (Anti-AI-Feel Logic)

- Pull ONLY from `/evidence-bank.md` — never fabricate.
- Prefer concrete numbers (17% labor savings, $23M saved, 45% redundancy cut) over leadership adjectives.
- Vary sentence rhythm; avoid template parallelism.
- Ban buzzword stacks: "spearheaded," "synergy," "leveraged cross-functional," "drove strategic alignment."
- Every claim must be defensible live in an interview.
- Preserve Blake's operator voice: plain, measurement-first, slightly dry.
- Self-check pass: after drafting, re-read and cut any sentence that sounds like a LinkedIn bio.

---

## 10. Resume Tailor Bot — Core Logic

Input: job description + `/master-resume.md` + `/evidence-bank.md`.

1. Parse JD for title, required tools, success metrics, domain language.
2. Match against evidence bank.
3. Select 8-12 strongest proof points.
4. Rewrite using ONLY grounded claims, run through Authenticity Guard.
5. Output: tailored resume (PDF-ready), short cover note, 30-sec pitch, 5 likely interview questions + talking points.

---

## 11. Career Counselor Bot — Recommendations

**Short-term (low-hanging):**
- Publish 2-3 LinkedIn case studies: Amazon tote replenishment, Sendoso Central Flow, Lynx AI automation.
- Complete one applied AI/ML systems or cloud AI architecture certification.
- Ship one public ops-intelligence demo built with Claude Code or Codex.

**Longer-term:**
- Deeper fluency in data systems and cloud/AI platform concepts.
- Formal credential ONLY if target roles repeatedly require it — generally lower ROI than proof-of-work.

---

## 12. Execution Order (where we are right now)

1. ✅ Lock final search criteria and role-title list.
2. ⏳ Build master evidence bank from Blake's real stories.
3. ⏳ Rewrite master resume around AI-enabled systems leadership.
4. ⏳ Create 3 role-family resume variants.
5. ⏳ Stand up daily surfacing + scoring workflow.
6. ⏳ Build Resume Tailor and Career Counselor bots.

---

## 13. Open Inputs Needed From Blake

Any bot that encounters an ambiguity in these areas must stop and ask Blake directly:

- Latest LinkedIn headline and About text
- Startup vs. mid-market vs. both
- Hybrid Phoenix acceptable or remote only
- People-management-heavy vs. IC-strategic vs. both
- Approval to draft exact bot prompts and workflow spec

---

## 14. Communication Contract

Every bot response to Blake ends with a single line:

> **Next action for Blake:** `<one concrete thing>`

No exceptions. If there is no next action, say so explicitly: `Next action for Blake: none — waiting on X.`

---

## 15. Repo Structure (target)
