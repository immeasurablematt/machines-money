"""Data models shared by the scanner pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


DEFAULT_SOURCE_LIST_ID = "2011849979095138608"


@dataclass
class CandidatePost:
    post_id: str
    post_url: str
    author_handle: str
    posted_at: str
    text: str
    captured_at: str
    source_list_id: str = DEFAULT_SOURCE_LIST_ID
    urls: list[dict[str, Any]] = field(default_factory=list)
    project_names: list[str] = field(default_factory=list)
    title: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class IngestionResult:
    path: str
    source_list_id: str
    captured_at: str
    verification_status: str
    posts: list[CandidatePost] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class ScannerConfig:
    ingestion: str
    input_path: str | None
    output_dir: str
    source_list_id: str = DEFAULT_SOURCE_LIST_ID
    lookback_hours: int = 24
    max_items: int | None = None


@dataclass
class ScannerOutput:
    run_id: str
    markdown_path: str
    json_path: str
    item_count: int
    verification_status: str
    warnings: list[str]
