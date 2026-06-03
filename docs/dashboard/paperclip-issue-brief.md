# Paperclip Issue Brief: Machines & Money Dashboard Discovery

Date: 2026-06-02

## Suggested Title

Build Machines & Money dashboard discovery and MVP spec

## Context

Ian provided a broad dashboard outline covering cross-project metrics, sector comparisons, and project-specific charts across DeFi, tokenized assets, derivatives, lending, asset management, infra, and AI.

The outline is enough to begin discovery, but not enough to build the full dashboard directly. The next step is to map requested metrics to real data sources, identify which metrics are reliable enough for Machines & Money research, and define a narrow MVP.

## Goal

Create the first dashboard planning layer:

- metric inventory,
- source discovery plan,
- MVP dashboard spec,
- and an implementation-ready first slice.

## Deliverables

- `docs/dashboard/ian-outline-analysis.md`
- `docs/dashboard/mvp-spec.md`
- `docs/dashboard/metric-inventory.csv`
- `docs/dashboard/source-discovery-plan.md`
- `docs/dashboard/starter-source-map.csv`
- `docs/dashboard/source-check-notes.md`
- `docs/dashboard/sample-protocol-tvl-2026-06-02.csv`
- `docs/dashboard/prototype.html`
- `docs/dashboard/generated-dashboard-data.csv`
- `docs/dashboard/generated-dashboard-data.js`
- `docs/dashboard/runbook.md`
- `docs/dashboard/here-now.md`
- `scripts/refresh_dashboard_data.py`

## Acceptance Criteria

- Ian's outline is translated into an organized metric inventory.
- Each metric has a priority, likely source, source relationship, and availability status.
- MVP scope is narrowed to a first project universe, first sectors, global controls, and first views.
- Source discovery rules match Machines & Money research standards.
- The work avoids building unverified charts before source reliability is known.
- The first public source map identifies starter-project source splits and aggregation risks.
- A real-shaped sample TVL dataset exists for the first prototype.
- A static dashboard prototype can be opened locally for Ian review.
- The prototype has a repeatable public-source refresh path and supports TVL, fees, revenue, and DEX volume where available.

## Notes

Paperclip is reachable at the configured `mattmini` endpoint, but direct project writes require authenticated access in this session. This brief can be used to create or update the live issue manually if needed.
