#!/usr/bin/env python3
"""
Notion Writer — Standalone utility for writing job rows to Notion
"""
import os
import json
import sys
from notion_client import Client

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DB_ID = os.getenv("NOTION_DB_ID")

notion = Client(auth=NOTION_API_KEY)

def write_job(job_data):
    try:
        notion.pages.create(
            parent={"database_id": NOTION_DB_ID},
            properties={
                "Title": {"title": [{"text": {"content": job_data['title']}}]},
                "Company": {"rich_text": [{"text": {"content": job_data['company']}}]},
                "URL": {"url": job_data['url']},
                "Source": {"select": {"name": job_data['source']}},
                "Location": {"rich_text": [{"text": {"content": job_data.get('location', '')}}]},
                "Match Score": {"number": job_data['score']},
                "Score Breakdown": {"rich_text": [{"text": {"content": job_data['breakdown']}}]},
                "Status": {"select": {"name": "New"}},
                "Priority": {"checkbox": job_data['score'] >= 85}
            }
        )
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: echo '{...}' | python notion_writer.py")
        sys.exit(1)
    if sys.argv[1].endswith('.json'):
        with open(sys.argv[1]) as f:
            job_data = json.load(f)
    else:
        job_data = json.loads(sys.stdin.read())
    success = write_job(job_data)
    sys.exit(0 if success else 1)
