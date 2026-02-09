# Parallel Diligence Pack: Where We Need More Data

Date: 2026-02-09  
Scope: All memos in `memos/`

## 1) Executive readout

The memos are directionally strong but data-fragile in the same places:

1. Repeated protocol/market claims with low traceability.
2. Multiple high-impact figures that look stale or internally inconsistent.
3. Heavy reliance on estimates/interpolation in source datasets.

Most useful next step is not more narrative work. It is a parallel evidence pass that normalizes KPIs, validates key claims, and downgrades rumor-level items.

## 2) Quant snapshot (claim density vs source density)

| Memo | Lines | Numeric lines | Source-marker lines | Assumption-marker lines |
| --- | ---: | ---: | ---: | ---: |
| `memos/agent-economy-memo.md` | 713 | 364 | 19 | 25 |
| `memos/agent-fintech-intersection-deep-dive.md` | 495 | 212 | 1 | 1 |
| `memos/fintech-agents-intersection.md` | 412 | 146 | 4 | 11 |
| `memos/fintech-investment-opportunities-2026.md` | 323 | 128 | 3 | 8 |
| `memos/fintech-market-analysis.md` | 551 | 266 | 5 | 8 |
| `memos/investment-committee-memo-agent-fintech-infrastructure-2026-02-09.md` | 71 | 30 | 0 | 2 |
| `memos/investment-opportunities.md` | 387 | 134 | 6 | 8 |
| `memos/x402-research-memo.md` | 269 | 114 | 9 | 7 |
| `memos/x402-value-capture-analysis.md` | 504 | 189 | 8 | 10 |

Interpretation: the largest diligence lift comes from source hardening, not additional ideation.

## 3) Highest-priority data gaps (P0)

### P0-A: Canonical x402 KPI reconciliation

Evidence:
- `memos/x402-research-memo.md:10`
- `memos/x402-research-memo.md:103`
- `memos/x402-value-capture-analysis.md:26`
- `memos/agent-fintech-intersection-deep-dive.md:19`
- `memos/fintech-agents-intersection.md:57`
- `memos/investment-committee-memo-agent-fintech-infrastructure-2026-02-09.md:17`

Issue:
- Same headline metrics are repeated across memos (`157.6M` tx / `$600M+` volume), but those values need timestamped reconciliation against current primary counters and on-chain data.
- A current homepage snapshot check (2026-02-09) returned materially different counters (`75.41M` tx, `$24.24M` volume, `94.06K` buyers, `22K` sellers), confirming the need for a canonical source-of-truth table.

Data to collect:
1. Daily time series by chain: tx count, payment volume, active buyers/sellers.
2. Metric definitions: what qualifies as a transaction and volume event.
3. One canonical KPI table with `as_of_date`.

Primary sources:
- x402 official site counters
- Dune query IDs / on-chain dashboards
- Coinbase/x402 docs and release notes

Deliverable:
- `data/x402_kpi_canonical.csv`
- `research/source-registry.md` entry for each KPI

---

### P0-B: Organic vs speculative flow split

Evidence:
- `memos/agent-fintech-intersection-deep-dive.md:19`
- `memos/agent-fintech-intersection-deep-dive.md:181`
- `memos/agent-fintech-intersection-deep-dive.md:208`
- `memos/investment-opportunities.md:348`
- `memos/investment-committee-memo-agent-fintech-infrastructure-2026-02-09.md:65`

Issue:
- “~4% organic” is investment-critical and repeated, but methodology is not explicit.

Data to collect:
1. Classification rules for organic/speculative.
2. Labeled sample of top counterparties and flow types.
3. Weekly trendline of organic share.

Primary sources:
- On-chain labels / Dune entity tagging
- Protocol ecosystem registry of live services
- Facilitator-level reports where available

Deliverable:
- `research/organic-vs-speculative-method.md`
- `data/x402_organic_share_weekly.csv`

---

### P0-C: Protocol traction scoreboard beyond x402

Evidence:
- `memos/agent-fintech-intersection-deep-dive.md:181`
- `memos/agent-fintech-intersection-deep-dive.md:182`
- `memos/agent-fintech-intersection-deep-dive.md:183`
- `memos/agent-fintech-intersection-deep-dive.md:184`
- `memos/fintech-agents-intersection.md:53`
- `memos/fintech-agents-intersection.md:57`

Issue:
- ACP/AP2/TAP/Agent Pay/Agent Ready are compared, but production transaction evidence is uneven and often qualitative.

Data to collect:
1. Standard schema per protocol: launch date, pilot vs GA, disclosed volume, active partners, live merchants.
2. “Enabled distribution” vs “actual usage” distinction.

