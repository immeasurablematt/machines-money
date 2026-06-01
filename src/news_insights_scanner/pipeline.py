"""Source-agnostic scanner pipeline."""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from .classify_items import classify_item, why_it_matters
from .dedupe import dedupe_items
from .extract_links import extract_links, preferred_evidence_urls
from .extract_metrics import extract_metrics
from .ingest import ingest_manual, ingest_x_api
from .models import CandidatePost, ScannerConfig, ScannerOutput
from .render_digest import render_outputs
from .score_items import priority, score_item


def run_scanner(config: ScannerConfig) -> ScannerOutput:
    ingestion = _ingest(config)
    run_id = f"news-insights-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    posts = _filter_lookback(ingestion.posts, config.lookback_hours)
    if config.max_items:
        posts = posts[: config.max_items]

    items = [_build_item(run_id, post) for post in posts]
    items = dedupe_items(items)
    verification_status = _run_verification_status(ingestion.verification_status, items)
    payload = {
        "run_id": run_id,
        "source_list_id": config.source_list_id,
        "ingestion_path": ingestion.path,
        "captured_at": ingestion.captured_at,
        "lookback_hours": config.lookback_hours,
        "verification_status": verification_status,
        "warnings": ingestion.warnings,
        "items": items,
    }
    markdown_path, json_path = render_outputs(payload, config.output_dir)
    return ScannerOutput(
        run_id=run_id,
        markdown_path=markdown_path,
        json_path=json_path,
        item_count=len(items),
        verification_status=verification_status,
        warnings=ingestion.warnings,
    )


def _ingest(config: ScannerConfig):
    if config.ingestion == "manual":
        if not config.input_path:
            raise ValueError("Manual ingestion requires --input.")
        return ingest_manual(config.input_path, config.source_list_id)
    if config.ingestion == "x_api":
        return ingest_x_api(config.source_list_id, config.max_items or 100)
    raise ValueError(f"Unsupported ingestion path: {config.ingestion}")


def _build_item(run_id: str, post: CandidatePost) -> dict:
    links = extract_links(post)
    evidence_urls = preferred_evidence_urls(links)
    classification = classify_item(post)
    metrics = extract_metrics(post, evidence_urls)
    scores = score_item(post, classification, evidence_urls, metrics)
    item_priority = priority(scores)
    verification_status = _item_verification_status(post, classification, evidence_urls, metrics)
    summary = _summary(post)
    item = {
        "run_id": run_id,
        "source_list_id": post.source_list_id,
        "post_id": post.post_id,
        "post_url": post.post_url,
        "author_handle": post.author_handle,
        "posted_at": post.posted_at,
        "captured_at": post.captured_at,
        "classification": classification,
        "project_names": _project_names(post),
        "summary": summary,
        "evidence_urls": evidence_urls,
        "metrics": metrics,
        "scores": scores,
        "confidence": _confidence_label(scores, verification_status),
        "priority": item_priority,
        "recommended_action": _recommended_action(classification, item_priority, metrics, post),
        "verification_status": verification_status,
        "notes": _notes(post, classification, verification_status),
        "why_it_matters": why_it_matters(classification, summary),
    }
    dossier_seed = _dossier_seed(item)
    if dossier_seed:
        item["dossier_seed"] = dossier_seed
    return item


def _filter_lookback(posts: list[CandidatePost], lookback_hours: int) -> list[CandidatePost]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=lookback_hours)
    filtered = []
    for post in posts:
        if not post.posted_at:
            filtered.append(post)
            continue
        try:
            posted_at = datetime.fromisoformat(post.posted_at.replace("Z", "+00:00")).astimezone(timezone.utc)
        except ValueError:
            filtered.append(post)
            continue
        if posted_at >= cutoff:
            filtered.append(post)
    return filtered


def _summary(post: CandidatePost) -> str:
    text = post.title or post.text.strip().replace("\n", " ")
    if not text:
        return "Untitled scanner item"
    return text if len(text) <= 160 else text[:157].rstrip() + "..."


def _project_names(post: CandidatePost) -> list[str]:
    if post.project_names:
        return post.project_names
    words = []
    for token in post.text.replace("#", " ").split():
        clean = token.strip(".,:;()[]")
        if clean[:1].isupper() and len(clean) > 2 and clean.lower() not in {"the", "ian"}:
            words.append(clean)
    return words[:3] or ["Unknown"]


def _item_verification_status(
    post: CandidatePost, classification: str, evidence_urls: list[str], metrics: list[dict]
) -> str:
    explicit_status = post.metadata.get("verification_status")
    if explicit_status in {"verified", "needs_verification", "manual_review_needed"}:
        return str(explicit_status)
    if post.metadata.get("source_verified") is True:
        return "verified"
    if classification == "Skip":
        return "needs_verification"
    if not evidence_urls:
        return "needs_verification"
    if classification == "Adoption Stat" and not metrics:
        return "needs_verification"
    return "needs_verification"


def _recommended_action(classification: str, item_priority: str, metrics: list[dict], post: CandidatePost) -> str:
    override = post.metadata.get("recommended_action")
    if override:
        return str(override)
    if classification == "Skip":
        return "skip"
    if classification == "Adoption Stat" and metrics:
        return "save chart/stat"
    if classification == "Deep Dive/Article" and item_priority == "High":
        return "save read"
    if classification == "Announcement" and item_priority == "High":
        return "short mention"
    if item_priority == "Medium":
        return "track project"
    return "verify"


def _confidence_label(scores: dict[str, int], verification_status: str) -> str:
    if verification_status != "verified":
        return "medium" if scores["evidence_quality"] >= 3 else "low"
    if scores["evidence_quality"] >= 5:
        return "high"
    if scores["evidence_quality"] >= 3:
        return "medium"
    return "low"


def _notes(post: CandidatePost, classification: str, verification_status: str) -> str:
    notes = [str(post.metadata.get("notes") or "").strip()]
    if verification_status != "verified":
        notes.append("Needs manual verification before reuse.")
    if classification == "Skip":
        notes.append("Collapsed into low-signal section by MVP classifier.")
    return " ".join(note for note in notes if note)


def _dossier_seed(item: dict) -> dict | None:
    if item["classification"] != "Deep Dive/Article" or item["priority"] != "High":
        return None
    if len(item.get("project_names", [])) != 1:
        return None
    project = item["project_names"][0]
    if project == "Unknown":
        return None
    return {
        "project_name": project,
        "why_it_surfaced": "High-priority single-project deep dive candidate from the broad scanner.",
        "best_source_links": item["evidence_urls"][:3],
        "key_metrics_found": item["metrics"],
        "differentiating_feature_or_thesis": item["summary"],
        "suggested_hands_on_test": "Open the current project app or docs and identify a practical non-custodial product flow; do not trade, stake, deposit, withdraw, or sign.",
        "open_questions": ["What is current as of the source date?", "What can Ian safely test directly?"],
        "dossier_questions": {
            "what_does_it_do": "Needs focused follow-up.",
            "why_important_unique": "Needs focused follow-up.",
            "how_can_this_help_people": "Needs focused follow-up.",
            "how_are_we_using_it": "Needs focused follow-up.",
        },
    }


def _run_verification_status(ingestion_status: str, items: list[dict]) -> str:
    if ingestion_status == "manual_review_needed":
        return "manual_review_needed"
    if any(item["verification_status"] != "verified" for item in items):
        return "needs_verification"
    return "verified"
