# Market Size Harmonization (2026 Q1)

Last updated: 2026-02-09

## Why this exists

Memos use multiple TAM/CAGR figures sourced from different definitions. This file normalizes ranges and makes assumptions explicit.

## Harmonized Range Table

| Domain | Base Year | Low Case | Base Case | High Case | Notes |
| --- | --- | --- | --- | --- | --- |
| AI agent software market | 2025 | $7B | $8B | $10B | Definition-sensitive (tooling vs full stack) |
| AI agent market by 2030 | 2030 | $47B | $52B | $90B | Conservative planning range for committee models |
| AI agent market early 2030s (broad framing) | 2033+ | $90B | $140B | $200B | Broad-scope scenarios in secondary research |
| Global fintech market | 2024 | $340B | $395B (2025 projection) | $461B (2026 projection) | Sequential year framing from memo corpus |
| Global fintech market long horizon | 2033 | $700B | $828B | $950B | Depends on inclusion of infrastructure and embedded finance layers |
| Embedded finance | 2025 | $85.8B | $100B | $120B | Scope varies across BaaS, distribution, and software layers |
| Embedded finance long horizon | 2035 | $300B | $370.9B | $450B | Long-range volatility from policy and distribution assumptions |
| Stablecoin circulation | 2025 | $250B | $300B+ | $400B | Treat as state variable, not static TAM |

## Default Modeling Conventions

1. For investment memos, use `base case` unless an explicit stress case is requested.
2. Show at least one downside (`low`) and one upside (`high`) in IC materials.
3. Never mix totals from different definition scopes in a single CAGR calculation.

## Definitions

- `software TAM`: direct spend on products and platforms.
- `transaction-mediated TAM`: value flowing through rails/protocols.
- `economic-impact TAM`: broad productivity/economy framing (not directly monetizable by one company).

## Data Quality Flags

1. Secondary market-research providers often use non-identical category boundaries.
2. Long-horizon CAGR projections are fragile to base-year restatements.
3. Keep horizon tables tagged with source family and update timestamp before external sharing.
