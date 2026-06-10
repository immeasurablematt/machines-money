"""Send a scanner digest to the Google Doc webhook.

Reads ``digest.md``, sanity-checks the sibling ``digest.json`` for a healthy
run, and POSTs the markdown to the Apps Script web app that creates a Google
Doc in Drive (see ``scripts/apps_script/digest_webhook.gs``).

Environment variables:

- ``DIGEST_WEBHOOK_URL``: the Apps Script web app URL.
- ``DIGEST_WEBHOOK_TOKEN``: shared token matching the script's SHARED_TOKEN.

Usage:

    python3 scripts/deliver_digest.py outputs/news-insights-scanner/2026-06-09/digest.md
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

RETRY_DELAYS_SECONDS = (2, 4, 8, 16)


def main() -> int:
    parser = argparse.ArgumentParser(description="Deliver a scanner digest to the Google Doc webhook.")
    parser.add_argument("digest_md", help="Path to the digest.md produced by the scanner.")
    parser.add_argument("--title", help="Optional Google Doc title. Defaults to a dated digest title.")
    parser.add_argument(
        "--allow-setup-warnings",
        action="store_true",
        help="Deliver even when the run is flagged manual_review_needed (normally a setup failure).",
    )
    args = parser.parse_args()

    digest_path = Path(args.digest_md)
    if not digest_path.is_file():
        print(f"ERROR: digest file not found: {digest_path}", file=sys.stderr)
        return 1
    markdown = digest_path.read_text(encoding="utf-8")

    json_path = digest_path.with_name("digest.json")
    if json_path.is_file() and not args.allow_setup_warnings:
        run_data = json.loads(json_path.read_text(encoding="utf-8"))
        if run_data.get("verification_status") == "manual_review_needed":
            warnings = run_data.get("warnings") or []
            print(
                "ERROR: the scanner run needs setup attention, so the digest was not sent.\n"
                "This usually means the X API token is missing or invalid.\n"
                "Run warnings: " + ("; ".join(warnings) if warnings else "none recorded"),
                file=sys.stderr,
            )
            return 1

    webhook_url = os.environ.get("DIGEST_WEBHOOK_URL", "").strip()
    token = os.environ.get("DIGEST_WEBHOOK_TOKEN", "").strip()
    if not webhook_url or not token:
        print(
            "ERROR: DIGEST_WEBHOOK_URL and DIGEST_WEBHOOK_TOKEN must both be set.",
            file=sys.stderr,
        )
        return 1

    title = args.title or f"Machines & Money News Digest {date.today().isoformat()}"
    body = json.dumps({"token": token, "title": title, "markdown": markdown}).encode("utf-8")

    response_text = _post_with_retries(webhook_url, body)
    if response_text is None:
        return 1

    try:
        response = json.loads(response_text)
    except json.JSONDecodeError:
        print(f"ERROR: webhook returned a non-JSON response: {response_text[:500]}", file=sys.stderr)
        return 1
    if not response.get("ok"):
        print(f"ERROR: webhook rejected the digest: {response.get('error', 'unknown error')}", file=sys.stderr)
        return 1

    print(f"Digest delivered: {response.get('doc_url', '(no doc URL returned)')}")
    return 0


def _post_with_retries(url: str, body: bytes) -> str | None:
    last_error = ""
    for attempt, delay in enumerate((0,) + RETRY_DELAYS_SECONDS):
        if delay:
            time.sleep(delay)
        request = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            # Apps Script web apps answer POSTs with a redirect to the real
            # response URL; urllib follows it automatically.
            with urllib.request.urlopen(request, timeout=60) as raw:
                return raw.read().decode("utf-8")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = str(exc)
            print(f"Webhook attempt {attempt + 1} failed: {last_error}", file=sys.stderr)
    print(f"ERROR: could not reach the digest webhook after retries: {last_error}", file=sys.stderr)
    return None


if __name__ == "__main__":
    raise SystemExit(main())
