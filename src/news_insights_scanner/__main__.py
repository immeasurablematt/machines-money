"""Command-line entry point for the scanner MVP."""

from __future__ import annotations

import argparse
import json
from datetime import date

from .models import DEFAULT_SOURCE_LIST_ID, ScannerConfig
from .pipeline import run_scanner


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Machines & Money X List News & Insights Scanner.")
    parser.add_argument("--ingestion", choices=["manual", "x_api"], default="manual")
    parser.add_argument("--input", help="Manual JSON or newline input file. Required for manual ingestion.")
    parser.add_argument("--source-list-id", default=DEFAULT_SOURCE_LIST_ID)
    parser.add_argument("--lookback-hours", type=int, default=24)
    parser.add_argument("--lookback-days", type=int, help="Convenience override for multi-day scans.")
    parser.add_argument("--top-n", type=int, default=12, help="Number of selected items to show in the human digest.")
    parser.add_argument("--max-items", type=int, help="Deprecated alias for --top-n.")
    parser.add_argument("--max-ingest-pages", type=int, default=10, help="Safety cap for X API pagination pages.")
    parser.add_argument("--output-dir", default=f"outputs/news-insights-scanner/{date.today().isoformat()}")
    args = parser.parse_args()

    lookback_hours = args.lookback_days * 24 if args.lookback_days else args.lookback_hours
    top_n = args.max_items if args.max_items is not None else args.top_n
    output = run_scanner(
        ScannerConfig(
            ingestion=args.ingestion,
            input_path=args.input,
            output_dir=args.output_dir,
            source_list_id=args.source_list_id,
            lookback_hours=lookback_hours,
            top_n=top_n,
            max_ingest_pages=args.max_ingest_pages,
        )
    )
    cli_payload = {
        "run_id": output.run_id,
        "markdown_path": output.markdown_path,
        "json_path": output.json_path,
        "item_count": output.item_count,
        "review_status": _review_status_label(output.verification_status),
        "warnings": output.warnings,
    }
    print(json.dumps(cli_payload, indent=2, sort_keys=True))
    return 0


def _review_status_label(status: str) -> str:
    if status == "verified":
        return "source checked"
    if status == "manual_review_needed":
        return "needs setup attention"
    return "ready for Ian review; check sources before publishing"


if __name__ == "__main__":
    raise SystemExit(main())
