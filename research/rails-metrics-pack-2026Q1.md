# Rails Metrics Pack (FedNow, RTP, Related)

Last verified: 2026-02-09

## FedNow (Federal Reserve Financial Services)

| Metric | Value | Date Context | Source | Confidence |
| --- | --- | --- | --- | --- |
| Participating financial institutions | Over 1,500 | Dec 4, 2025 communication | https://www.frbservices.org/news/communications/120425-general-announcing-2026-fees | high |
| Participation growth vs prior year | 44% increase | Dec 4, 2025 communication | https://www.frbservices.org/news/communications/120425-general-announcing-2026-fees | high |
| Network transaction limit | Increased from $1M to $10M | 2025 reflection item | https://www.frbservices.org/news/communications/120425-general-announcing-2026-fees | high |

## RTP (The Clearing House)

| Metric | Value | Date Context | Source | Confidence |
| --- | --- | --- | --- | --- |
| Annual transactions | 343 million | 2024 full-year | https://www.theclearinghouse.org/payment-systems/articles/2025/04/rtp-network-achieves-breakout-growth-in-2024 | high |
| Annual value | $246 billion | 2024 full-year | https://www.theclearinghouse.org/payment-systems/articles/2025/04/rtp-network-achieves-breakout-growth-in-2024 | high |
| Daily payment pace | Over 1.1 million payments/day | 2024 full-year context | https://www.theclearinghouse.org/payment-systems/articles/2025/04/rtp-network-achieves-breakout-growth-in-2024 | high |
| Annual tx growth | 16% YoY | 2024 full-year | https://www.theclearinghouse.org/payment-systems/articles/2025/04/rtp-network-achieves-breakout-growth-in-2024 | high |

## Gaps To Close

1. FedNow public transaction-count time series still needs a stable, current page with explicit counts.
2. Unified denominator between FedNow and RTP (institution count, active senders, and transaction composition) is not yet standardized.
3. Add ACH same-day and card push-to-card comparison rows for full multi-rail routing model.

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
