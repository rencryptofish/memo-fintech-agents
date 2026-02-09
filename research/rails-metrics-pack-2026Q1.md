# Rails Metrics Pack (FedNow, RTP, Related)

Last verified: 2026-02-09

## FedNow (Federal Reserve Financial Services)

| Metric | Value | Date Context | Source | Confidence |
| --- | --- | --- | --- | --- |
| Annual transactions | 8.4 million | 2025 full-year | https://www.frbservices.org/resources/financial-services/fednow/volume-value-stats | high |
| Annual value | $853 billion | 2025 full-year | https://www.frbservices.org/resources/financial-services/fednow/volume-value-stats | high |
| Q4 transactions | Over 1 million | Q4 2025 | https://www.frbservices.org/resources/financial-services/fednow/volume-value-stats | high |
| Q4 value | Over $40 billion | Q4 2025 | https://www.frbservices.org/resources/financial-services/fednow/volume-value-stats | high |
| Participating financial institutions | Over 1,500 | Dec 4, 2025 communication | https://www.frbservices.org/news/communications/120425-general-announcing-2026-fees | high |
| Participation growth vs prior year | 44% increase | Dec 4, 2025 communication | https://www.frbservices.org/news/communications/120425-general-announcing-2026-fees | high |
| Network transaction limit | Increased from $1M to $10M | 2025 reflection item | https://www.frbservices.org/news/communications/120425-general-announcing-2026-fees | high |

## RTP (The Clearing House)

| Metric | Value | Date Context | Source | Confidence |
| --- | --- | --- | --- | --- |
| Cumulative value milestone | Surpassed $1 trillion cumulative payments | Through 2025 | https://www.theclearinghouse.org/payment-systems/articles/2026/01/rtp-growth-accelerates-in-2025-as-the-network-surpasses-1-trillion-in-cumulative-payments | high |
| Q4 transactions | 125 million | Q4 2025 | https://www.theclearinghouse.org/payment-systems/articles/2026/01/rtp-growth-accelerates-in-2025-as-the-network-surpasses-1-trillion-in-cumulative-payments | high |
| Q4 value | $405 billion | Q4 2025 | https://www.theclearinghouse.org/payment-systems/articles/2026/01/rtp-growth-accelerates-in-2025-as-the-network-surpasses-1-trillion-in-cumulative-payments | high |
| Participating financial institutions | Over 1,130 | 2025 | https://www.theclearinghouse.org/payment-systems/articles/2026/01/rtp-growth-accelerates-in-2025-as-the-network-surpasses-1-trillion-in-cumulative-payments | high |

## ACH (Nacha)

| Metric | Value | Date Context | Source | Confidence |
| --- | --- | --- | --- | --- |
| Annual transactions | 33.6 billion | 2025 full-year | https://www.nacha.org/news/new-ach-network-records-set-2025 | high |
| Annual value | $86.2 trillion | 2025 full-year | https://www.nacha.org/news/new-ach-network-records-set-2025 | high |
| Same Day ACH transactions | 1.3 billion | 2025 full-year | https://www.nacha.org/news/new-ach-network-records-set-2025 | high |
| Same Day ACH value | $3.5 trillion | 2025 full-year | https://www.nacha.org/news/new-ach-network-records-set-2025 | high |

## Gaps To Close

1. Build a comparable denominator between FedNow and RTP (active senders/receivers, transaction composition, and average ticket size).
2. Add card push-to-card and wire benchmarks for full multi-rail routing economics.
3. Archive quarterly snapshots of source pages to reduce link-rot and restatement risk.

## Suggested Canonical Fields

- `rail`
- `period`
- `txn_count`
- `txn_value_usd`
- `active_participants`
- `limit_policy`
- `source_url`
- `last_verified`
- `confidence`
