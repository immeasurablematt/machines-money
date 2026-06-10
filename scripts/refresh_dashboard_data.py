#!/usr/bin/env python3
"""Refresh the Machines & Money dashboard data.

The dashboard is static, so this script writes browser-loadable data files.
Successful refreshes are snapshotted and copied to last-known-good files.
Failed refreshes restore the last-known-good generated files instead of
publishing broken or empty data.
"""

from __future__ import annotations

import csv
import shutil
import json
import os
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
TOKEN_MAP_CSV = DASHBOARD_DIR / "starter-token-map.csv"
SNAPSHOT_DIR = DASHBOARD_DIR / "snapshots"
LAST_GOOD_DIR = DASHBOARD_DIR / "last-good"
LAST_GOOD_JS = LAST_GOOD_DIR / "generated-dashboard-data.js"
LAST_GOOD_CSV = LAST_GOOD_DIR / "generated-dashboard-data.csv"
MIN_REFRESH_ROWS = int(os.environ.get("DASHBOARD_MIN_ROWS", "40"))
MIN_LAST_GOOD_RATIO = float(os.environ.get("DASHBOARD_MIN_LAST_GOOD_RATIO", "0.5"))

USER_AGENT = "machines-money-dashboard-refresh/0.2"
DUNE_API_BASE = "https://api.dune.com/api/v1"

DUNE_DEX_ACTIVE_WALLETS_SQL = """
SELECT
  project,
  count(DISTINCT tx_from) AS active_wallets_7d
FROM dex.trades
WHERE block_time >= now() - interval '7' day
  AND lower(project) IN ('uniswap', 'curve', 'aerodrome')
GROUP BY 1
ORDER BY active_wallets_7d DESC
LIMIT 20
"""

DUNE_DEX_PROJECTS = {
    "aerodrome": {"project": "Aerodrome", "sector": "Spot"},
    "curve": {"project": "Curve", "sector": "Spot"},
    "uniswap": {"project": "Uniswap", "sector": "Spot"},
}


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


# Perps/derivatives records matched against DefiLlama's derivatives overview by module.
# Module slugs are confirmed or corrected from first live-run warnings.
DERIVATIVES_RECORDS = [
    {"module": "hyperliquid", "project": "Hyperliquid", "record": "Hyperliquid Perps", "sector": "Derivatives", "confidence": "high", "notes": "Perp notional volume from DefiLlama derivatives overview."},
    {"module": "jupiter-perpetual-exchange", "project": "Jupiter", "record": "Jupiter Perpetual Exchange", "sector": "Derivatives", "confidence": "medium", "notes": "Perp notional volume from DefiLlama derivatives overview."},
]

# Stablecoin product supplies from stablecoins.llama.fi, matched by symbol.
STABLECOIN_RECORDS = {
    "USDe": {"project": "Ethena", "record": "Ethena USDe", "sector": "Asset Management", "confidence": "high", "notes": "Circulating stablecoin supply; product metric, not token market cap."},
    "USDtb": {"project": "Ethena", "record": "Ethena USDtb", "sector": "Asset Management", "confidence": "medium", "notes": "Circulating stablecoin supply; product metric, not token market cap."},
    "USDf": {"project": "Falcon", "record": "Falcon USDf", "sector": "Asset Management", "confidence": "medium", "notes": "Circulating stablecoin supply; reserve attestations need separate review."},
    "USDY": {"project": "Ondo", "record": "Ondo USDY", "sector": "Tokenization", "confidence": "high", "notes": "Tokenized yield-asset supply via DefiLlama stablecoins."},
    "USDS": {"project": "Sky", "record": "Sky USDS", "sector": "Asset Management", "confidence": "high", "notes": "Circulating stablecoin supply; product metric, not token market cap."},
}

# Yield pools from yields.llama.fi matched by (project, symbol); current APY only.
YIELD_POOL_RECORDS = [
    {"pool_project": "ethena", "symbol": "SUSDE", "project": "Ethena", "record": "Ethena sUSDe", "sector": "Asset Management", "confidence": "high", "notes": "Current sUSDe staking APY from DefiLlama yields; methodology is pool-level."},
    {"pool_project": "sky-money", "symbol": "SUSDS", "project": "Sky", "record": "Sky sUSDS", "sector": "Asset Management", "confidence": "medium", "notes": "Current sUSDS APY from DefiLlama yields; methodology is pool-level."},
]

