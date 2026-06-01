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
    parser.add_argument("--max-items", type=int)
    parser.add_argument("--output-dir", default=f"outputs/news-insights-scanner/{date.today().isoformat()}")
    args = parser.parse_args()

    lookback_hours = args.lookback_days * 24 if args.lookback_days else args.lookback_hours
    output = run_scanner(
        ScannerConfig(
            ingestion=args.ingestion,
            input_path=args.input,
            output_dir=args.output_dir,
            source_list_id=args.source_list_id,
            lookback_hours=lookback_hours,
            max_items=args.max_items,
        )
    )
    print(json.dumps(output.__dict__, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
