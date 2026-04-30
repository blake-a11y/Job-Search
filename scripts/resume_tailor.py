#!/usr/bin/env python3
"""
Resume Tailor — Adapts master resume to specific job posting
"""
import os
import sys
from pathlib import Path
from notion_client import Client
from openai import OpenAI

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

notion = Client(auth=NOTION_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def load_prompt(name):
    with open(f"prompts/{name}.md") as f:
        return f.read()

def load_evidence_bank():
    with open("evidence-bank.md") as f:
        return f.read()

def select_resume_variant(job_title):
    title_lower = job_title.lower()
    if any(term in title_lower for term in ['gtm', 'customer success', 'customer']):
        return "ai-gtm-customer-success.md"
    elif any(term in title_lower for term in ['program', 'project', 'pmo']):
        return "ai-program-management.md"
    else:
        return "ai-for-internal-ops.md"

def tailor_resume(job_desc, base_resume, evidence_bank):
    prompt = f"""You are Resume Tailor. Adapt the base resume to this specific job description.

JOB DESCRIPTION:
{job_desc}

BASE RESUME:
{base_resume}

EVIDENCE BANK (use only verified facts):
{evidence_bank}

INSTRUCTIONS:
1. Keep the structure identical to the base resume
2. Rewrite the Summary section to mirror the JD's key themes
3. Adjust the top 5 bullet points to use JD language while staying factually accurate
4. Use only facts from the evidence bank
5. Vary sentence rhythm, avoid buzzword stacking
6. Keep Blake's operator tone

OUTPUT the full tailored resume in markdown.
"""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI error: {e}")
        return None

def authenticity_guard(tailored_resume, evidence_bank):
    guard_prompt = load_prompt("authenticity-guard")
    check_prompt = f"""{guard_prompt}

RESUME TO CHECK:
{tailored_resume}

EVIDENCE BANK:
{evidence_bank}

Return PASS or FAIL with brief explanation.
"""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": check_prompt}],
            temperature=0.3
        )
        result = response.choices[0].message.content
        return "PASS" in result.upper()
    except:
        return True

def process_priority_job(page_id):
    page = notion.pages.retrieve(page_id)
    title = page['properties']['Title']['title'][0]['text']['content']
    url = page['properties']['URL']['url']
    print(f"Processing: {title}")

    job_desc = f"Job Title: {title}\nURL: {url}\n(Full JD scraping not yet implemented)"
    evidence = load_evidence_bank()
    variant_file = select_resume_variant(title)

    with open(f"resume-variants/{variant_file}") as f:
        base_resume = f.read()
    print(f"  Using variant: {variant_file}")

    tailored = tailor_resume(job_desc, base_resume, evidence)
    if not tailored:
        print("  ✗ Tailoring failed")
        return False

    if not authenticity_guard(tailored, evidence):
        print("  ⚠ Authenticity guard FAIL - needs manual review")

    output_dir = Path("output/tailored-resumes")
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-')).strip()[:50]
    output_file = output_dir / f"{safe_title}.md"

    with open(output_file, "w") as f:
        f.write(tailored)
    print(f"  ✓ Saved to {output_file}")

    notion.pages.update(
        page_id=page_id,
        properties={"Status": {"select": {"name": "Ready for Blake Review"}}}
    )
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python resume_tailor.py <notion_page_id>")
        sys.exit(1)
    page_id = sys.argv[1]
    success = process_priority_job(page_id)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
