"""Selection layer that turns a broad feed scan into a short review queue."""

from __future__ import annotations

from collections import Counter
from datetime import datetime


STRONG_ANNOUNCEMENT_TERMS = (
    "announced",
    "launch",
    "launched",
    "go live",
    "is live",
    "partnership",
    "partnered",
    "integration",
    "integrated",
    "raised",
    "funding",
    "mainnet",
    "acquired",
)

DEEP_DIVE_TERMS = (
    "report",
    "research",
    "deep dive",
    "analysis",
    "thesis",
    "explainer",
    "case study",
    "breaks down",
)

PROMO_TERMS = (
    "podcast",
    "episode",
    "joined",
    "speaking",
    "taking the stage",
    "agenda",
    "hackathon",
    "spaces",
    "webinar",
    "mentor clinic",
)

LOW_SIGNAL_TERMS = (
    "gm",
    "vibes",
    "crazy work",
    "keep cooking",
    "we're cooked",
    "meme",
)


def triage_items(items: list[dict], top_n: int) -> tuple[list[dict], dict]:
    scored: list[dict] = []
    drop_reasons: Counter[str] = Counter()

    for item in items:
        score, reasons, drop_reason = _selection_score(item)
        if drop_reason:
            drop_reasons[drop_reason] += 1
            continue
        copy = dict(item)
        copy["selection_score"] = score
        copy["selection_reasons"] = reasons
        scored.append(copy)

    scored.sort(key=lambda item: (item["selection_score"], _posted_sort_key(item)), reverse=True)
    selected = scored[: max(0, top_n)]
    selected_ids = {item["post_id"] for item in selected}
    drop_reasons["below_selection_cutoff"] += len([item for item in scored if item["post_id"] not in selected_ids])

    audit = {
        "reviewed_tweet_count": len(items),
        "candidate_count": len(scored),
        "selected_count": len(selected),
        "dropped_count": len(items) - len(selected),
        "top_n": top_n,
        "drop_reasons": dict(sorted(drop_reasons.items())),
    }
    return selected, audit


def _selection_score(item: dict) -> tuple[int, list[str], str | None]:
    summary = str(item.get("summary") or "")
    text = summary.lower()
    classification = item.get("classification")
    metrics = item.get("metrics", [])
    evidence_urls = item.get("evidence_urls", [])
    scores = item.get("scores", {})

    if classification == "Skip":
        return 0, [], "classifier_skip"
    if text.startswith("rt @"):
        return 0, [], "retweet"
    if any(term in text for term in LOW_SIGNAL_TERMS):
        return 0, [], "low_signal_language"

    has_metric = bool(metrics)
    has_strong_announcement = any(term in text for term in STRONG_ANNOUNCEMENT_TERMS)
    has_deep_dive = any(term in text for term in DEEP_DIVE_TERMS)
    is_promo = any(term in text for term in PROMO_TERMS)

    if is_promo and not has_metric and not has_strong_announcement and not has_deep_dive:
        return 0, [], "event_or_podcast_promo"
    if classification == "Adoption Stat" and not has_metric and not has_strong_announcement and not has_deep_dive:
        return 0, [], "no_concrete_signal"

    score = 0
    reasons: list[str] = []

    if has_metric:
        score += 5
        reasons.append("hard metric extracted")
    if classification == "Announcement" or has_strong_announcement:
        score += 4
        reasons.append("concrete announcement language")
    if classification == "Deep Dive/Article" or has_deep_dive:
        score += 4
        reasons.append("deep-dive/report language")
    if evidence_urls:
        score += 1
        reasons.append("source link captured")
    if scores.get("evidence_quality", 0) >= 5:
        score += 2
        reasons.append("primary/dashboard source link")
    if scores.get("relevance", 0) >= 5:
        score += 2
        reasons.append("core Machines & Money theme")
    if scores.get("editorial_value", 0) >= 4:
        score += 1
        reasons.append("high editorial value")
    if is_promo:
        score -= 2
        reasons.append("promo/event framing penalty")

    if score < 5:
        return score, reasons, "below_quality_threshold"
    return score, reasons, None


def _posted_sort_key(item: dict) -> datetime:
    posted_at = str(item.get("posted_at") or "")
    if not posted_at:
        return datetime.min
    try:
        return datetime.fromisoformat(posted_at.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return datetime.min
