#!/usr/bin/env python3
"""Refresh the Machines & Money dashboard prototype data.

The dashboard is still a static HTML prototype, so this script writes a small
JavaScript data file that can be loaded directly from file:// without a server.
"""

from __future__ import annotations

import csv
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "docs" / "dashboard"
DATA_JS = DASHBOARD_DIR / "generated-dashboard-data.js"
DATA_CSV = DASHBOARD_DIR / "generated-dashboard-data.csv"

USER_AGENT = "machines-money-dashboard-refresh/0.1"


RECORDS = [
    {
        "project": "Uniswap",
        "record": "Uniswap V3",
        "sector": "Spot",
        "protocol_slug": "uniswap-v3",
        "fee_slug": "uniswap-v3",
        "dex_module": "uniswap-v3",
        "confidence": "high",
        "notes": "Version-specific record; do not silently blend with V2/V4.",
    },
    {
        "project": "Uniswap",
        "record": "Uniswap V2",
        "sector": "Spot",
        "protocol_slug": "uniswap-v2",
        "fee_slug": "uniswap-v2",
        "dex_module": "uniswap-v2",
        "confidence": "high",
        "notes": "Version-specific legacy liquidity record.",
    },
    {
        "project": "Uniswap",
        "record": "Uniswap V4",
        "sector": "Spot",
        "protocol_slug": "uniswap-v4",
        "fee_slug": "uniswap-v4",
        "dex_module": "uniswap-v4",
        "confidence": "high",
        "notes": "Version-specific record; aggregation rule needs to stay visible.",
    },
    {
        "project": "Aave",
        "record": "Aave V3",
        "sector": "Lending",
        "protocol_slug": "aave-v3",
        "fee_slug": "aave-v3",
        "confidence": "high",
        "notes": "Primary Aave MVP lending record.",
    },
    {
        "project": "Aave",
        "record": "Aave V4",
        "sector": "Lending",
        "protocol_slug": "aave-v4",
        "fee_slug": "aave-v4",
        "confidence": "medium",
        "notes": "V4 hub/spoke detail still needs native source discovery.",
    },
    {
        "project": "Pendle",
        "record": "Pendle",
        "sector": "Derivatives",
        "protocol_slug": "pendle",
        "fee_slug": "pendle",
        "confidence": "high",
        "notes": "PT/YT volume and vePENDLE yield require separate source discovery.",
    },
    {
        "project": "Hyperliquid",
        "record": "Hyperliquid HLP",
        "sector": "Derivatives",
        "protocol_slug": "hyperliquid-hlp",
        "fee_slug": "hyperliquid-hlp",
        "confidence": "medium",
        "notes": "HLP-specific record; not total Hyperliquid perps activity.",
    },
    {
        "project": "Hyperliquid",
        "record": "Hyperliquid Spot Orderbook",
        "sector": "Derivatives",
        "protocol_slug": "hyperliquid-spot-orderbook",
        "confidence": "medium",
        "notes": "Spot-orderbook record; keep separate from HLP and perps.",
    },
    {
        "project": "Ethena",
        "record": "Ethena USDe",
        "sector": "Asset Management",
        "protocol_slug": "ethena-usde",
        "fee_slug": "ethena-usde",
        "confidence": "high",
        "notes": "USDe-specific record; reserves and APY need native source checks.",
    },
    {
        "project": "Ethena",
        "record": "Ethena USDtb",
        "sector": "Asset Management",
        "protocol_slug": "ethena-usdtb",
        "fee_slug": "ethena-usdtb",
        "confidence": "medium",
        "notes": "Separate Ethena stablecoin product.",
    },
    {
        "project": "Sky",
        "record": "Sky Lending",
        "sector": "Lending",
        "protocol_slug": "sky-lending",
        "fee_slug": "sky-lending",
        "confidence": "high",
        "notes": "Lending/CDP record; APY and Agent metrics need native source checks.",
    },
    {
        "project": "Sky",
        "record": "Sky Money",
        "sector": "Asset Management",
        "protocol_slug": "sky-money",
        "confidence": "medium",
        "notes": "Separate Sky money product record.",
    },
    {
        "project": "Sky",
        "record": "Sky RWA",
        "sector": "Tokenization",
        "protocol_slug": "sky-rwa",
        "confidence": "medium",
        "notes": "Separate Sky RWA record.",
    },
    {
        "project": "Ondo",
        "record": "Ondo Yield Assets",
        "sector": "Tokenization",
        "protocol_slug": "ondo-yield-assets",
        "fee_slug": "ondo-yield-assets",
        "confidence": "high",
        "notes": "Good tokenized-assets starter record.",
    },
    {
        "project": "Ondo",
        "record": "Ondo Global Markets",
        "sector": "Tokenization",
        "protocol_slug": "ondo-global-markets",
        "confidence": "medium",
        "notes": "Separate Ondo product; confirm MVP scope.",
    },
    {
        "project": "Aerodrome",
        "record": "Aerodrome Slipstream",
        "sector": "Spot",
        "protocol_slug": "aerodrome-slipstream",
        "fee_slug": "aerodrome-slipstream",
        "dex_module": "aerodrome-slipstream",
        "confidence": "high",
        "notes": "Concentrated-liquidity record; keep separate from V1 unless labeled.",
    },
    {
        "project": "Aerodrome",
        "record": "Aerodrome V1",
        "sector": "Spot",
        "protocol_slug": "aerodrome-v1",
        "fee_slug": "aerodrome",
        "dex_module": "aerodrome",
        "confidence": "high",
        "notes": "V1 record; keep version labels.",
    },
    {
        "project": "Morpho",
        "record": "Morpho Blue",
        "sector": "Lending",
        "protocol_slug": "morpho-blue",
        "fee_slug": "morpho-blue",
        "confidence": "high",
        "notes": "Curator data needs Morpho-native or Dune source.",
    },
    {
        "project": "Jupiter",
        "record": "Jupiter Lend",
        "sector": "Lending",
        "protocol_slug": "jupiter-lend",
        "confidence": "medium",
        "notes": "Separate product record; not aggregator usage.",
    },
    {
        "project": "Jupiter",
        "record": "Jupiter Perpetual Exchange",
        "sector": "Derivatives",
        "protocol_slug": "jupiter-perpetual-exchange",
        "fee_slug": "jupiter-perpetual-exchange",
        "confidence": "medium",
        "notes": "Perps product record; derivatives overview access may be restricted.",
    },
    {
        "project": "Jupiter",
        "record": "Jupiter Staked SOL",
        "sector": "Asset Management",
        "protocol_slug": "jupiter-staked-sol",
        "confidence": "medium",
        "notes": "Liquid-staking product record.",
    },
]