Primary sources:
- Official press releases / docs (Stripe, Google, Visa, Mastercard, PayPal)
- Public sandbox/partner lists with dates

Deliverable:
- `research/protocol-scoreboard-2026Q1.md` (with confidence tags)

---

### P0-D: M&A and valuation rumor cleanup

Evidence:
- `memos/fintech-investment-opportunities-2026.md:82`
- `memos/fintech-investment-opportunities-2026.md:88`
- `memos/fintech-investment-opportunities-2026.md:99`
- `memos/investment-opportunities.md:294`
- `memos/investment-opportunities.md:296`
- `memos/agent-fintech-intersection-deep-dive.md:250`

Issue:
- Several claims are “reportedly / pending” but used as directional anchors.

Data to collect:
1. Verification status for each deal: `official`, `credible-report`, `unverified`.
2. Last-verified date and primary URL.
3. If unverified, replace with neutral wording.

Primary sources:
- Acquirer press rooms
- SEC 8-K / filings
- Top-tier financial reporting (only if no primary filing exists)

Deliverable:
- `research/mna-verification-ledger.md`

---

### P0-E: Regulatory timeline hardening (US-first)

Evidence:
- `memos/fintech-investment-opportunities-2026.md:60`
- `memos/fintech-agents-intersection.md:248`
- `memos/agent-fintech-intersection-deep-dive.md:438`
- `memos/investment-opportunities.md:355`

Issue:
- GENIUS/FDIC/SEC timing and “effective date” statements are core to theses, but need precise status labeling (enacted/proposed/comment period/effective).

Data to collect:
1. Statute/rule status matrix with exact dates.
2. Impact mapping to memo recommendations.
3. Trigger list for revisions when rules move.

Primary sources:
- Congress / federal register / agency pages
- SEC exam priorities PDFs
- FDIC notice pages

Deliverable:
- `research/regulatory-tracker-us-2026.md`

## 4) Secondary data gaps (P1)

### P1-A: FedNow adoption and throughput normalization

Evidence:
- `memos/fintech-investment-opportunities-2026.md:107`
- `memos/fintech-investment-opportunities-2026.md:111`
- `memos/fintech-market-analysis.md:104`

Need:
- One source-of-truth table for institutions, transactions, and growth periods with consistent denominators.

### P1-B: CFO stack funding and company KPI refresh

Evidence:
- `memos/fintech-investment-opportunities-2026.md:145`
- `memos/investment-opportunities.md:18`
- `memos/fintech-agents-intersection.md:91`

Need:
- Quarterly refresh pack for funding/ARR/valuation claims (Ramp, Brex, Mercury, etc.) with primary references only.

### P1-C: Market-size stack harmonization

Evidence:
- `memos/agent-economy-memo.md:14`
- `memos/fintech-market-analysis.md:26`

Need:
- Reconcile competing TAM/CAGR numbers and document range logic, base year, and market definition.

## 5) Memo-by-memo: where more data is most useful

### `memos/agent-economy-memo.md`
1. Replace broad multi-source forecast claims with a range table keyed to explicit definitions and dates (`memos/agent-economy-memo.md:14`, `memos/agent-economy-memo.md:16`).
2. Add primary-source backing for top ARR/valuation claims in market map sections (`memos/agent-economy-memo.md:167`, `memos/agent-economy-memo.md:170`).
3. Keep “industry estimate” flags where no primary study exists (`memos/agent-economy-memo.md:525`).

### `memos/fintech-market-analysis.md`
1. Tighten macro market sizing and profitability stats to one reconciled source set (`memos/fintech-market-analysis.md:26`).
2. Verify FedNow figures and growth percentages with dated releases (`memos/fintech-market-analysis.md:104`).
3. Re-check 2024-2026 funding/recovery numbers quarterly (`memos/fintech-market-analysis.md:330`).

### `memos/fintech-investment-opportunities-2026.md`
1. Convert M&A rumor claims to confidence-tagged entries (`memos/fintech-investment-opportunities-2026.md:82`, `memos/fintech-investment-opportunities-2026.md:88`).
2. Re-verify GENIUS legal-status language and implementation timeline (`memos/fintech-investment-opportunities-2026.md:60`).
3. Normalize FedNow and Treasury usage claims to current official statements (`memos/fintech-investment-opportunities-2026.md:107`, `memos/fintech-investment-opportunities-2026.md:111`).

### `memos/fintech-agents-intersection.md`
1. Reconcile protocol volume/partner claims across x402/AP2/TAP/Agent Pay (`memos/fintech-agents-intersection.md:53`).
2. Validate regulatory framing with concrete status labels (`memos/fintech-agents-intersection.md:247`, `memos/fintech-agents-intersection.md:248`).
3. Confirm CFO stack funding metric and period definition (`memos/fintech-agents-intersection.md:91`).

