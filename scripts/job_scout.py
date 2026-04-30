#!/usr/bin/env python3
"""
Job Scout — Daily job posting scraper, scorer, and Notion writer
"""
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from notion_client import Client
import json

# Load environment
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DB_ID = os.getenv("NOTION_DB_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

notion = Client(auth=NOTION_API_KEY)

def load_sources():
    """Load all source URLs from sources/ directory"""
    sources = {}
    source_dir = Path("sources")
    if source_dir.exists():
        for file in source_dir.glob("*.txt"):
            with open(file) as f:
                sources[file.stem] = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return sources

def fetch_linkedin_jobs(urls):
    """Scrape LinkedIn saved search URLs (placeholder - requires auth)"""
    jobs = []
    # NOTE: LinkedIn requires authentication and has anti-scraping measures
    # Production implementation should use LinkedIn API or authenticated session
    print(f"  [LinkedIn] Skipping {len(urls)} URLs (requires auth)")
    return jobs

def fetch_greenhouse_jobs(boards):
    """Scrape Greenhouse job boards"""
    jobs = []
    for board_url in boards:
        try:
            resp = requests.get(f"{board_url}/embed/jobs", timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            for job_div in soup.select('.opening'):
                title = job_div.select_one('a').text.strip()
                job_url = job_div.select_one('a')['href']
                location = job_div.select_one('.location').text.strip() if job_div.select_one('.location') else ''
                jobs.append({
                    'title': title,
                    'company': board_url.split('//')[1].split('.')[0].title(),
                    'url': job_url,
                    'location': location,
                    'source': 'Greenhouse',
                    'posted_date': datetime.now(timezone.utc).isoformat()
                })
        except Exception as e:
            print(f"  [Greenhouse] Error on {board_url}: {e}")
    return jobs

def fetch_lever_jobs(boards):
    """Scrape Lever job boards"""
    jobs = []
    for board_url in boards:
        try:
            resp = requests.get(board_url, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            for posting in soup.select('.posting'):
                title = posting.select_one('h5').text.strip()
                job_url = posting.select_one('a')['href']
                location = posting.select_one('.location').text.strip() if posting.select_one('.location') else ''
                jobs.append({
                    'title': title,
                    'company': board_url.split('//')[1].split('.')[0].title(),
                    'url': job_url,
                    'location': location,
                    'source': 'Lever',
                    'posted_date': datetime.now(timezone.utc).isoformat()
                })
        except Exception as e:
            print(f"  [Lever] Error on {board_url}: {e}")
    return jobs

def apply_hard_filters(job):
    """Return True if job should be rejected"""
    title_lower = job['title'].lower()
    if any(word in title_lower for word in ['clearance required', 'ts/sci', 'polygraph']):
        return True
    if 'seed' in job.get('company', '').lower():
        return True
    return False

def score_job(job):
    """Score job 0-100 using CONFIG.md rubric"""
    score = 0
    breakdown = []
    title = job['title'].lower()
    location = job.get('location', '').lower()

    if 'remote' in location or 'phoenix' in location or 'hybrid' in location:
        score += 15
        breakdown.append("Remote/Hybrid: +15")

    if any(term in title for term in ['ai', 'ml', 'machine learning', 'llm', 'artificial intelligence']):
        score += 15
        breakdown.append("AI role: +15")

    if any(term in title for term in ['operations', 'systems', 'platform', 'infrastructure', 'mlops']):
        score += 15
        breakdown.append("Systems/Ops focus: +15")

    if any(term in title for term in ['observability', 'gtm', 'program', 'product ops', 'customer success']):
        score += 10
        breakdown.append("Specialization match: +10")

    score += 10
    breakdown.append("Est comp: +10 (needs JD parse)")
    score += 5
    breakdown.append("Company quality: +5 (default)")

    return score, breakdown

def get_notion_existing():
    """Fetch existing job URLs from Notion to dedupe"""
    try:
        results = notion.databases.query(database_id=NOTION_DB_ID)
        existing_urls = set()
        for page in results.get('results', []):
            url_prop = page['properties'].get('URL', {})
            if url_prop.get('url'):
                existing_urls.add(url_prop['url'])
        return existing_urls
    except Exception as e:
        print(f"Error fetching Notion DB: {e}")
        sys.exit(1)

def write_to_notion(job, score, breakdown):
    """Write job posting to Notion DB"""
    try:
        notion.pages.create(
            parent={"database_id": NOTION_DB_ID},
            properties={
                "Title": {"title": [{"text": {"content": job['title']}}]},
                "Company": {"rich_text": [{"text": {"content": job['company']}}]},
                "URL": {"url": job['url']},
                "Source": {"select": {"name": job['source']}},
                "Location": {"rich_text": [{"text": {"content": job.get('location', '')}}]},
                "Match Score": {"number": score},
                "Score Breakdown": {"rich_text": [{"text": {"content": '; '.join(breakdown)}}]},
                "Status": {"select": {"name": "New"}},
                "Priority": {"checkbox": score >= 85},
                "Posted Date": {"date": {"start": job['posted_date']}}
            }
        )
        return True
    except Exception as e:
        print(f"  Error writing to Notion: {e}")
        return False

def generate_digest(new_jobs, priority_count):
    """Generate daily digest markdown"""
    today = datetime.now().strftime("%Y-%m-%d")
    digest = f"""# Daily Job Scout Digest — {today}

**Summary:** Surfaced {len(new_jobs)} new postings, {priority_count} Priority (≥85 score)

## Top 10 Roles

| Score | Title | Company | Location | URL |
|-------|-------|---------|----------|-----|
"""
    sorted_jobs = sorted(new_jobs, key=lambda x: x['score'], reverse=True)[:10]
    for job in sorted_jobs:
        digest += f"| {job['score']} | {job['title']} | {job['company']} | {job['location'][:30]} | [Apply]({job['url']}) |\n"

    digest += f"""

---
**Next action for Blake:** Review {priority_count} Priority rows in Notion "🔥 Priority Apply Today" view.
"""
    Path("reports").mkdir(exist_ok=True)
    with open(f"reports/{today}-digest.md", "w") as f:
        f.write(digest)
    return digest

def main():
    print("🔍 Job Scout starting...")
    sources = load_sources()
    print(f"✓ Loaded {sum(len(v) for v in sources.values())} source URLs")

    existing_urls = get_notion_existing()
    print(f"✓ Found {len(existing_urls)} existing jobs in Notion")

    all_jobs = []
    all_jobs.extend(fetch_greenhouse_jobs(sources.get('greenhouse_boards', [])))
    all_jobs.extend(fetch_lever_jobs(sources.get('lever_boards', [])))
    all_jobs.extend(fetch_linkedin_jobs(sources.get('linkedin_urls', [])))
    print(f"✓ Scraped {len(all_jobs)} total postings")

    new_jobs = []
    priority_count = 0

    for job in all_jobs:
        if apply_hard_filters(job):
            continue
        if job['url'] in existing_urls:
            continue
        score, breakdown = score_job(job)
        if score >= 65:
            job['score'] = score
            job['breakdown'] = breakdown
            new_jobs.append(job)
            if write_to_notion(job, score, breakdown):
                if score >= 85:
                    priority_count += 1

    print(f"✓ Wrote {len(new_jobs)} new jobs to Notion ({priority_count} Priority)")
    generate_digest(new_jobs, priority_count)
    print(f"✓ Digest saved to reports/{datetime.now().strftime('%Y-%m-%d')}-digest.md")
    print("✅ Job Scout complete")

if __name__ == "__main__":
    main()
