# machinesandmoney.xyz redirect

This directory is a tiny Cloudflare Pages site whose only job is to redirect
`machinesandmoney.xyz` traffic to:

https://machinesandmoney.beehiiv.com/

It is intentionally separate from the free dashboard deployment so the branded
domain can forward to Beehiiv without changing the dashboard at
`machines-money`.

## Cloudflare setup

1. Deploy this directory with the `Deploy machinesandmoney.xyz Redirect` GitHub
   Actions workflow. The workflow tries to create the Cloudflare Pages project
   named `machinesandmoney-xyz` if it does not already exist.
2. In Cloudflare Pages, add both custom domains to the `machinesandmoney-xyz`
   project:
   - `machinesandmoney.xyz`
   - `www.machinesandmoney.xyz`
3. At the domain registrar, point the domain DNS to Cloudflare. If the registrar
   keeps DNS hosting, use its equivalent `CNAME`/`ALIAS` records for the Pages
   custom-domain target Cloudflare provides.

Once DNS finishes propagating, both the apex domain and `www` should return a
permanent redirect to Beehiiv.
