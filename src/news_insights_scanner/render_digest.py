"""Markdown and JSON rendering."""

from __future__ import annotations

import json
from pathlib import Path


SECTIONS = [
    ("Top Picks", lambda item: item["priority"] == "High" and item["classification"] != "Skip"),
    ("Announcements", lambda item: item["classification"] == "Announcement"),
    ("Adoption Stats & Charts", lambda item: item["classification"] == "Adoption Stat"),
    ("Deep Dives & Articles", lambda item: item["classification"] == "Deep Dive/Article"),
    ("Follow-Up Candidates", lambda item: item["recommended_action"] in {"track project", "track theme", "optional dossier seed", "save read"}),
    ("Needs Verification", lambda item: item["verification_status"] != "verified"),
    ("Skipped/Low-Signal", lambda item: item["classification"] == "Skip" or item["priority"] == "Low"),
]


def render_outputs(payload: dict, output_dir: str) -> tuple[str, str]:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    markdown_path = path / "digest.md"
    json_path = path / "digest.json"
    markdown_path.write_text(render_markdown(payload), encoding="utf-8")
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return str(markdown_path), str(json_path)


def render_markdown(payload: dict) -> str:
    lines = [
        "# X List News & Insights Scanner Digest",
        "",
        f"- Run ID: `{payload['run_id']}`",
        f"- Source list ID: `{payload['source_list_id']}`",
        f"- Ingestion path: `{payload['ingestion_path']}`",
        f"- Captured at: `{payload['captured_at']}`",
        f"- Lookback hours: `{payload['lookback_hours']}`",
        f"- Run verification status: `{payload['verification_status']}`",
    ]
    if payload.get("warnings"):
        lines.extend(["", "## Ingestion Warnings", ""])
        lines.extend(f"- {warning}" for warning in payload["warnings"])

    items = payload.get("items", [])
    for title, predicate in SECTIONS:
        section_items = [item for item in items if predicate(item)]
        lines.extend(["", f"## {title}", ""])
        if not section_items:
            lines.append("_No items._")
            continue
        for item in section_items:
            lines.extend(_item_lines(item))
    return "\n".join(lines).rstrip() + "\n"


def _item_lines(item: dict) -> list[str]:
    projects = ", ".join(item.get("project_names") or ["Unknown project"])
    evidence = ", ".join(f"[source {index + 1}]({url})" for index, url in enumerate(item.get("evidence_urls", []))) or "No source link captured"
    metrics = _metrics_line(item.get("metrics", []))
    scores = item.get("scores", {})
    lines = [
        f"### {item['summary']}",
        "",
        f"- Type: {item['classification']}",
        f"- Project: {projects}",
        f"- Date: {item.get('posted_at') or 'unknown'}",
        f"- Why it matters: {item['why_it_matters']}",
        f"- Source links: {evidence}",
        f"- Metrics: {metrics}",
        f"- Scores: relevance {scores.get('relevance')}, timeliness {scores.get('timeliness')}, evidence {scores.get('evidence_quality')}, editorial {scores.get('editorial_value')}",
        f"- Confidence: {item.get('confidence', 'unknown')}",
        f"- Priority: {item['priority']}",
        f"- Suggested next action: {item['recommended_action']}",
        f"- Verification: {item['verification_status']}",
    ]
    if item.get("dossier_seed"):
        seed = item["dossier_seed"]
        questions = "; ".join(f"{key}: {value}" for key, value in seed["dossier_questions"].items())
        lines.extend(
            [
                f"- Optional dossier seed: {seed['project_name']} - {seed['why_it_surfaced']}",
                f"- Dossier questions: {questions}",
            ]
        )
    if item.get("notes"):
        lines.append(f"- Notes: {item['notes']}")
    lines.append("")
    return lines


def _metrics_line(metrics: list[dict]) -> str:
    if not metrics:
        return "none captured"
    return "; ".join(
        f"{metric['metric_name']} {metric['value']} ({metric['period']}, {metric['source_kind']}, confidence {metric['confidence']})"
        for metric in metrics
    )
