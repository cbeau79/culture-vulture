#!/usr/bin/env python3
"""Send the most recent Culture Digest email as HTML.

Credentials come from the environment — never hard-code them, never commit them:

    export DIGEST_SMTP_USER="you@gmail.com"
    export DIGEST_SMTP_PASS="your-16-char-app-password"   # Gmail App Password
    export DIGEST_TO="chris.beaumont@gmail.com"

Gmail requires an App Password (not your account password) with 2FA enabled:
https://myaccount.google.com/apppasswords

Usage:
    python3 send-digest.py                 # send the newest file in emails/
    python3 send-digest.py --dry-run       # print what would be sent, send nothing
    python3 send-digest.py --file emails/2026-07-10-culture-digest.md
"""

import argparse
import os
import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465  # implicit TLS
VAULT = Path(__file__).resolve().parent.parent
EMAILS_DIR = VAULT / "emails"


def latest_digest() -> Path:
    files = sorted(EMAILS_DIR.glob("*-culture-digest.md"))
    if not files:
        sys.exit(f"No digest files found in {EMAILS_DIR}")
    return files[-1]


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].lstrip("\n")
    return text


def subject_from(path: Path, body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return f"Culture Digest — {path.stem[:10]}"


def to_html(markdown: str) -> str:
    """Render markdown if the `markdown` package is present; else send plain text."""
    try:
        import markdown as md
    except ImportError:
        return None
    return md.markdown(markdown, extensions=["extra"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", help="digest file to send (default: newest)")
    ap.add_argument("--dry-run", action="store_true", help="print, don't send")
    args = ap.parse_args()

    path = Path(args.file).expanduser() if args.file else latest_digest()
    if not path.is_absolute():
        path = VAULT / path
    if not path.exists():
        sys.exit(f"Not found: {path}")

    raw = path.read_text(encoding="utf-8")
    body = strip_frontmatter(raw)
    subject = subject_from(path, body)

    user = os.environ.get("DIGEST_SMTP_USER")
    password = os.environ.get("DIGEST_SMTP_PASS")
    recipient = os.environ.get("DIGEST_TO", user)

    if args.dry_run:
        print(f"file:    {path}")
        print(f"to:      {recipient or '<DIGEST_TO unset>'}")
        print(f"subject: {subject}")
        print(f"from:    {user or '<DIGEST_SMTP_USER unset>'}")
        print(f"pass:    {'set' if password else '<DIGEST_SMTP_PASS unset>'}")
        print("-" * 60)
        print(body)
        return

    missing = [
        name
        for name, val in (
            ("DIGEST_SMTP_USER", user),
            ("DIGEST_SMTP_PASS", password),
            ("DIGEST_TO", recipient),
        )
        if not val
    ]
    if missing:
        sys.exit(f"Missing environment variables: {', '.join(missing)}")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = recipient
    msg.set_content(body)

    html = to_html(body)
    if html:
        msg.add_alternative(
            f"<html><body style='max-width:42em;font-family:-apple-system,"
            f"Segoe UI,sans-serif;line-height:1.5'>{html}</body></html>",
            subtype="html",
        )

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=30) as smtp:
        smtp.login(user, password)
        smtp.send_message(msg)

    print(f"Sent {path.name} to {recipient}")


if __name__ == "__main__":
    main()
