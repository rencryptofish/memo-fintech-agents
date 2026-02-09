# Canonical Underwriting Assumptions (2026 Q1)

Use this as the single assumptions layer for decision memos.

Rules:
1. Requote headline metrics only from the canonical row for each assumption ID.
2. If a claim has `low` confidence, treat it as directional context, not a base-case input.
3. If a metric appears in multiple forms (for example, raw vs adjusted), keep the definition label with the number.

| Assumption ID | Canonical Value (As of Feb 9, 2026) | Confidence | Use Rule | Source Artifacts |
|---|---|---|---|---|
| CUA-001 | x402 homepage counters: **75.41M transactions**, **$24.24M volume** | High | Use for current-state traction framing. | `../data/x402_kpi_canonical.csv` |
| CUA-002 | x402 legacy claims: **157.6M / $600M+** | Low (conflict) | Keep as historical-context hypothesis only. Do not use in underwriting base case. | `../data/x402_kpi_canonical.csv`, `memo-citation-backfill-matrix.csv` |
| CUA-003 | Stablecoin scale: **$300B+ supply**, **~$46T raw annualized transfer volume**, **~$9T adjusted economic annualized volume** | Medium-High | Always include raw vs adjusted label when cited. | `rails-metrics-pack-2026Q1.md`, `market-size-harmonization-2026Q1.md` |
| CUA-004 | Rail migration anchor: **ACH $93T (2025)**, **RTP >$1T cumulative**, **FedNow 1,192 institutions / 1.5M transactions (2024 usage)** | High | Use for migration-speed comparisons, not growth marketing. | `rails-metrics-pack-2026Q1.md` |
| CUA-005 | FedNow distribution anchor: **~1,500+ institutions connected** | High | Use as network coverage context; pair with CUA-004 usage when discussing adoption. | `rails-metrics-pack-2026Q1.md` |
| CUA-006 | Fintech funding recovery: **$51.8B (2025)** with baseline-sensitive YoY (**+27% vs $40.8B; +19.4% vs $43.4B**) | Medium | Report trend direction with baseline sensitivity in the same sentence. | `market-size-harmonization-2026Q1.md` |
| CUA-007 | M&A treatment: official deals are base-case evidence; report-level deals are watchlist-only | High | Never anchor valuation cases to rumor-only items. | `mna-verification-ledger.md` |
| CUA-008 | 2030 scenario priors: **55/30/10/5** (Hybrid/Multi-rail/Crypto-first/Delayed) | Medium (subjective) | Treat as model priors and refresh quarterly. | `memos/agent-fintech-mental-models-end-states.md` |
| CUA-009 | Top-15 conviction composite: `0.60*Opportunity + 0.25*Readiness + 0.15*Evidence` | High (method) | Use tier gates from the scoring overlay before changing rankings. | `../data/investment_opportunity_conviction_overlay_2026Q1.csv` |
| CUA-010 | Milestone IDs `MS-001` through `MS-025` are the canonical watchlist keys | High | Update status in tracker before changing milestone text in memos. | `milestone-status-tracker.csv` |

Refresh cadence: weekly for `CUA-001/002`, monthly for `CUA-003/004/005/006`, quarterly for `CUA-008/009`, and event-driven for `CUA-007/010`.
