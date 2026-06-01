"""Metric extraction for adoption-stat candidates."""

from __future__ import annotations

import re
from datetime import date

from .extract_links import infer_source_kind, preferred_evidence_urls
from .models import CandidatePost


METRIC_PATTERNS = [
    ("TVL", re.compile(r"\b(?:TVL|total value locked)\b[^$0-9]*(\$?\d[\d,.]*(?:\.\d+)?\s?(?:k|m|mn|million|b|bn|billion)?)", re.IGNORECASE)),
    ("AUM", re.compile(r"\bAUM\b[^$0-9]*(\$?\d[\d,.]*(?:\.\d+)?\s?(?:k|m|mn|million|b|bn|billion)?)", re.IGNORECASE)),
    ("Revenue", re.compile(r"\brevenue\b[^$0-9]*(\$?\d[\d,.]*(?:\.\d+)?\s?(?:k|m|mn|million|b|bn|billion)?)", re.IGNORECASE)),
    ("Fees", re.compile(r"\bfees?\b[^$0-9]*(\$?\d[\d,.]*(?:\.\d+)?\s?(?:k|m|mn|million|b|bn|billion)?)", re.IGNORECASE)),
    ("Volume", re.compile(r"\bvolume\b[^$0-9]*(\$?\d[\d,.]*(?:\.\d+)?\s?(?:k|m|mn|million|b|bn|billion)?)", re.IGNORECASE)),
    ("Active Loans", re.compile(r"(\$?\d[\d,.]*(?:\.\d+)?\s?(?:k|m|mn|million|b|bn|billion)?)\s+in\s+active\s+loans\b", re.IGNORECASE)),
    ("Users", re.compile(r"(\d[\d,.]*(?:\.\d+)?\s?(?:k|m|mn|million)?)\s+(?:active\s+)?users?\b", re.IGNORECASE)),
    ("Wallets", re.compile(r"(\d[\d,.]*(?:\.\d+)?\s?(?:k|m|mn|million)?)\s+(?:active\s+)?wallets?\b", re.IGNORECASE)),
    ("Transactions", re.compile(r"(\d[\d,.]*(?:\.\d+)?\s?(?:k|m|mn|million)?)\s+transactions?\b", re.IGNORECASE)),
]
PERIOD_RE = re.compile(r"\b(last|past|trailing)\s+(\d+\s+(?:hours?|days?|weeks?|months?))|\b(Q[1-4]\s+20\d{2}|20\d{2})\b", re.IGNORECASE)


def extract_metrics(post: CandidatePost, evidence_urls: list[str]) -> list[dict[str, str]]:
    text = " ".join(part for part in (post.title or "", post.text) if part)
    metrics = []
    for metric_name, pattern in METRIC_PATTERNS:
        match = pattern.search(text)
        if not match:
            continue
        source_url = _metric_source(evidence_urls)
        metrics.append(
            {
                "metric_name": metric_name,
                "value": match.group(1).strip(),
                "period": _period(text),
                "source_url": source_url,
                "pulled_date": date.today().isoformat(),
                "confidence": _confidence(source_url),
                "source_kind": infer_source_kind(source_url) if source_url else "unknown",
            }
        )
    return metrics


def _metric_source(evidence_urls: list[str]) -> str:
    if not evidence_urls:
        return ""
    return preferred_evidence_urls([{"url": url, "source_kind": infer_source_kind(url)} for url in evidence_urls])[0]


def _period(text: str) -> str:
    match = PERIOD_RE.search(text)
    if not match:
        return "unspecified"
    return " ".join(group for group in match.groups() if group)


def _confidence(source_url: str) -> str:
    if not source_url:
        return "low"
    kind = infer_source_kind(source_url)
    if kind in {"primary", "dashboard"}:
        return "medium"
    return "low"
