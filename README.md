# Fintech & AI Agent Economy Research

Research memos analyzing fintech market opportunities, AI agent economy infrastructure, and their convergence. Compiled February 2026.

## Memos

| Memo | Description |
|------|-------------|
| [Fintech Market Analysis](memos/fintech-market-analysis.md) | Comprehensive fintech landscape: $340B market, 8 founding cohorts (pre-2008 through 2026), geographic hubs, success/failure patterns, cohort funding comparison |
| [Agent Economy](memos/agent-economy-memo.md) | AI agent economy overview: $7-8B market (2025), 10 verticals, infrastructure stack, funding landscape, MCP/A2A protocols |
| [x402 Protocol Deep Dive](memos/x402-research-memo.md) | Coinbase's HTTP-native stablecoin payment protocol: 157M+ transactions, $600M+ volume, technical architecture |
| [x402 Value Capture Analysis](memos/x402-value-capture-analysis.md) | First-principles value chain analysis: 8 layers, 9 historical analogies, seven-force framework, investable opportunities |
| [Fintech x Agents Intersection](memos/fintech-agents-intersection.md) | Convergence research: agent payment protocols (x402, ACP, AP2, TAP), agent wallets, DeFAI, KYA framework |
| [Fintech Investment Opportunities](memos/fintech-investment-opportunities-2026.md) | Specific investable opportunities: AI-native fintech, stablecoin infra, real-time payments, CFO stack |
| [Top 15 Investment Opportunities](memos/investment-opportunities.md) | Final synthesized ranking across all three domains with evaluation framework and M&A signals |

## Charts

Generated from sourced data in `data/`. Run scripts with `uv run python scripts/<script>.py` (or `uv run python gen_x402_value_accrual.py` for x402 charts 9-11).

- **`charts/fintech/`** - 4 charts: stacked bar, market map, heatmap, and funding-vs-revenue trajectory scatter
- **`charts/agent-economy/`** - 13 charts: market sizing, ARR race, growth rates, valuation multiples, market map, funding rounds, M&A, Gartner timeline, autonomy spectrum, infrastructure gaps, and funding-vs-revenue trajectory scatter
- **`charts/x402/`** - 11 charts: daily transactions, cumulative growth, chain split, facilitator share, value chain, ecosystem mcap, developer adoption, buyer/seller ratio, deep buyer/seller dynamics, value accrual stack, Coinbase flywheel

## Structure

```
memos/          Research memos (markdown)
charts/         Generated visualizations (PNG)
  agent-economy/
  x402/
  fintech/
data/           Structured datasets with source attribution
scripts/        Python chart generation scripts
```
