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
