"""Link extraction and primary-source preference helpers."""

from __future__ import annotations

from urllib.parse import urlparse

from .models import CandidatePost


def extract_links(post: CandidatePost) -> list[dict[str, str]]:
    links = []
    seen = set()
    for raw in post.urls:
        url = str(raw.get("url", "")).strip()
        if not url or url in seen:
            continue
        seen.add(url)
        links.append(
            {
                "url": url,
                "source_kind": str(raw.get("source_kind") or infer_source_kind(url)),
                "label": str(raw.get("title") or raw.get("label") or host_label(url)),
            }
        )
    if post.post_url and post.post_url not in seen:
        links.append({"url": post.post_url, "source_kind": "reposted", "label": "X post"})
    return links


def preferred_evidence_urls(links: list[dict[str, str]]) -> list[str]:
    ordered = sorted(links, key=lambda link: _kind_rank(link["source_kind"]))
    return [link["url"] for link in ordered]


def infer_source_kind(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if any(source in host for source in ("dune.com", "defillama.com", "tokenterminal.com", "artemis.xyz")):
        return "dashboard"
    if host.endswith("x.com") or host.endswith("twitter.com"):
        return "reposted"
    return "primary"


def host_label(url: str) -> str:
    host = urlparse(url).netloc.lower().removeprefix("www.")
    return host or url


def _kind_rank(kind: str) -> int:
    return {"primary": 0, "dashboard": 1, "reposted": 2}.get(kind, 3)
