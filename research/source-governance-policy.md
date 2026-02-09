# Source Governance Policy

Version: 1.0  
Effective date: 2026-02-09

## Purpose

Ensure memo claims are traceable, refreshable, and confidence-scored before investment decisions.

## Mandatory Metadata for Every Decision-Critical Claim

1. `source_id`
2. `source_url`
3. `source_type` (`official`, `filing`, `credible_report`, `secondary`)
4. `last_verified_utc`
5. `confidence` (`high`, `medium`, `low`)
6. `status` (`supported`, `partial`, `conflict`, `unverified`)

## Freshness SLA

| Claim Class | Refresh SLA | Example |
| --- | --- | --- |
| Market prices / counters | 7 days | protocol counters, equity prices |
| Regulatory status | event-driven + 30 days | FDIC/SEC/Congress status |
| M&A status | 7 days until close/termination | pending transactions and rumors |
| Long-horizon TAM/CAGR | 90 days | market-size forecast tables |

## Confidence Rules

- `high`: direct primary-source support with clear wording.
- `medium`: primary source exists but evidence is indirect or incomplete.
- `low`: rumor, secondary aggregation, or unresolved contradiction.

## Contradiction Handling

If two high-visibility sources disagree:

1. Mark claim as `conflict`.
2. Exclude from base-case assumptions.
3. Add a dated reconciliation task with owner and deadline.

## Link Hygiene

1. Archive every external URL snapshot at first use.
2. Store archived copy hash and retrieval timestamp.
3. Flag 404/redirect changes on weekly validation runs.

## Editorial Guardrails for Memos

1. Rumor-level claims cannot be phrased as facts.
2. Any table mixing measured and estimated values must include a confidence column.
3. Committee memos must reference canonical data files, not copied static numbers.

## Operational Cadence

1. Weekly: run source-health check and M&A status check.
2. Monthly: refresh regulatory and rails trackers.
3. Quarterly: refresh TAM harmonization ranges.

## Minimum Release Gate (before external distribution)

1. 100% of Tier 1 numeric claims have source metadata.
2. No `low` confidence claim appears in the base-case model without explicit exception note.
3. Conflicting claims are labeled and isolated from valuation outputs.