def fetch_json(url: str) -> Any:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=25) as response:
        return json.load(response)


def source_url(path: str) -> str:
    return f"https://api.llama.fi/{path}"


def append_row(
    rows: list[dict[str, Any]],
    *,
    record: dict[str, str],
    metric: str,
    value: float | int | None,
    period: str,
    source_name: str,
    source: str,
    notes: str | None = None,
) -> None:
    if value is None:
        return
    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return
    if numeric_value <= 0:
        return

    rows.append(
        {
            "pulled_date": date.today().isoformat(),
            "project": record["project"],
            "record": record["record"],
            "sector": record["sector"],
            "metric": metric,
            "value": round(numeric_value, 2),
            "unit": "USD",
            "period": period,
            "source_name": source_name,
            "source": source,
            "source_relationship": "third_party",
            "confidence": record["confidence"],
            "notes": notes or record["notes"],
        }
    )


def build_rows() -> tuple[list[dict[str, Any]], list[str]]:
    warnings: list[str] = []
    metric_rows: list[dict[str, Any]] = []

    protocols = fetch_json(source_url("protocols"))
    tvl_by_slug = {item.get("slug"): item.get("tvl") for item in protocols}

    for record in RECORDS:
        append_row(
            metric_rows,
            record=record,
            metric="TVL",
            value=tvl_by_slug.get(record["protocol_slug"]),
            period="current",
            source_name="DefiLlama protocol",
            source=source_url(f"protocol/{record['protocol_slug']}"),
        )

    for metric, data_type in [("30D Fees", "dailyFees"), ("30D Revenue", "dailyRevenue")]:
        for record in RECORDS:
            fee_slug = record.get("fee_slug")
            if not fee_slug:
                continue
            url_path = f"summary/fees/{fee_slug}?dataType={data_type}"
            try:
                data = fetch_json(source_url(url_path))
            except urllib.error.HTTPError as exc:
                if exc.code not in (400, 404):
                    warnings.append(f"{metric} unavailable for {record['record']}: HTTP {exc.code}")
                continue
            except Exception as exc:  # noqa: BLE001 - retain source warning in generated metadata.
                warnings.append(f"{metric} unavailable for {record['record']}: {exc.__class__.__name__}")
                continue

            append_row(
                metric_rows,
                record=record,
                metric=metric,
                value=data.get("total30d"),
                period="30D",
                source_name="DefiLlama fees",
                source=source_url(url_path),
                notes=f"{metric} from DefiLlama fees endpoint. Methodology should be reviewed before final citation.",
            )
            time.sleep(0.05)

    try:
        dex_data = fetch_json(
            source_url(
                "overview/dexs?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true"
            )
        )
        dex_by_module = {item.get("module"): item for item in dex_data.get("protocols", [])}
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"DEX volume unavailable: {exc.__class__.__name__}")
        dex_by_module = {}

    for record in RECORDS:
        dex_module = record.get("dex_module")
        if not dex_module:
            continue
        dex_record = dex_by_module.get(dex_module)
        if not dex_record:
            warnings.append(f"30D DEX Volume missing for {record['record']}")
            continue
        append_row(
            metric_rows,
            record=record,
            metric="30D DEX Volume",
            value=dex_record.get("total30d"),
            period="30D",
            source_name="DefiLlama DEX overview",
            source=source_url(
                "overview/dexs?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true"
            ),
            notes="DEX volume is source-comparable only for DEX records; lending and derivatives volume still need separate source discovery.",
        )

    metric_rows.sort(key=lambda row: (row["metric"], -row["value"], row["project"], row["record"]))
    return metric_rows, warnings


def write_outputs(rows: list[dict[str, Any]], warnings: list[str]) -> None:
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "pulled_date",
        "project",
        "record",
        "sector",
        "metric",
        "value",
        "unit",
        "period",
        "source_name",
        "source",
        "source_relationship",
        "confidence",
        "notes",
    ]
    with DATA_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "generated_at": date.today().isoformat(),
        "row_count": len(rows),
        "warnings": warnings,
        "source_note": "Generated from public DefiLlama endpoints; review methodology before final citation.",
    }
    js = (
        "// Generated by scripts/refresh_dashboard_data.py. Do not edit by hand.\n"
        f"window.dashboardMeta = {json.dumps(metadata, indent=2)};\n"
        f"window.dashboardRows = {json.dumps(rows, indent=2)};\n"
    )
    DATA_JS.write_text(js)


def main() -> int:
    rows, warnings = build_rows()
    if not rows:
        print("No dashboard rows generated.", file=sys.stderr)
        return 1
    write_outputs(rows, warnings)
    print(f"Wrote {len(rows)} rows to {DATA_CSV}")
    print(f"Wrote {DATA_JS}")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
