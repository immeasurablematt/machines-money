# T001 Scout Gap Map

## Summary

The free dashboard has a clear public-facing shell and the free/pro boundary is currently preserved. `docs/dashboard/free.html` is the only dashboard implementation file with a diff; `docs/dashboard/prototype.html` has no diff.

The highest-leverage next slice is to expose source/caveat/freshness information inside the free dashboard UI, using data already present in `generated-dashboard-data.js`.

## Evidence

- `docs/dashboard/free-dashboard-production-plan.md` defines the free dashboard as the production surface and explicitly keeps `docs/dashboard/prototype.html` separate.
- `docs/dashboard/free.html` already has the main public IA: nav, first viewport, summary stats, category map, interactive chart controls, leaderboard, source cards, and Beehiiv CTA.
- `docs/dashboard/generated-dashboard-data.js` exposes row-level `source_name`, `source`, `source_relationship`, `confidence`, `period`, and `notes`.
- `docs/dashboard/generated-dashboard-data.csv` currently has 137 rows, 20 projects, and metric families for token volume, FDV, market cap, TVL, token price, fees, revenue, DEX volume, and active wallets.
- Current data confidence is 119 high rows and 18 medium rows. All rows are third-party source rows.
- Current active-wallet coverage is sparse: 3 rows, all 7D.
- `docs/dashboard/runbook.md` explains refresh and source gaps, but it is still framed around the broader prototype rather than the free dashboard.

## Gap Map By Production-Plan Section

- Final information architecture: mostly present in `free.html`; category map was updated to Ian's taxonomy. Missing stronger source/caveat module connected to selected chart/table state.
- Free vs pro boundary: good. Free and pro are separate files, and `prototype.html` is unchanged.
- First-screen visitor journey: present, but the first viewport can do more to say what is trustworthy and what is directional.
- Category map and naming: present. Some categories are aspirational because current data has sparse or no rows for several Ian-specific metrics.
- Chart/timeframe model: present for current, 24H, 7D, and 30D. Missing 30D DEX volume in the metric selector even though generated data includes it. Growth/time-series charts are correctly deferred until historical snapshots exist.
- Data freshness and refresh workflow: visible snapshot date exists. Missing a clearer public freshness/cadence explanation and free-dashboard-specific runbook copy.
- Source/caveat system: biggest gap. Data contains source and confidence fields, but the public UI only shows generic source cards and a usage caveat.
- Newsletter CTA and social-sharing loop: Beehiiv CTA is present. Chart-angle cards exist. Missing share controls/tracking hooks.
- Mobile readiness: CSS has responsive rules. Needs browser walkthrough after Worker changes.
- Analytics/tracking: not implemented. Should be lightweight and not block first source/caveat slice.
- Hosting/permanent URL: documented in plan, not implemented. Needs separate deployment/handoff task.
- QA checklist: partially verified by HTTP checks in the prior prep turn; needs full walkthrough after implementation.

## Verification Commands And Walkthrough Approach

- Start local dashboard server from `docs/dashboard`: `python3 -m http.server 8765`.
- Check load: `curl -I http://127.0.0.1:8765/free.html` and `curl -I http://127.0.0.1:8765/generated-dashboard-data.js`.
- Walk through `free.html`:
  - category cards,
  - timeframe buttons,
  - metric buttons,
  - sector filter,
  - table sorting,
  - Beehiiv CTA href,
  - mobile viewport readability.
- Confirm `git diff -- docs/dashboard/prototype.html` is empty.
- Check GoalBuddy board with `node /Users/mbaggetta/.codex/plugins/cache/goalbuddy/goalbuddy/0.3.8/skills/goalbuddy/scripts/check-goal-state.mjs docs/goals/free-dashboard-production-ready/state.yaml`.

## Ranked Safe Implementation Slices

1. Add selected-metric source/caveat/freshness visibility to `docs/dashboard/free.html`, including confidence counts, source names, period, source relationship, and notes from generated rows.
2. Add the missing `30D DEX Volume` metric to the 30D chart selector because it already exists in generated data.
3. Add source/caveat columns or expandable details to the public table without overcrowding mobile.
4. Add lightweight share/CTA tracking hooks or data attributes, deferring analytics vendor choice.
5. Update `docs/dashboard/free-dashboard.md` and `docs/dashboard/runbook.md` so the refresh/review instructions are explicitly free-dashboard-aware.
6. Create deployment/permanent URL handoff once hosting credentials/path are known.

## Recommended First Worker Package

Objective: Improve `docs/dashboard/free.html` source/caveat visibility and current metric coverage without touching `docs/dashboard/prototype.html`.

Allowed files:

- `docs/dashboard/free.html`

Verify:

- Serve the dashboard locally and confirm `free.html` plus `generated-dashboard-data.js` load.
- Exercise metric/timeframe/category/sector controls.
- Confirm selected-metric source/caveat summary updates when controls change.
- Confirm Beehiiv CTA href remains `https://machinesandmoney.beehiiv.com`.
- Confirm `git diff -- docs/dashboard/prototype.html` is empty.

Stop if:

- The implementation needs data schema changes in generated files.
- The implementation needs edits to `docs/dashboard/prototype.html`.
- Browser verification cannot run and no HTTP/static fallback is available.