### `memos/agent-fintech-intersection-deep-dive.md`
1. Hard-verify the core “157.6M / $600M / 4% organic” chain because it drives multiple recommendations (`memos/agent-fintech-intersection-deep-dive.md:19`, `memos/agent-fintech-intersection-deep-dive.md:181`).
2. Recompute developer funnel and supply bottleneck metrics from reproducible source pulls (`memos/agent-fintech-intersection-deep-dive.md:210`).
3. De-risk rumor-level corporate activity claims (`memos/agent-fintech-intersection-deep-dive.md:250`).

### `memos/investment-opportunities.md`
1. Replace pending M&A items with verified-status ledger links (`memos/investment-opportunities.md:294`, `memos/investment-opportunities.md:296`).
2. Attach data-source appendix to all Tier 1 conviction stats (`memos/investment-opportunities.md:18`, `memos/investment-opportunities.md:89`).
3. Track x402 organic-volume trigger monthly (`memos/investment-opportunities.md:348`).

### `memos/x402-research-memo.md`
1. Refresh headline metrics with timestamp + source IDs (`memos/x402-research-memo.md:10`, `memos/x402-research-memo.md:103`).
2. Quantify the “90% drop” with exact windows and denominator (`memos/x402-research-memo.md:128`).
3. Replace broad source bucket with per-claim citations (`memos/x402-research-memo.md:269`).

### `memos/x402-value-capture-analysis.md`
1. Separate measured data from modeled assumptions in every chart section (`memos/x402-value-capture-analysis.md:26`, `memos/x402-value-capture-analysis.md:504`).
2. Validate bottleneck metrics (53:1, 0.6% conversion) with refreshed query pulls (`memos/x402-value-capture-analysis.md:73`, `memos/x402-value-capture-analysis.md:472`).
3. Add confidence grades to forecast scenarios (`memos/x402-value-capture-analysis.md:431`).

### `memos/investment-committee-memo-agent-fintech-infrastructure-2026-02-09.md`
1. Add explicit links to source tables for all decision-critical figures (`memos/investment-committee-memo-agent-fintech-infrastructure-2026-02-09.md:17`).
2. Keep a tracked risk item for estimate-heavy datasets (`memos/investment-committee-memo-agent-fintech-infrastructure-2026-02-09.md:56`).

## 6) Supporting data-file risk flags

### `data/x402_data.py`
- Contains many explicit estimated points (`est.`), synthetic trajectory values, and mixed-quality sources; needs a confidence field per row.

### `data/fintech_funding_data.py`
- Uses interpolation/derived assumptions by design; should not be treated as primary evidence without row-level confidence filtering.

## 7) Parallel execution plan (10 streams)

| Stream | Outcome | Priority | Cadence |
| --- | --- | --- | --- |
| 1. x402 KPI Canonicalization | Unified daily KPI table + definitions | P0 | Weekly |
| 2. Organic vs Speculative Split | Reproducible classifier + trendline | P0 | Weekly |
| 3. Protocol Scoreboard | ACP/AP2/TAP/Agent Pay/Agent Ready production tracker | P0 | Biweekly |
| 4. Regulatory Tracker | US status matrix (GENIUS/FDIC/SEC + dates) | P0 | On event + monthly |
| 5. M&A Verification Ledger | Official vs rumor status, last-verified timestamp | P0 | Weekly |
| 6. Public/Private KPI Refresh | CFO stack + key infra players | P1 | Monthly |
| 7. FedNow/RTP/Rail Metrics Pack | Consistent rail adoption table | P1 | Monthly |
| 8. Market Size Harmonization | TAM/CAGR range table by definition | P1 | Quarterly |
| 9. Memo Citation Backfill | Per-claim source IDs in high-impact sections | P0 | Sprint-based |
| 10. Data Governance | Source SLA, archive snapshot, confidence taxonomy | P0 | Continuous |

## 8) Immediate edits recommended (before sharing externally)

1. Downgrade unverified M&A statements to “unconfirmed” until primary confirmation.
2. Timestamp every protocol traction table with `as_of_date`.
3. Add a one-page “Data Quality Appendix” to every memo packet.
4. Link committee memo claims directly to canonical tables.

## 9) Definition of done

This diligence pass is complete when:

1. Every decision-critical numeric claim in Tier 1 theses maps to one primary source URL and last-verified date.
2. x402 metrics in all memos resolve to one canonical table.
3. Rumor-level items are explicitly labeled and excluded from base-case assumptions.
4. Regulatory timeline statements are date-specific and status-correct.
