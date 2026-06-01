"""Pluggable ingestion for manual files and optional official X API access."""

from __future__ import annotations

import json
import os
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import CandidatePost, DEFAULT_SOURCE_LIST_ID, IngestionResult


URL_RE = re.compile(r"https?://[^\s)>\]]+")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ingest_manual(input_path: str, source_list_id: str = DEFAULT_SOURCE_LIST_ID) -> IngestionResult:
    captured_at = utc_now_iso()
    path = Path(input_path)
    raw = path.read_text(encoding="utf-8")
    posts = _load_json_posts(raw, captured_at, source_list_id)
    if posts is None:
        posts = _load_line_posts(raw, captured_at, source_list_id)

    return IngestionResult(
        path="manual",
        source_list_id=source_list_id,
        captured_at=captured_at,
        verification_status="needs_verification",
        posts=posts,
        warnings=[],
    )


def ingest_x_api(source_list_id: str = DEFAULT_SOURCE_LIST_ID, max_results: int = 100) -> IngestionResult:
    captured_at = utc_now_iso()
    token = os.environ.get("X_BEARER_TOKEN") or os.environ.get("TWITTER_BEARER_TOKEN")
    if not token:
        return IngestionResult(
            path="x_api",
            source_list_id=source_list_id,
            captured_at=captured_at,
            verification_status="manual_review_needed",
            posts=[],
            warnings=[
                "X API ingestion was selected, but X_BEARER_TOKEN or TWITTER_BEARER_TOKEN is not set. "
                "No posts were fabricated; rerun with credentials or use manual input."
            ],
        )

    params = urllib.parse.urlencode(
        {
            "max_results": str(min(max_results, 100)),
            "tweet.fields": "created_at,author_id,entities",
            "expansions": "author_id",
            "user.fields": "username",
        }
    )
    url = f"https://api.x.com/2/lists/{source_list_id}/tweets?{params}"
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:  # pragma: no cover - depends on live X API/network.
        return IngestionResult(
            path="x_api",
            source_list_id=source_list_id,
            captured_at=captured_at,
            verification_status="manual_review_needed",
            posts=[],
            warnings=[
                f"X API ingestion failed: {exc}. No posts were fabricated; rerun with credentials or use manual input."
            ],
        )

    users_by_id = {
        user.get("id"): user.get("username", "")
        for user in payload.get("includes", {}).get("users", [])
    }
    posts: list[CandidatePost] = []
    for tweet in payload.get("data", []):
        post_id = str(tweet.get("id", ""))
        author_handle = users_by_id.get(tweet.get("author_id"), "")
        expanded_urls = [
            {"url": url.get("expanded_url") or url.get("url"), "source_kind": "linked"}
            for url in tweet.get("entities", {}).get("urls", [])
            if url.get("expanded_url") or url.get("url")
        ]
        posts.append(
            CandidatePost(
                post_id=post_id,
                post_url=f"https://x.com/{author_handle}/status/{post_id}" if author_handle and post_id else "",
                author_handle=author_handle,
                posted_at=tweet.get("created_at", ""),
                text=tweet.get("text", ""),
                urls=expanded_urls,
                captured_at=captured_at,
                source_list_id=source_list_id,
            )
        )

    return IngestionResult(
        path="x_api",
        source_list_id=source_list_id,
        captured_at=captured_at,
        verification_status="needs_verification",
        posts=posts,
        warnings=[],
    )


def _load_json_posts(raw: str, captured_at: str, default_list_id: str) -> list[CandidatePost] | None:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return None

    source_list_id = str(payload.get("source_list_id") or default_list_id)
    raw_posts = payload.get("posts")
    if not isinstance(raw_posts, list):
        raise ValueError("Manual JSON input must include a top-level posts array.")

    posts: list[CandidatePost] = []
    for index, item in enumerate(raw_posts, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Post {index} must be an object.")
        text = str(item.get("text") or item.get("summary") or "")
        explicit_urls = item.get("urls") or item.get("links") or []
        urls = _normalize_urls(explicit_urls, text)
        post_url = str(item.get("post_url") or _first_x_url(urls) or "")
        posts.append(
            CandidatePost(
                post_id=str(item.get("post_id") or item.get("id") or f"manual-{index:04d}"),
                post_url=post_url,
                author_handle=str(item.get("author_handle") or item.get("author") or ""),
                posted_at=str(item.get("posted_at") or item.get("date") or ""),
                text=text,
                captured_at=captured_at,
                source_list_id=str(item.get("source_list_id") or source_list_id),
                urls=urls,
                project_names=[str(project) for project in item.get("project_names", [])],
                title=item.get("title"),
                metadata={
                    "expected_classification": item.get("classification"),
                    "recommended_action": item.get("recommended_action"),
                    "notes": item.get("notes"),
                },
            )
        )
    return posts


def _load_line_posts(raw: str, captured_at: str, source_list_id: str) -> list[CandidatePost]:
    posts = []
    for index, line in enumerate((line.strip() for line in raw.splitlines()), start=1):
        if not line or line.startswith("#"):
            continue
        urls = _normalize_urls([], line)
        posts.append(
            CandidatePost(
                post_id=f"manual-{index:04d}",
                post_url=_first_x_url(urls),
                author_handle="",
                posted_at="",
                text=line,
                captured_at=captured_at,
                urls=urls,
                source_list_id=source_list_id,
            )
        )
    return posts


def _normalize_urls(explicit_urls: Any, text: str) -> list[dict[str, Any]]:
    urls: list[dict[str, Any]] = []
    if isinstance(explicit_urls, list):
        for value in explicit_urls:
            if isinstance(value, str):
                urls.append({"url": value, "source_kind": _source_kind(value)})
            elif isinstance(value, dict) and value.get("url"):
                copy = dict(value)
                copy.setdefault("source_kind", _source_kind(str(copy["url"])))
                urls.append(copy)

    seen = {item["url"] for item in urls}
    for url in URL_RE.findall(text):
        clean_url = url.rstrip(".,;")
        if clean_url not in seen:
            urls.append({"url": clean_url, "source_kind": _source_kind(clean_url)})
            seen.add(clean_url)
    return urls


def _first_x_url(urls: list[dict[str, Any]]) -> str:
    for url in urls:
        value = str(url.get("url", ""))
        if "x.com/" in value or "twitter.com/" in value:
            return value
    return ""


def _source_kind(url: str) -> str:
    lowered = url.lower()
    if any(host in lowered for host in ("dune.com", "defillama.com", "tokenterminal.com", "artemis.xyz")):
        return "dashboard"
    if "x.com/" in lowered or "twitter.com/" in lowered:
        return "reposted"
    return "primary"
