"""Scoring and priority derivation."""

from __future__ import annotations

from datetime import datetime, timezone

from .extract_links import infer_source_kind
from .models import CandidatePost


CORE_TOPICS = (
    "defi",
    "tokenized",
    "rwa",
    "real-world asset",
    "asset management",
    "yield",
    "derivatives",
    "ai",
    "financial infrastructure",
    "stablecoin",
    "protocol",
    "onchain",
)


def score_item(post: CandidatePost, classification: str, evidence_urls: list[str], metrics: list[dict[str, str]]) -> dict[str, int]:
    text = f"{post.title or ''} {post.text}".lower()
    relevance = 5 if any(topic in text for topic in CORE_TOPICS) else 3
    timeliness = _timeliness(post.posted_at)
    evidence_quality = _evidence_quality(evidence_urls)
    editorial_value = _editorial_value(classification, metrics, evidence_quality)
    if classification == "Skip":
        relevance = min(relevance, 2)
        editorial_value = min(editorial_value, 2)
    return {
        "relevance": relevance,
        "timeliness": timeliness,
        "evidence_quality": evidence_quality,
        "editorial_value": editorial_value,
    }


def priority(scores: dict[str, int]) -> str:
    average = sum(scores.values()) / len(scores)
    if average >= 4.0 and scores["evidence_quality"] >= 3:
        return "High"
    if average >= 3.0:
        return "Medium"
    return "Low"


def _timeliness(posted_at: str) -> int:
    if not posted_at:
        return 3
    try:
        parsed = datetime.fromisoformat(posted_at.replace("Z", "+00:00"))
    except ValueError:
        return 3
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    age_hours = (datetime.now(timezone.utc) - parsed.astimezone(timezone.utc)).total_seconds() / 3600
    if age_hours <= 48:
        return 5
    if age_hours <= 168:
        return 4
    if age_hours <= 720:
        return 3
    return 2


def _evidence_quality(evidence_urls: list[str]) -> int:
    if not evidence_urls:
        return 2
    kinds = {infer_source_kind(url) for url in evidence_urls}
    if "primary" in kinds or "dashboard" in kinds:
        return 5
    if "reposted" in kinds:
        return 3
    return 2


def _editorial_value(classification: str, metrics: list[dict[str, str]], evidence_quality: int) -> int:
    if classification == "Adoption Stat" and metrics:
        return 5
    if classification in {"Announcement", "Deep Dive/Article"} and evidence_quality >= 4:
        return 4
    if classification == "Skip":
        return 1
    return 3
