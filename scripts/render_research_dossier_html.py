#!/usr/bin/env python3
"""Render a Machines & Money research dossier Markdown file as clean HTML.

The output is intentionally simple Google-Docs-friendly HTML: headings, real
lists, paragraphs, inline emphasis, code spans, and links.
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


def inline_markdown(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    escaped = re.sub(
        r"(https?://[^\s<)]+)",
        r'<a href="\1">\1</a>',
        escaped,
    )
    return escaped


def render_markdown(markdown: str, title: str) -> str:
    parts: list[str] = [
        "<!doctype html>",
        "<html>",
        "<head>",
        '<meta charset="utf-8">',
        f"<title>{html.escape(title)}</title>",
        "</head>",
        "<body>",
    ]
    open_list: str | None = None

    def close_list() -> None:
        nonlocal open_list
        if open_list:
            parts.append(f"</{open_list}>")
            open_list = None

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            close_list()
            continue

        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        if heading:
            close_list()
            level = len(heading.group(1))
            parts.append(f"<h{level}>{inline_markdown(heading.group(2))}</h{level}>")
            continue

        bullet = re.match(r"^-\s+(.+)$", line)
        if bullet:
            if open_list != "ul":
                close_list()
                parts.append("<ul>")
                open_list = "ul"
            parts.append(f"<li>{inline_markdown(bullet.group(1))}</li>")
            continue

        numbered = re.match(r"^\d+\.\s+(.+)$", line)
        if numbered:
            if open_list != "ol":
                close_list()
                parts.append("<ol>")
                open_list = "ol"
            parts.append(f"<li>{inline_markdown(numbered.group(1))}</li>")
            continue

        close_list()
        parts.append(f"<p>{inline_markdown(line)}</p>")

    close_list()
    parts.extend(["</body>", "</html>"])
    return "\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown_path", type=Path)
    parser.add_argument("--output", "-o", type=Path)
    parser.add_argument("--title")
    args = parser.parse_args()

    markdown = args.markdown_path.read_text(encoding="utf-8")
    title = args.title or args.markdown_path.stem
    rendered = render_markdown(markdown, title)
    output = args.output or args.markdown_path.with_suffix(".html")
    output.write_text(rendered, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
