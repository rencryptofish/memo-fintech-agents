# M&A Verification Ledger

Last verified: 2026-02-09

## Status Definitions

- `official`: confirmed by acquirer/target primary release.
- `credible_report`: reported by established financial/industry media but no definitive filing/release located.
- `unverified`: claim present in memo discourse but no reliable primary or strong secondary confirmation found.

## Ledger

| Deal | Claimed Value | Verification Status | Last Verified | Primary Source | Confidence | Action |
| --- | --- | --- | --- | --- | --- | --- |
| Stripe -> Bridge | $1.1B | official | 2026-02-09 | https://stripe.com/newsroom/news/stripe-agrees-to-acquire-bridge | high | Keep as confirmed |
| Xero -> Melio | Up to $2.5B | official | 2026-02-09 | https://www.xero.com/us/media-releases/xero-to-acquire-melio/ | high | Keep as confirmed |
| Capital One -> Brex | $5.15B | official | 2026-02-09 | https://www.capitalone.com/about/newsroom/capital-one-to-acquire-brex/ | high | Keep as confirmed; monitor close |
| Mastercard -> Zero Hash | $1.5B-$2B (talks) | credible_report | 2026-02-09 | https://www.coindesk.com/business/2025/12/10/mastercard-in-talks-to-acquire-crypto-infrastructure-firm-zero-hash-sources | medium | Treat as rumor until filing/press release |
| Coinbase -> BVNK | ~$2B (explored) | credible_report | 2026-02-09 | https://www.finextra.com/newsarticle/46057/coinbase-reportedly-tried-to-buy-stablecoin-startup-bvnk-for-2bn | low | Do not use as base-case signal |
| Mastercard -> Zero Hash (definitive close) | n/a | unverified | 2026-02-09 | n/a | low | Remove any "is acquiring" wording in downstream memos |
| Coinbase -> BVNK (signed transaction) | n/a | unverified | 2026-02-09 | n/a | low | Keep as "reportedly explored" only |

## Editorial Rule

For investment memos, only `official` deals can be used in base-case market-structure inference. `credible_report` can be mentioned in watchlists. `unverified` should be excluded from valuation logic.
