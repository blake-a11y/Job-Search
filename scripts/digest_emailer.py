#!/usr/bin/env python3
"""
Digest Emailer — Send daily/weekly reports via SendGrid
"""
import os
import sys
from pathlib import Path
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
BLAKE_EMAIL = os.getenv("BLAKE_EMAIL")
FROM_EMAIL = os.getenv("FROM_EMAIL", "bot@blake-a11y.com")

def send_email(subject, body):
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=BLAKE_EMAIL,
        subject=subject,
        html_content=body
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"✓ Email sent: {response.status_code}")
        return True
    except Exception as e:
        print(f"✗ Email failed: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python digest_emailer.py <report_file.md>")
        sys.exit(1)

    report_file = Path(sys.argv[1])
    if not report_file.exists():
        print(f"Report not found: {report_file}")
        sys.exit(1)

    with open(report_file) as f:
        content = f.read()

    html_content = content.replace("\n", "<br>")
    html_content = f"<pre style='font-family: monospace;'>{html_content}</pre>"
    subject = f"[Job Search] {report_file.stem}"
    send_email(subject, html_content)

if __name__ == "__main__":
    main()
