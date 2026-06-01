"""Markdown and JSON rendering."""

from __future__ import annotations

import json
from pathlib import Path


SECTIONS = [
    ("Top Picks", lambda item: item["priority"] == "High"),
    ("Worth A Look", lambda item: item["priority"] == "Medium"),
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
    audit = payload.get("selection_audit") or {}
    items = payload.get("items", [])
    lines = [
        "# X List News & Insights Scanner Digest",
        "",
        "## Executive Summary",
        "",
        _summary_sentence(payload, audit),
        "",
        _class_mix_sentence(items),
        "",
        "Use this as Ian's reading shortlist. Source links are captured, but any claim or metric should still be checked before it is quoted or published.",
    ]

    if payload.get("warnings"):
        lines.extend(["", "## Setup Notes", ""])
        lines.extend(f"- {warning}" for warning in payload["warnings"])

    for title, predicate in SECTIONS:
        section_items = [item for item in items if predicate(item)]
        if not section_items and title == "Worth A Look":
            continue
        lines.extend(["", f"## {title}", ""])
        if not section_items:
            lines.append("_No items._")
            continue
        for item in section_items:
            lines.extend(_item_lines(item))

    low_priority_count = len([item for item in items if item["priority"] == "Low"])
    if low_priority_count:
        lines.extend(
            [
                "",
                "## Low Priority",
                "",
                f"{low_priority_count} selected item(s) were low priority and are omitted from the reader brief.",
            ]
        )

    if audit:
        lines.extend(["", "## How It Was Narrowed", ""])
        lines.append(
            f"The scanner reviewed {audit.get('reviewed_tweet_count', 0)} tweets from the last "
            f"{payload['lookback_hours']} hours and selected {audit.get('selected_count', 0)} for Ian."
        )
        drop_reasons = audit.get("drop_reasons") or {}
        omitted = sum(
            drop_reasons.get(reason, 0)
            for reason in ["retweet", "no_concrete_signal", "event_or_podcast_promo", "low_signal_language"]
        )
        if omitted:
            lines.append(f"It omitted {omitted} retweets, promos, or low-signal posts from the reader-facing brief.")

    lines.extend(
        [
            "",
            "## Run Details",
            "",
            f"- Captured: {payload['captured_at']}",
            f"- Source: X list {payload['source_list_id']}",
            f"- Ingestion: {payload['ingestion_path']}",
            f"- Run ID: {payload['run_id']}",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def _item_lines(item: dict) -> list[str]:
    evidence = ", ".join(f"[source {index + 1}]({url})" for index, url in enumerate(item.get("evidence_urls", []))) or "No source link captured"
    lines = [
        f"### {item['summary']}",
        "",
        f"- Type: {item['classification']}",
        f"- Source account: @{item.get('author_handle') or 'unknown'}",
        f"- Why it matters: {item['why_it_matters']}",
        f"- Source links: {evidence}",
        f"- Suggested next step: {_action_label(item['recommended_action'])}",
        f"- Posted: {item.get('posted_at') or 'unknown'}",
    ]
    metrics = _metrics_line(item.get("metrics", []))
    if metrics:
        lines.insert(-2, f"- Metric or chart to check: {metrics}")
    if item.get("dossier_seed"):
        seed = item["dossier_seed"]
        questions = "; ".join(f"{key}: {value}" for key, value in seed["dossier_questions"].items())
        lines.extend(
            [
                f"- Optional dossier seed: {seed['project_name']} - {seed['why_it_surfaced']}",
                f"- Dossier questions: {questions}",
            ]
        )
    lines.append("")
    return lines


def _summary_sentence(payload: dict, audit: dict) -> str:
    reviewed = audit.get("reviewed_tweet_count", 0)
    selected = audit.get("selected_count", len(payload.get("items", [])))
    dropped = audit.get("dropped_count", 0)
    return (
        f"Reviewed {reviewed} tweets from the last {payload['lookback_hours']} hours and selected "
        f"{selected} high-signal {_plural('item', selected)} for Ian. "
        f"{dropped} lower-value {_plural('item', dropped)} were filtered out."
    )


def _class_mix_sentence(items: list[dict]) -> str:
    if not items:
        return "No high-signal announcements, adoption stats, or deep reads were selected in this run."
    counts: dict[str, int] = {}
    for item in items:
        counts[item["classification"]] = counts.get(item["classification"], 0) + 1
    parts = [f"{count} {_plural(name.lower(), count)}" for name, count in sorted(counts.items())]
    return "Today's shortlist includes " + ", ".join(parts) + "."


def _plural(label: str, count: int) -> str:
    if count == 1:
        return label
    if label.endswith("y"):
        return label[:-1] + "ies"
    if "/" in label:
        return label + "s"
    return label + "s"


def _action_label(action: str) -> str:
    labels = {
        "save chart/stat": "Save the chart or stat after checking the source",
        "save read": "Save as a deep-read candidate",
        "short mention": "Consider for a short newsletter mention",
        "track project": "Track the project if it connects to an active theme",
        "verify": "Check the linked source before using",
        "skip": "Skip",
    }
    return labels.get(action, action)


def _metrics_line(metrics: list[dict]) -> str:
    if not metrics:
        return ""
    return "; ".join(
        f"{metric['metric_name']} {metric['value']} ({metric['period']}, {metric['source_kind']}, confidence {metric['confidence']})"
        for metric in metrics
    )