# Lending records whose outstanding borrows (stock, not new-borrow flow) are read
# from the protocol endpoint's borrowed TVL. Definition decided 2026-06-10:
# the dashboard's "borrow volume" means outstanding borrows.
BORROW_RECORDS = [
    {"protocol_slug": "aave-v3", "project": "Aave", "record": "Aave V3", "sector": "Lending", "confidence": "high", "notes": "Outstanding borrows (current stock) from DefiLlama borrowed TVL; not daily new-borrow flow."},
    {"protocol_slug": "morpho-blue", "project": "Morpho", "record": "Morpho Blue", "sector": "Lending", "confidence": "high", "notes": "Outstanding borrows (current stock) from DefiLlama borrowed TVL; not daily new-borrow flow."},
    {"protocol_slug": "jupiter-lend", "project": "Jupiter", "record": "Jupiter Lend", "sector": "Lending", "confidence": "medium", "notes": "Outstanding borrows (current stock) from DefiLlama borrowed TVL; not daily new-borrow flow."},
    {"protocol_slug": "sky-lending", "project": "Sky", "record": "Sky Lending", "sector": "Lending", "confidence": "medium", "notes": "Outstanding borrows (current stock) from DefiLlama borrowed TVL; not daily new-borrow flow."},
]


def fetch_json(url: str, headers: dict[str, str] | None = None) -> Any:
    request_headers = {"User-Agent": USER_AGENT}
    if headers:
        request_headers.update(headers)
    req = urllib.request.Request(url, headers=request_headers)
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
    unit: str = "USD",
    notes: str | None = None,
    allow_negative: bool = False,
) -> None:
    if value is None:
        return
    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return
    if numeric_value != numeric_value:  # NaN guard
        return
    if not allow_negative and numeric_value <= 0:
        return

    rows.append(
        {
            "pulled_date": date.today().isoformat(),
            "project": record["project"],
            "record": record["record"],
            "sector": record["sector"],
            "metric": metric,
            "value": round(numeric_value, 2 if unit != "%" else 4),
            "unit": unit,
            "period": period,
            "source_name": source_name,
            "source": source,
            "source_relationship": "third_party",
            "confidence": record["confidence"],
            "notes": notes or record["notes"],
        }
    )


def read_token_map() -> list[dict[str, str]]:
    if not TOKEN_MAP_CSV.exists():
        return []
    with TOKEN_MAP_CSV.open(newline="") as handle:
        return list(csv.DictReader(handle))


def coingecko_source_url(ids: list[str]) -> str:
    joined_ids = ",".join(ids)
    return (
        "https://api.coingecko.com/api/v3/coins/markets"
        f"?vs_currency=usd&ids={joined_ids}"
        "&order=market_cap_desc&per_page=250&page=1&sparkline=false"
        "&price_change_percentage=24h%2C7d%2C30d%2C1y"
    )


