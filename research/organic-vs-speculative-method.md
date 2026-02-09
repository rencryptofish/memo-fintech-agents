# Organic vs Speculative Flow Method

Last updated: 2026-02-09

## Objective

Create a reproducible split of x402 payment activity into:

1. `organic`: utility-driven API/service payments.
2. `speculative`: meme, wash-like, or clearly non-service market activity.
3. `unknown`: cannot be confidently labeled.

## Classification Rules

### Label `organic`

All conditions must hold:

1. Counterparty maps to a known service endpoint or facilitator route with documented API/service utility.
2. Payment size and cadence fit stated service pricing models.
3. Repeated payer-payee behavior reflects service consumption rather than cyclic churn.

### Label `speculative`

Any one condition is sufficient:

1. Token-centric churn with no service linkage.
2. High-frequency reciprocal transfers among clustered addresses with no service metadata.
3. Activity spikes tied to hype cycles where price/volume dislocate from service adoption.

### Label `unknown`

Use when:

1. Address labeling is incomplete.
2. Off-chain context is unavailable.
3. Pattern confidence is below threshold.

## Scoring Model

For each flow cluster:

- `service_link_score` (0-1)
- `behavioral_fit_score` (0-1)
- `counterparty_reliability_score` (0-1)

Labeling thresholds:

- `organic` if weighted score >= 0.70
- `speculative` if weighted score <= 0.35
- otherwise `unknown`

Default weights:

- `service_link_score`: 0.45
- `behavioral_fit_score`: 0.35
- `counterparty_reliability_score`: 0.20

## Current Limitation

The current weekly series is partially inferred from memo-era claims (for example, "organic ~4%" around mid-January 2026) and is not yet fully grounded in publicly reproducible labeled transaction sets. Treat the initial file as a working baseline with mixed confidence.

## Immediate Upgrade Path

1. Publish exact query IDs for all sampled on-chain pulls.
2. Version the counterparty labeling dictionary.
3. Add per-week `coverage_ratio` and `unknown_share` to avoid false precision.
