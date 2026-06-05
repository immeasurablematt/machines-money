# Dune Active Wallets Adapter

Date: 2026-06-04

This is the first Dune adapter for Ian's top post-market-data metric: active users/wallets.

## Current Scope

The first wired metric is:

- `7D Active Wallets`

Current coverage:

- Uniswap
- Curve
- Aerodrome

Source table:

- `dex.trades`

Definition:

`7D Active Wallets` counts distinct wallets that interacted with the protocol over the last 7 days.

For the current DEX implementation, that means distinct `tx_from` wallets in Dune's `dex.trades` table over the last 7 days, rolled up to one total per project across all supported chains.

This is a protocol-interaction wallet proxy for the covered DEX surface. It is not app visitors, governance participants, lenders, borrowers, or stablecoin holders.

## SQL

```sql
SELECT
  project,
  count(DISTINCT tx_from) AS active_wallets_7d
FROM dex.trades
WHERE block_time >= now() - interval '7' day
  AND lower(project) IN ('uniswap', 'curve', 'aerodrome')
GROUP BY 1
ORDER BY active_wallets_7d DESC
LIMIT 20
```

## Verification

Verified on 2026-06-04:

- Dune `SELECT 1` completed successfully through the standard Dune API.
- `DESCRIBE dex.trades` completed successfully.
- The starter active-wallet query completed successfully.

## Why This Is Narrow

Active users/wallets are not directly comparable across every project yet.

For example:

- DEX activity can use `dex.trades`.
- Lending activity needs lending-specific tables or project-native APIs.
- Stablecoin products need holders, minters/redeemers, or staking participants.
- Infrastructure projects need message senders, apps, or endpoint-specific users.

The dashboard should label the Dune metric as a wallet proxy until project-specific user definitions are mapped.

## Next Dune Work

1. Add saved Dune queries or stable SQL files for each metric family.
2. Map lending active wallets separately for Aave, Morpho, Euler, and Kamino.
3. Map stablecoin holder/staker activity for Sky, Ethena, Maple, and Falcon.
4. Map infrastructure activity for LayerZero and Canton.
5. Decide whether active wallets should be 7D, 30D, or both.