def append_market_rows(metric_rows: list[dict[str, Any]], warnings: list[str]) -> None:
    token_rows = [
        row
        for row in read_token_map()
        if row.get("coingecko_id") and row.get("status") == "verified_search"
    ]
    if not token_rows:
        warnings.append("CoinGecko market data skipped: no verified token mappings")
        return

    api_key = os.environ.get("COINGECKO_DEMO_API_KEY")
    if not api_key:
        warnings.append(
            "CoinGecko market data skipped: set COINGECKO_DEMO_API_KEY after the free Demo key is available"
        )
        return

    ids = sorted({row["coingecko_id"] for row in token_rows})
    url = coingecko_source_url(ids)
    try:
        data = fetch_json(url, headers={"x-cg-demo-api-key": api_key})
    except urllib.error.HTTPError as exc:
        warnings.append(f"CoinGecko market data unavailable: HTTP {exc.code}")
        return
    except Exception as exc:  # noqa: BLE001 - retain source warning in generated metadata.
        warnings.append(f"CoinGecko market data unavailable: {exc.__class__.__name__}")
        return

    by_id = {item.get("id"): item for item in data if isinstance(item, dict)}
    for token in token_rows:
        market = by_id.get(token["coingecko_id"])
        if not market:
            warnings.append(f"CoinGecko market data missing for {token['project']} / {token['coingecko_id']}")
            continue

        record = {
            "project": token["project"],
            "record": f"{token['token_symbol']} token",
            "sector": token["sector"],
            "confidence": "high",
            "notes": token.get("notes", "Token-level market metric from CoinGecko."),
        }
        notes = "Token-level market metric from CoinGecko; do not treat as protocol/product usage."
        append_row(
            metric_rows,
            record=record,
            metric="Token Price",
            value=market.get("current_price"),
            period="current",
            source_name="CoinGecko markets",
            source=url,
            notes=notes,
        )
        append_row(
            metric_rows,
            record=record,
            metric="Market Cap",
            value=market.get("market_cap"),
            period="current",
            source_name="CoinGecko markets",
            source=url,
            notes=notes,
        )
        append_row(
            metric_rows,
            record=record,
            metric="FDV",
            value=market.get("fully_diluted_valuation"),
            period="current",
            source_name="CoinGecko markets",
            source=url,
            notes=notes,
        )
        append_row(
            metric_rows,
            record=record,
            metric="24H Token Volume",
            value=market.get("total_volume"),
            period="24H",
            source_name="CoinGecko markets",
            source=url,
            notes=notes,
        )
        for metric, field, period in [
            ("24H Token Performance", "price_change_percentage_24h_in_currency", "24H"),
            ("7D Token Performance", "price_change_percentage_7d_in_currency", "7D"),
            ("30D Token Performance", "price_change_percentage_30d_in_currency", "30D"),
            ("1Y Token Performance", "price_change_percentage_1y_in_currency", "1Y"),
        ]:
            append_row(
                metric_rows,
                record=record,
                metric=metric,
                value=market.get(field),
                unit="%",
                period=period,
                source_name="CoinGecko markets",
                source=url,
                notes="Token price change; market sentiment, not product adoption.",
                allow_negative=True,
            )


def dune_request(path: str, api_key: str, *, data: dict[str, Any] | None = None) -> Any:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
        "X-Dune-Api-Key": api_key,
    }
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(f"{DUNE_API_BASE}{path}", data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def execute_dune_sql(sql: str, api_key: str, warnings: list[str]) -> list[dict[str, Any]]:
    try:
        execution = dune_request(
            "/sql/execute",
            api_key,
            data={"sql": sql, "performance": "small"},
        )
    except urllib.error.HTTPError as exc:
        warnings.append(f"Dune SQL execution unavailable: HTTP {exc.code}")
        return []
    except Exception as exc:  # noqa: BLE001 - keep refresh resilient if Dune is unavailable.
        warnings.append(f"Dune SQL execution unavailable: {exc.__class__.__name__}")
        return []

    execution_id = execution.get("execution_id")
    if not execution_id:
        warnings.append("Dune SQL execution unavailable: no execution_id returned")
        return []

    state = execution.get("state")
    for _ in range(30):
        if state in {
            "QUERY_STATE_COMPLETED",
            "QUERY_STATE_FAILED",
            "QUERY_STATE_CANCELLED",
            "QUERY_STATE_EXPIRED",
        }:
            break
        time.sleep(2)
        try:
            status = dune_request(f"/execution/{execution_id}/status", api_key)
        except Exception as exc:  # noqa: BLE001
            warnings.append(f"Dune SQL status unavailable: {exc.__class__.__name__}")
            return []
        state = status.get("state")

    if state != "QUERY_STATE_COMPLETED":
        warnings.append(f"Dune SQL execution did not complete: {state}")
        return []

    try:
        result = dune_request(f"/execution/{execution_id}/results?limit=1000", api_key)
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"Dune SQL results unavailable: {exc.__class__.__name__}")
        return []

    rows = result.get("result", {}).get("rows", [])
    return rows if isinstance(rows, list) else []


