# here.now Preview

## Current Free Dashboard Preview

Published: 2026-06-08

Live preview:

- https://marble-pocket-zz9d.here.now/

Notes:

- This is an anonymous here.now publish of the free dashboard bundle.
- It expires at approximately 2026-06-10T00:43:51Z unless claimed.
- The claim URL contains a token and is not stored in this repo.
- Published files:
  - `index.html` from `docs/dashboard/free.html`
  - `generated-dashboard-data.js`

Verification:

- `https://marble-pocket-zz9d.here.now/` returned HTTP 200.
- `https://marble-pocket-zz9d.here.now/generated-dashboard-data.js` returned HTTP 200.
- The live HTML contains the DeFi20 opportunity tracker copy, selected-metric source panel, Beehiiv CTA, and data script reference.

## Older Prototype Preview

Published: 2026-06-04

Live preview:

- https://whole-vault-9d9p.here.now/

Notes:

- This is an anonymous here.now publish created with the installed here.now skill.
- This publish expires roughly 24 hours after the most recent anonymous update unless claimed.
- The claim URL contains a token and is not stored in this repo.
- Local update state is stored in ignored `.herenow/state.json`.
- Published files:
  - `index.html`
  - `generated-dashboard-data.js`

## Prototype Preview Bundle

The 2026-06-04 preview was for the broader prototype dashboard.

To republish the broader prototype manually, bundle:

- `docs/dashboard/prototype.html` as `index.html`
- `docs/dashboard/generated-dashboard-data.js`

Then publish the two files through the here.now publish API or the here.now skill.

## Free Dashboard Preview Bundle

For the free public dashboard, do not reuse the prototype bundle.

Bundle:

- `docs/dashboard/free.html` as `index.html`
- `docs/dashboard/generated-dashboard-data.js`

The free dashboard preview should be treated as temporary unless the here.now URL is claimed or replaced with a permanent Machines & Money URL.

Before sharing any free-dashboard preview with Ian or using it in social posts:

- confirm `index.html` came from `docs/dashboard/free.html`,
- confirm `generated-dashboard-data.js` is included next to it,
- confirm the Beehiiv CTA points to `https://machinesandmoney.beehiiv.com`,
- confirm the selected-metric source/caveat panel is visible,
- confirm the URL will not expire before the review window.
