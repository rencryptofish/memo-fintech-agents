# Fintech & AI Agent Economy Research

Research memos analyzing fintech market opportunities, AI agent economy infrastructure, and their convergence. Compiled February 2026.

## Memos

Hierarchy and reading order:

1. [Top-Level Takeaways (Start Here)](memos/00-top-level-takeaways.md)
2. [Memo Hierarchy Index](memos/README.md)

| Layer | Memo | Description |
|------|------|-------------|
| Decision | [Investment Committee Memo](memos/investment-committee-memo-agent-fintech-infrastructure-2026-02-09.md) | Current view, risk controls, and go/no-go milestones |
| Decision | [Top 15 Investment Opportunities](memos/investment-opportunities.md) | Synthesized ranking across all research domains |
| Convergence | [Agent-Fintech Intersection Deep Dive](memos/agent-fintech-intersection-deep-dive.md) | 8-layer stack map, traction, moat hierarchy, and investable wedges |
| Convergence | [Fintech x AI Agents Intersection](memos/fintech-agents-intersection.md) | Protocol comparison, KYA framing, and intersection opportunity set |
| Convergence | [Agent-Fintech Mental Models](memos/agent-fintech-mental-models-end-states.md) | Probability-weighted end states, path dependence, and control-point frameworks |
| Domain | [Fintech Market Analysis](memos/fintech-market-analysis.md) | Fintech landscape, cohort history, and segment economics |
| Domain | [Fintech Investment Opportunities](memos/fintech-investment-opportunities-2026.md) | Company-level fintech opportunities and M&A signals |
| Domain | [Agent Economy](memos/agent-economy-memo.md) | Agent stack, market map, and infrastructure opportunities |
| Domain | [x402 Protocol Deep Dive](memos/x402-research-memo.md) | Protocol mechanics, adoption metrics, and competitive positioning |
| Domain | [x402 Value Capture Analysis](memos/x402-value-capture-analysis.md) | Layer-by-layer value accrual and monetization dynamics |

## Charts

Generated from sourced data in `data/`. Run scripts with `uv run python scripts/<script>.py` (or `uv run python gen_x402_value_accrual.py` for x402 charts 9-11).
For funding stage breakdowns specifically, run `uv run python scripts/generate_fintech_stage_charts.py`.

- **`charts/fintech/`** - 18 charts: core funding/market maps, trajectory and cohort views, stage breakdown pack, category-company map, geography dashboard, failure-risk KPI dashboard, and value-creation-vs-destruction case dashboard
- **`charts/agent-economy/`** - 13 charts: market sizing, ARR race, growth rates, valuation multiples, market map, funding rounds, M&A, Gartner timeline, autonomy spectrum, infrastructure gaps, and funding-vs-revenue trajectory scatter
- **`charts/intersection/`** - 4 charts: protocol launch timeline, protocol capability matrix, layer funding heatmap, and agent-commerce readiness roadmap
- **`charts/x402/`** - 14 charts: core adoption/economics set plus layer-revenue sensitivity, Coinbase revenue scenarios, and risk matrix

## Structure

```
memos/          Research memos (markdown)
charts/         Generated visualizations (PNG)
  agent-economy/
  intersection/
  x402/
  fintech/
data/           Structured datasets with source attribution
scripts/        Python chart generation scripts
```