def append_dune_active_wallet_rows(metric_rows: list[dict[str, Any]], warnings: list[str]) -> None:
    api_key = os.environ.get("DUNE_API_KEY")
    if not api_key:
        warnings.append("Dune active-wallet data skipped: set DUNE_API_KEY")
        return

    rows = execute_dune_sql(DUNE_DEX_ACTIVE_WALLETS_SQL, api_key, warnings)
    for row in rows:
        project_key = str(row.get("project", "")).lower()
        project = DUNE_DEX_PROJECTS.get(project_key)
        if not project:
            continue
        record = {
            "project": project["project"],
            "record": project["project"],
            "sector": project["sector"],
            "confidence": "medium",
            "notes": "7D active wallets from Dune dex.trades using distinct tx_from across all supported chains for this project. Treat as protocol-interaction wallets for the covered DEX surface.",
        }
        append_row(
            metric_rows,
            record=record,
            metric="7D Active Wallets",
            value=row.get("active_wallets_7d"),
            unit="wallets",
            period="7D",
            source_name="Dune dex.trades",
            source=f"{DUNE_API_BASE}/sql/execute",
            notes=record["notes"],
        )


def build_rows() -> tuple[list[dict[str, Any]], list[str]]:
    warnings: list[str] = []
    metric_rows: list[dict[str, Any]] = []

    protocols = fetch_json(source_url("protocols"))
    protocols_by_slug = {item.get("slug"): item for item in protocols}
    tvl_by_slug = {slug: item.get("tvl") for slug, item in protocols_by_slug.items()}

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
        protocol_item = protocols_by_slug.get(record["protocol_slug"]) or {}
        append_row(
            metric_rows,
            record=record,
            metric="7D TVL Growth",
            value=protocol_item.get("change_7d"),
            unit="%",
            period="7D",
            source_name="DefiLlama protocol",
            source=source_url("protocols"),
            notes="Point-in-time TVL change over 7 days, precomputed by DefiLlama.",
            allow_negative=True,
        )

    for metric, data_type in [
        ("30D Fees", "dailyFees"),
        ("30D Revenue", "dailyRevenue"),
        ("30D Holders Revenue", "dailyHoldersRevenue"),
    ]:
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
            if metric in ("30D Fees", "30D Revenue"):
                seven_day_metric = metric.replace("30D", "7D")
                append_row(
                    metric_rows,
                    record=record,
                    metric=seven_day_metric,
                    value=data.get("total7d"),
                    period="7D",
                    source_name="DefiLlama fees",
                    source=source_url(url_path),
                    notes=f"{seven_day_metric} from the same DefiLlama fees response as the 30D figure.",
                )
            time.sleep(0.05)

    try:
        fees_overview = fetch_json(
            source_url(
                "overview/fees?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true"
            )
        )
        fees_by_module = {item.get("module"): item for item in fees_overview.get("protocols", [])}
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"Fees overview unavailable: {exc.__class__.__name__}")
        fees_by_module = {}

    for record in RECORDS:
        fee_slug = record.get("fee_slug")
        overview_item = fees_by_module.get(fee_slug) if fee_slug else None
        if not overview_item:
            continue
        for metric, field, period in [
            ("7D Fee Growth", "change_7dover7d", "7D"),
            ("30D Fee Growth", "change_1m", "30D"),
        ]:
            append_row(
                metric_rows,
                record=record,
                metric=metric,
                value=overview_item.get(field),
                unit="%",
                period=period,
                source_name="DefiLlama fees overview",
                source=source_url("overview/fees"),
                notes="Fee growth precomputed by DefiLlama (current window vs prior window).",
                allow_negative=True,
            )

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

    # DEX volume market share from the same overview response (per spec: one call, no math).
    dex_category_total = sum(
        item.get("total30d") or 0 for item in dex_by_module.values() if isinstance(item, dict)
    )
    if dex_category_total:
        for record in RECORDS:
            dex_module = record.get("dex_module")
            dex_record = dex_by_module.get(dex_module) if dex_module else None
            if not dex_record or not dex_record.get("total30d"):
                continue
            append_row(
                metric_rows,
                record=record,
                metric="30D DEX Volume Share",
                value=dex_record["total30d"] / dex_category_total * 100,
                unit="%",
                period="30D",
                source_name="DefiLlama DEX overview",
                source=source_url("overview/dexs"),
                notes="Share of all DefiLlama-tracked DEX volume over 30D; record-level, not project-blended.",
            )

    deriv_by_module = {}
    for overview_path in (
        "overview/derivatives?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true",
        "overview/derivatives",
        "overview/perps?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true",
        "overview/perps",
    ):
        try:
            deriv_data = fetch_json(source_url(overview_path))
            deriv_by_module = {item.get("module"): item for item in deriv_data.get("protocols", [])}
            break
        except urllib.error.HTTPError as exc:
            warnings.append(f"Derivatives volume unavailable at {overview_path}: HTTP {exc.code}")
        except Exception as exc:  # noqa: BLE001
            warnings.append(f"Derivatives volume unavailable at {overview_path}: {exc.__class__.__name__}")

    deriv_category_total = sum(
        item.get("total30d") or 0 for item in deriv_by_module.values() if isinstance(item, dict)
    )
    for record in DERIVATIVES_RECORDS:
        deriv_record = deriv_by_module.get(record["module"])
        if not deriv_record:
            warnings.append(f"30D Derivatives Volume missing for {record['record']}")
            continue
        append_row(
            metric_rows,
            record=record,
            metric="30D Derivatives Volume",
            value=deriv_record.get("total30d"),
            period="30D",
            source_name="DefiLlama derivatives overview",
            source=source_url("overview/derivatives"),
            notes=record["notes"],
        )
        if deriv_category_total and deriv_record.get("total30d"):
            append_row(
                metric_rows,
                record=record,
                metric="30D Derivatives Volume Share",
                value=deriv_record["total30d"] / deriv_category_total * 100,
                unit="%",
                period="30D",
                source_name="DefiLlama derivatives overview",
                source=source_url("overview/derivatives"),
                notes="Share of all DefiLlama-tracked perp volume over 30D.",
            )

    for record in BORROW_RECORDS:
        url_path = f"protocol/{record['protocol_slug']}"
        try:
            protocol_detail = fetch_json(source_url(url_path))
        except Exception as exc:  # noqa: BLE001
            warnings.append(f"Outstanding Borrows unavailable for {record['record']}: {exc.__class__.__name__}")
            continue
        borrowed = (protocol_detail.get("currentChainTvls") or {}).get("borrowed")
        append_row(
            metric_rows,
            record=record,
            metric="Outstanding Borrows",
            value=borrowed,
            period="current",
            source_name="DefiLlama protocol",
            source=source_url(url_path),
            notes=record["notes"],
        )
        time.sleep(0.1)

    try:
        stables = fetch_json("https://stablecoins.llama.fi/stablecoins")
        stable_assets = stables.get("peggedAssets", [])
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"Stablecoin supplies unavailable: {exc.__class__.__name__}")
        stable_assets = []

    for asset in stable_assets:
        record = STABLECOIN_RECORDS.get(asset.get("symbol"))
        if not record:
            continue
        circulating = (asset.get("circulating") or {}).get("peggedUSD")
        append_row(
            metric_rows,
            record=record,
            metric="Stablecoin Supply",
            value=circulating,
            period="current",
            source_name="DefiLlama stablecoins",
            source="https://stablecoins.llama.fi/stablecoins",
            notes=record["notes"],
        )

    try:
        pools = fetch_json("https://yields.llama.fi/pools").get("data", [])
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"Yield pool APYs unavailable: {exc.__class__.__name__}")
        pools = []

    for record in YIELD_POOL_RECORDS:
        matches = [pool for pool in pools if pool.get("symbol") == record["symbol"]]
        if not matches:
            warnings.append(f"Current APY missing for {record['record']}")
            continue
        best = max(matches, key=lambda pool: pool.get("tvlUsd") or 0)
        append_row(
            metric_rows,
            record=record,
            metric="Current APY",
            value=best.get("apy"),
            unit="%",
            period="current",
            source_name="DefiLlama yields",
            source="https://yields.llama.fi/pools",
            notes=record["notes"],
        )

    append_market_rows(metric_rows, warnings)
    append_dune_active_wallet_rows(metric_rows, warnings)

    metric_rows.sort(key=lambda row: (row["metric"], -row["value"], row["project"], row["record"]))
    return metric_rows, warnings


