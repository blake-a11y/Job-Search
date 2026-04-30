#!/usr/bin/env python3
"""
Interview Prep — Generate prep doc when screen is scheduled
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

def load_evidence_bank():
    with open("evidence-bank.md") as f:
        return f.read()

def generate_prep_doc(job_title, job_desc, evidence):
    prompt = f"""You are Interview Prep Bot. Create a focused interview prep doc.

JOB: {job_title}

JOB DESCRIPTION:
{job_desc}

EVIDENCE BANK (Blake's verified stories):
{evidence}

GENERATE:
1. Top 5 likely questions based on this JD
2. For each question, suggest which story from evidence bank to use
3. Draft 2-3 sentence answer framework (NOT full script)
4. Flag any knowledge gaps Blake should research

Keep it concise - one page max.
"""
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

def main():
    if len(sys.argv) < 2:
        print("Usage: python interview_prep.py <notion_page_id>")
        sys.exit(1)

    page_id = sys.argv[1]
    page = notion.pages.retrieve(page_id)
    title = page['properties']['Title']['title'][0]['text']['content']
    url = page['properties']['URL']['url']
    print(f"Generating prep for: {title}")

    job_desc = f"Title: {title}\nURL: {url}"
    evidence = load_evidence_bank()
    prep_doc = generate_prep_doc(title, job_desc, evidence)

    output_dir = Path("output/interview-prep")
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-')).strip()[:50]
    output_file = output_dir / f"{safe_title}-prep.md"

    with open(output_file, "w") as f:
        f.write(prep_doc)
    print(f"✓ Prep doc saved to {output_file}")

if __name__ == "__main__":
    main()
