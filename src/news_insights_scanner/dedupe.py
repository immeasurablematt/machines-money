"""Duplicate-story grouping."""

from __future__ import annotations

import re
from urllib.parse import urlparse


STOPWORDS = {"the", "and", "for", "with", "from", "that", "this", "into", "over", "after", "about"}


def dedupe_items(items: list[dict]) -> list[dict]:
    grouped: dict[str, dict] = {}
    for item in items:
        key = _dedupe_key(item)
        if key not in grouped:
            item["duplicate_count"] = 1
            grouped[key] = item
            continue
        existing = grouped[key]
        existing["duplicate_count"] += 1
        existing["evidence_urls"] = _merge(existing.get("evidence_urls", []), item.get("evidence_urls", []))
        existing["notes"] = _append_note(existing.get("notes", ""), f"Duplicate source grouped: {item.get('post_url') or item.get('post_id')}")
        if item.get("priority") == "High":
            existing["priority"] = "High"
    return list(grouped.values())


def _dedupe_key(item: dict) -> str:
    primary_urls = [url for url in item.get("evidence_urls", []) if "x.com/" not in url and "twitter.com/" not in url]
    if primary_urls:
        parsed = urlparse(primary_urls[0])
        return f"url:{parsed.netloc.lower()}{parsed.path.rstrip('/')}"
    projects = "-".join(item.get("project_names", []))
    words = [
        word
        for word in re.findall(r"[a-z0-9]+", item.get("summary", "").lower())
        if word not in STOPWORDS and len(word) > 2
    ]
    return f"text:{projects}:{'-'.join(words[:8])}"


def _merge(first: list[str], second: list[str]) -> list[str]:
    merged = list(first)
    for value in second:
        if value not in merged:
            merged.append(value)
    return merged


def _append_note(existing: str, note: str) -> str:
    if not existing:
        return note
    return f"{existing}; {note}"