def write_outputs(rows: list[dict[str, Any]], warnings: list[str], history: dict[str, Any] | None = None) -> None:
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    LAST_GOOD_DIR.mkdir(parents=True, exist_ok=True)

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

    today = date.today().isoformat()
    metadata = {
        "generated_at": today,
        "row_count": len(rows),
        "warnings": warnings,
        "source_note": "Generated from public DefiLlama endpoints; review methodology before final citation.",
        "refresh_status": "fresh",
        "last_known_good": today,
    }

    csv_text_path = DASHBOARD_DIR / ".generated-dashboard-data.csv.tmp"
    js_text_path = DASHBOARD_DIR / ".generated-dashboard-data.js.tmp"

    with csv_text_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    js = (
        "// Generated by scripts/refresh_dashboard_data.py. Do not edit by hand.\n"
        f"window.dashboardMeta = {json.dumps(metadata, indent=2)};\n"
        f"window.dashboardRows = {json.dumps(rows, indent=2)};\n"
        + (f"window.dashboardAggregateHistory = {json.dumps(history)};\n" if history else "")
    )
    js_text_path.write_text(js)

    shutil.move(str(csv_text_path), DATA_CSV)
    shutil.move(str(js_text_path), DATA_JS)

    snapshot_prefix = SNAPSHOT_DIR / f"dashboard-data-{today}"
    shutil.copy2(DATA_CSV, snapshot_prefix.with_suffix(".csv"))
    shutil.copy2(DATA_JS, snapshot_prefix.with_suffix(".js"))
    shutil.copy2(DATA_CSV, LAST_GOOD_CSV)
    shutil.copy2(DATA_JS, LAST_GOOD_JS)


