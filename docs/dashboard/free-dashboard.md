# Machines & Money Free Dashboard

This is a separate public-facing dashboard surface from `prototype.html`.

## Why It Is Separate

- `prototype.html` is the broader research/pro dashboard prototype.
- `free.html` is the smaller audience-growth dashboard for public sharing, social chart posts, and newsletter subscriber acquisition.
- Both can reuse `generated-dashboard-data.js`, but the UI and product intent are different.

## Free Dashboard Goal

Help crypto, TradFi, and Web2 readers quickly understand the fundamental reality of major crypto platforms:

- Which projects are largest
- Which products have meaningful TVL
- Which projects generate fees or revenue
- Where usage data is available
- Which chart angles are useful for newsletter and social posts

The free dashboard should make non-subscribers want the regular Machines & Money fundamentals series, and make subscribers more likely to keep returning for chart-filled issues.

## Design Direction

The free dashboard should borrow the useful product patterns Ian likes from `hl.eco`:

- Interactive chart controls instead of static screenshots
- Flexible timeframe navigation, starting with current, 24H, 7D, and 30D cuts
- A clean category map near the top that is educational on its own
- Visible data freshness and source caveats so the public chart can be trusted

The current prototype uses the generated public-data snapshot. Continuous updating will require a scheduled refresh/deploy path later; the UI is structured to make that status visible.

## Current Entry Point

Open `docs/dashboard/free.html`.

## Production Readiness Notes

The production lane should now be reviewed as the free public dashboard, not as the broader prototype:

- `free.html` is the public page to polish, QA, and eventually host.
- `prototype.html` remains the broader/pro research prototype and should stay untouched unless that separate product is being worked on.
- `generated-dashboard-data.js` is still the shared data snapshot, so visible source caveats and freshness copy matter.
- The public CTA target is `https://machinesandmoney.beehiiv.com`.

Before public launch, verify:

- category, timeframe, metric, sector, and sort controls work,
- source confidence and caveats update with the selected metric,
- the dashboard is readable on mobile,
- share and subscribe actions are visible,
- the page has a permanent public URL rather than an expiring preview.
