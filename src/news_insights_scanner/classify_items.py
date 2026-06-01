"""Heuristic item classification for scanner candidates."""

from __future__ import annotations

import re

from .models import CandidatePost


ANNOUNCEMENT_RE = re.compile(
    r"\b(announce|announced|launch|launched|release|released|partnership|partner|integration|"
    r"integrated|fundraise|raised|governance|proposal|vote|roadmap|mainnet|campaign|incentive)\b",
    re.IGNORECASE,
)
METRIC_RE = re.compile(
    r"(\$?\d[\d,.]*(?:\.\d+)?\s?(?:m|mn|million|b|bn|billion|k|%)?|\bTVL\b|\bAUM\b|\bfees?\b|"
    r"\brevenue\b|\bvolume\b|\busers?\b|\bwallets?\b|\btransactions?\b|\bbuybacks?\b)",
    re.IGNORECASE,
)
DEEP_DIVE_RE = re.compile(
    r"\b(deep dive|research|analysis|essay|thread|article|report|thesis|explainer|"
    r"technical|mechanism|market structure|case study)\b",
    re.IGNORECASE,
)
SKIP_RE = re.compile(r"\b(meme|giveaway|gm\b|airdrop rumor|price only|vibes|lol)\b", re.IGNORECASE)


def classify_item(post: CandidatePost) -> str:
    expected = post.metadata.get("expected_classification")
    if expected in {"Announcement", "Adoption Stat", "Deep Dive/Article", "Skip"}:
        return str(expected)

    text = " ".join(part for part in (post.title or "", post.text) if part)
    if SKIP_RE.search(text):
        return "Skip"
    if DEEP_DIVE_RE.search(text):
        return "Deep Dive/Article"
    if ANNOUNCEMENT_RE.search(text):
        return "Announcement"
    if METRIC_RE.search(text):
        return "Adoption Stat"
    return "Skip"


def why_it_matters(classification: str, summary: str) -> str:
    if classification == "Announcement":
        return "Concrete project news that may support a timely newsletter mention or project-watch update."
    if classification == "Adoption Stat":
        return "A dated metric that may support a chart, traction note, or Truth Within Trends angle."
    if classification == "Deep Dive/Article":
        return "Substantive analysis that may be worth reading, saving, or using as an article angle."
    return "Low-signal for the current broad scanner unless Ian is already tracking this project."