def row_count_from_csv(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open(newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def seed_last_good() -> None:
    if LAST_GOOD_JS.exists() and LAST_GOOD_CSV.exists():
        return
    if not DATA_JS.exists() or not DATA_CSV.exists():
        return
    LAST_GOOD_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(DATA_JS, LAST_GOOD_JS)
    shutil.copy2(DATA_CSV, LAST_GOOD_CSV)


def restore_last_good() -> bool:
    if not LAST_GOOD_JS.exists() or not LAST_GOOD_CSV.exists():
        return False
    shutil.copy2(LAST_GOOD_JS, DATA_JS)
    shutil.copy2(LAST_GOOD_CSV, DATA_CSV)
    return True


def validate_refresh(rows: list[dict[str, Any]], warnings: list[str]) -> list[str]:
    errors: list[str] = []
    if len(rows) < MIN_REFRESH_ROWS:
        errors.append(f"row count {len(rows)} is below DASHBOARD_MIN_ROWS={MIN_REFRESH_ROWS}")

    last_good_count = row_count_from_csv(LAST_GOOD_CSV)
    if last_good_count and len(rows) < last_good_count * MIN_LAST_GOOD_RATIO:
        errors.append(
            f"row count {len(rows)} is below {MIN_LAST_GOOD_RATIO:.0%} of last-known-good row count {last_good_count}"
        )

    required_metrics = {"TVL", "30D Fees", "30D Revenue"}
    present_metrics = {row["metric"] for row in rows}
    missing_metrics = sorted(required_metrics - present_metrics)
    if missing_metrics:
        errors.append(f"required metric families missing: {', '.join(missing_metrics)}")

    if len(warnings) >= int(os.environ.get("DASHBOARD_MAX_WARNINGS", "50")):
        errors.append(f"warning count {len(warnings)} is unexpectedly high")

    return errors


def collect_aggregate_history(warnings: list[str]) -> dict[str, Any] | None:
    """Sum daily TVL across all DeFi20 records and compare to all-DeFi TVL.

    Powers the welcome-page area charts. Failure is non-fatal: the page
    falls back to stat cards until history is available.
    """
    by_date: dict[int, float] = {}
    for record in RECORDS:
        try:
            detail = fetch_json(source_url(f"protocol/{record['protocol_slug']}"))
        except Exception:  # noqa: BLE001
            continue
        for point in detail.get("tvl") or []:
            ts = point.get("date")
            value = point.get("totalLiquidityUSD")
            if ts and value:
                by_date[int(ts)] = by_date.get(int(ts), 0.0) + float(value)
        time.sleep(0.1)
    if not by_date:
        warnings.append("Aggregate TVL history unavailable")
        return None

    try:
        all_defi = fetch_json("https://api.llama.fi/v2/historicalChainTvl")
        all_by_date = {int(p["date"]): float(p["tvl"]) for p in all_defi if p.get("tvl")}
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"All-DeFi TVL history unavailable: {exc.__class__.__name__}")
        all_by_date = {}

    market_context = {}
    try:
        headers = {}
        api_key = os.environ.get("COINGECKO_DEMO_API_KEY")
        if api_key:
            headers["x-cg-demo-api-key"] = api_key
        global_data = (fetch_json("https://api.coingecko.com/api/v3/global", headers=headers) or {}).get("data", {})
        total_mcap = (global_data.get("total_market_cap") or {}).get("usd")
        btc_share = (global_data.get("market_cap_percentage") or {}).get("btc")
        if total_mcap and btc_share:
            btc_mcap = total_mcap * btc_share / 100.0
            market_context = {
                "total_market_cap": round(total_mcap, 2),
                "btc_market_cap": round(btc_mcap, 2),
                "altcoin_market_cap": round(total_mcap - btc_mcap, 2),
            }
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"Global market context unavailable: {exc.__class__.__name__}")

    # Daily market-cap history: Bitcoin plus the summed DeFi20 tokens, for the
    # price-based market-share series on the welcome page.
    btc_mcap_by_date: dict[str, float] = {}
    defi20_mcap_by_date: dict[str, float] = {}
    api_key = os.environ.get("COINGECKO_DEMO_API_KEY")
    if api_key:
        cg_headers = {"x-cg-demo-api-key": api_key}

        def mcap_chart(coin_id: str) -> dict[str, float]:
            data = fetch_json(
                f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=365&interval=daily",
                headers=cg_headers,
            )
            out: dict[str, float] = {}
            for point in data.get("market_caps") or []:
                if len(point) == 2 and point[1]:
                    out[date.fromtimestamp(point[0] / 1000).isoformat()] = float(point[1])
            return out

        try:
            btc_mcap_by_date = mcap_chart("bitcoin")
        except Exception as exc:  # noqa: BLE001
            warnings.append(f"Bitcoin mcap history unavailable: {exc.__class__.__name__}")
        token_ids = sorted({
            row["coingecko_id"] for row in read_token_map()
            if row.get("coingecko_id") and row.get("status") == "verified_search"
        })
        for coin_id in token_ids:
            try:
                for day, value in mcap_chart(coin_id).items():
                    defi20_mcap_by_date[day] = defi20_mcap_by_date.get(day, 0.0) + value
            except Exception:  # noqa: BLE001
                warnings.append(f"Mcap history missing for {coin_id}")
            time.sleep(2)
    else:
        warnings.append("Market-cap history skipped: set COINGECKO_DEMO_API_KEY")

    dates = sorted(by_date)[-365:]
    iso_dates = [date.fromtimestamp(ts).isoformat() for ts in dates]
    return {
        "market_context": market_context,
        "defi20_mcap": [round(defi20_mcap_by_date.get(d, 0), 2) for d in iso_dates],
        "btc_mcap": [round(btc_mcap_by_date.get(d, 0), 2) for d in iso_dates],
        "dates": iso_dates,
        "defi20_tvl": [round(by_date[ts], 2) for ts in dates],
        "all_defi_tvl": [round(all_by_date.get(ts, 0), 2) for ts in dates],
        "source": "DefiLlama protocol TVL histories summed across DeFi20 records; all-DeFi from historicalChainTvl.",
    }


def main() -> int:
    seed_last_good()

    try:
        rows, warnings = build_rows()
    except Exception as exc:  # noqa: BLE001 - preserve last-known-good files on refresh failure.
        restored = restore_last_good()
        print(f"Dashboard refresh failed: {exc.__class__.__name__}: {exc}", file=sys.stderr)
        if restored:
            print("Restored last-known-good dashboard data.", file=sys.stderr)
        return 1

    if not rows:
        restore_last_good()
        print("No dashboard rows generated.", file=sys.stderr)
        return 1

    validation_errors = validate_refresh(rows, warnings)
    if validation_errors:
        restored = restore_last_good()
        print("Dashboard refresh validation failed:", file=sys.stderr)
        for error in validation_errors:
            print(f"- {error}", file=sys.stderr)
        if restored:
            print("Restored last-known-good dashboard data.", file=sys.stderr)
        return 1

    write_outputs(rows, warnings, collect_aggregate_history(warnings))
    print(f"Wrote {len(rows)} rows to {DATA_CSV}")
    print(f"Wrote {DATA_JS}")
    print(f"Wrote dated snapshots to {SNAPSHOT_DIR}")
    print(f"Updated last-known-good data in {LAST_GOOD_DIR}")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
