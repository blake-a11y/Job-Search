#!/usr/bin/env python3
"""
Apply Logger — Updates Notion when Blake clicks Approve & Apply
"""
import os
from datetime import datetime, timezone
from notion_client import Client
from pathlib import Path

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")

notion = Client(auth=NOTION_API_KEY)

def log_application():
    page = notion.pages.retrieve(NOTION_PAGE_ID)
    title = page['properties']['Title']['title'][0]['text']['content']
    company = page['properties']['Company']['rich_text'][0]['text']['content']

    notion.pages.update(
        page_id=NOTION_PAGE_ID,
        properties={
            "Status": {"select": {"name": "Applied"}},
            "Applied Date": {"date": {"start": datetime.now(timezone.utc).isoformat()}}
        }
    )

    log_entry = f"- [{datetime.now().strftime('%Y-%m-%d')}] {title} at {company}\n"
    Path("reports").mkdir(exist_ok=True)
    with open("reports/applications.md", "a") as f:
        f.write(log_entry)

    print(f"✓ Logged application: {title} at {company}")

if __name__ == "__main__":
    log_application()
