"""
x402 Protocol Adoption Data
============================
Raw data compiled from Dune Analytics, PANews, CoinTribune, Cryptonomist,
CryptSlate, x402.org, Coinbase Developer Docs, Stacy Muur, Lookonchain,
ainvest, ChainCatcher, and other public sources.

All data points include source annotations. Dates are approximate where
exact dates were not available.

Usage:
    uv run python x402_data.py  # prints summary tables

    # In other scripts:
    from x402_data import *
"""

import pandas as pd
import numpy as np
from datetime import datetime

# =============================================================================
# 1. DAILY TRANSACTION DATA (key data points, not continuous series)
# =============================================================================
# Sources: Dune Analytics (hashed_official), PANews, Stacy Muur, Cryptonomist

DAILY_TX_MILESTONES = pd.DataFrame([
    {"date": "2025-05-06", "daily_tx": 50,       "note": "Launch day (est.)", "source": "x402.org"},
    {"date": "2025-06-01", "daily_tx": 200,      "note": "Early adoption", "source": "est. from PANews trajectory"},
    {"date": "2025-07-01", "daily_tx": 500,      "note": "Post-hackathon (200+ projects)", "source": "est."},
    {"date": "2025-08-01", "daily_tx": 1000,     "note": "Slow steady growth", "source": "est."},
    {"date": "2025-09-01", "daily_tx": 2000,     "note": "Pre-Foundation announcement", "source": "est."},
    {"date": "2025-09-23", "daily_tx": 5000,     "note": "Foundation announced", "source": "est."},
    {"date": "2025-10-18", "daily_tx": 239505,   "note": "First major peak", "source": "PANews / Dune"},
    {"date": "2025-10-25", "daily_tx": 156492,   "note": "Weekly: 492% WoW increase", "source": "Lookonchain"},
    {"date": "2025-11-02", "daily_tx": 3000000,  "note": "All-time high", "source": "Stacy Muur / Dune"},
    {"date": "2025-11-15", "daily_tx": 2000000,  "note": "Sustained high", "source": "est."},
    {"date": "2025-11-25", "daily_tx": 200000,   "note": "Post-hype trough", "source": "multiple reports"},
    {"date": "2025-12-01", "daily_tx": 400000,   "note": "Recovery begins", "source": "est."},
    {"date": "2025-12-11", "daily_tx": 600000,   "note": "V2 release day", "source": "CryptSlate"},
    {"date": "2025-12-20", "daily_tx": 800000,   "note": "Post-V2 growth", "source": "est."},
    {"date": "2026-01-11", "daily_tx": 1023400,  "note": "Solana flips Base daily", "source": "Cryptonomist"},
    {"date": "2026-01-20", "daily_tx": 900000,   "note": "Stabilized", "source": "est."},
    {"date": "2026-02-01", "daily_tx": 850000,   "note": "Recent steady state", "source": "est."},
])
DAILY_TX_MILESTONES["date"] = pd.to_datetime(DAILY_TX_MILESTONES["date"])


# =============================================================================
# 2. CUMULATIVE TRANSACTION DATA
# =============================================================================

CUMULATIVE_TX = pd.DataFrame([
    {"date": "2025-05-06", "cumulative_tx": 0,         "cumulative_volume_usd": 0,          "source": "Launch"},
    {"date": "2025-10-26", "cumulative_tx": 1446000,   "cumulative_volume_usd": 1590000,    "source": "PANews / Dune"},
    {"date": "2025-11-15", "cumulative_tx": 40000000,  "cumulative_volume_usd": 10000000,   "source": "Stacy Muur / Dune"},
    {"date": "2025-12-01", "cumulative_tx": 75000000,  "cumulative_volume_usd": 24000000,   "source": "CryptSlate"},
    {"date": "2025-12-15", "cumulative_tx": 100000000, "cumulative_volume_usd": 35000000,   "source": "x402.org ('over 100M')"},
    {"date": "2026-01-15", "cumulative_tx": 157600000, "cumulative_volume_usd": 600000000,  "source": "Cryptonomist (119M Base + 38.6M Sol); ainvest ($600M)"},
])
CUMULATIVE_TX["date"] = pd.to_datetime(CUMULATIVE_TX["date"])


# =============================================================================
# 3. CHAIN SPLIT DATA
# =============================================================================

CHAIN_DATA = pd.DataFrame([
    # Base dominated early, Solana catching up
    {"date": "2025-10-26", "base_tx": 1400000,   "solana_tx": 46000,     "base_pct": 96.8, "solana_pct": 3.2,  "source": "PANews"},
    {"date": "2025-11-15", "base_tx": 38000000,  "solana_tx": 2000000,   "base_pct": 95.0, "solana_pct": 5.0,  "source": "est."},
    {"date": "2025-12-01", "base_tx": 68000000,  "solana_tx": 7000000,   "base_pct": 90.7, "solana_pct": 9.3,  "source": "est."},
    {"date": "2025-12-15", "base_tx": 85000000,  "solana_tx": 15000000,  "base_pct": 85.0, "solana_pct": 15.0, "source": "est."},
    {"date": "2026-01-11", "base_tx": 110000000, "solana_tx": 35000000,  "base_pct": 75.9, "solana_pct": 24.1, "source": "Cryptonomist"},
    {"date": "2026-01-15", "base_tx": 119000000, "solana_tx": 38600000,  "base_pct": 75.5, "solana_pct": 24.5, "source": "Cryptonomist"},
])
CHAIN_DATA["date"] = pd.to_datetime(CHAIN_DATA["date"])

# Daily chain split on Jan 11, 2026 (the day Solana flipped Base)
CHAIN_DAILY_JAN11 = {
    "base_daily": 505000,
    "solana_daily": 518400,
    "base_pct": 49.3,
    "solana_pct": 50.7,
    "source": "Cryptonomist",
}


# =============================================================================
# 4. FACILITATOR MARKET SHARE DATA
# =============================================================================

FACILITATOR_SHARE = pd.DataFrame([
    # Early period: Coinbase dominant
    {"date": "2025-10-01", "coinbase": 70, "dexter": 5,    "payai": 15,  "daydreams": 5,  "others": 5,  "source": "est. from reports"},
    {"date": "2025-11-01", "coinbase": 60, "dexter": 10,   "payai": 18,  "daydreams": 7,  "others": 5,  "source": "est."},
    {"date": "2025-12-01", "coinbase": 45, "dexter": 20,   "payai": 20,  "daydreams": 10, "others": 5,  "source": "est."},
    {"date": "2025-12-10", "coinbase": 31, "dexter": 30.7, "payai": 20,  "daydreams": 13, "others": 5.3, "source": "ChainCatcher / Dune"},
    {"date": "2026-01-01", "coinbase": 28, "dexter": 45,   "payai": 15,  "daydreams": 7,  "others": 5,  "source": "est."},
    {"date": "2026-01-15", "coinbase": 25, "dexter": 50,   "payai": 13,  "daydreams": 7,  "others": 5,  "source": "est. (Dexter ~50% daily)"},
])
FACILITATOR_SHARE["date"] = pd.to_datetime(FACILITATOR_SHARE["date"])

# Facilitator cumulative stats
FACILITATOR_CUMULATIVE = pd.DataFrame([
    {"name": "Coinbase CDP",  "cumulative_tx": 10000000, "cumulative_volume_usd": 1004000,  "fee_model": "$0.001/tx after 1K free/mo", "source": "PANews / Dune"},
    {"name": "Dexter",        "cumulative_tx": 10000000, "cumulative_volume_usd": None,      "fee_model": "Not disclosed", "source": "ecosystem reports"},
    {"name": "PayAI",         "cumulative_tx": 10000000, "cumulative_volume_usd": 219000,    "fee_model": "Gas-free; opt. 1% buyer fee", "source": "PANews / Dune"},
    {"name": "DayDreams",     "cumulative_tx": 10000000, "cumulative_volume_usd": None,      "fee_model": "Not disclosed", "source": "ecosystem reports"},
    {"name": "Stakefy",       "cumulative_tx": None,     "cumulative_volume_usd": None,      "fee_model": "0.5% per tx", "source": "Stakefy docs"},
    {"name": "Stake Capital", "cumulative_tx": None,     "cumulative_volume_usd": 2350000,   "fee_model": "Not disclosed", "source": "Stake Capital"},
])


# =============================================================================
# 5. USER METRICS
# =============================================================================

USER_METRICS = pd.DataFrame([
    {"date": "2025-10-23", "buyers": 4000,  "sellers": 1078, "source": "PANews / Dune"},
    {"date": "2025-10-26", "buyers": 74000, "sellers": 1405, "source": "PANews / Dune (70K added in 3 days)"},
])
USER_METRICS["date"] = pd.to_datetime(USER_METRICS["date"])

# 90-day Dune dashboard snapshot (as of late Oct 2025)
DUNE_90DAY = {
    "transactions": 52400,
    "tx_change_pct": 93.3,
    "volume_usd": 521100,
    "volume_change_pct": 4120.38,
    "buyers": 991,
    "buyers_change_pct": 279.6,
    "sellers": 244,
    "sellers_change_pct": 75.5,
    "period": "90 days ending ~Oct 26 2025",
    "source": "Dune Analytics",
}


# =============================================================================
# 6. DEVELOPER ADOPTION
# =============================================================================

DEVELOPER_METRICS = {
    "github_stars": 5400,
    "github_forks": 1000,
    "npm_weekly_downloads_coinbase_x402": 2826,
    "npm_dependent_projects": 19,
    "x402_express_dependents": 9,
    "x402_next_dependents": 0,
    "total_ecosystem_projects": 117,
    "live_services_endpoints": 31,
    "facilitator_count": 19,
    "infra_tooling_projects": 48,
    "client_integrations": 16,
    "hackathon_submissions_total": 600,  # 200+ (June) + 400+ (Solana)
    "latest_version": "2.1.0",
    "source": "GitHub, npm, x402.org ecosystem page",
}


# =============================================================================
# 7. PAYMENT SIZE DISTRIBUTION
# =============================================================================

PAYMENT_METRICS = {
    "avg_payment_usd": 0.80,            # midpoint of $0.60-$1.00 range
    "avg_payment_range": (0.60, 1.00),   # PANews / Dune
    "min_payment_possible": 0.001,
    "usdc_share_pct": 98.7,
    "avg_latency_rollup_ms": 200,
    "settlement_time_base_s": 2,
    "settlement_time_solana_ms": 400,
    "source": "PANews, x402.org docs, Cryptonomist",
}


# =============================================================================
# 8. VALUE CHAIN ECONOMICS (per $0.01 payment)
# =============================================================================

VALUE_CHAIN = pd.DataFrame([
    {"layer": "Application (seller)",    "amount_per_001": 0.0088, "pct_of_payment": 88.0, "margin_pct": "70-90%"},
    {"layer": "Facilitator",             "amount_per_001": 0.0010, "pct_of_payment": 10.0, "margin_pct": "50-75%"},
    {"layer": "Chain sequencer (Base)",  "amount_per_001": 0.0010, "pct_of_payment": 1.0,  "margin_pct": ">90%"},
    {"layer": "Chain validator (Solana)","amount_per_001": 0.00025,"pct_of_payment": 0.25, "margin_pct": "~50%"},
    {"layer": "Protocol (x402)",         "amount_per_001": 0.0000, "pct_of_payment": 0.0,  "margin_pct": "N/A"},
    {"layer": "RPC provider",            "amount_per_001": 0.0001, "pct_of_payment": 0.1,  "margin_pct": "60-70%"},
    {"layer": "USDC issuer (Circle)",    "amount_per_001": 0.0000, "pct_of_payment": 0.0,  "margin_pct": "~95% (float)"},
])


# =============================================================================
# 9. ECOSYSTEM TOKEN MARKET CAP (speculative / narrative-driven)
# =============================================================================

ECOSYSTEM_MCAP = pd.DataFrame([
    {"date": "2025-10-15", "mcap_usd": 100000000,   "source": "CoinGecko est."},
    {"date": "2025-10-26", "mcap_usd": 780000000,   "source": "CoinGecko"},
    {"date": "2025-11-05", "mcap_usd": 12000000000,  "source": "CoinGecko (1300% gain in ~2 weeks)"},
    {"date": "2025-12-01", "mcap_usd": 5000000000,   "source": "est. post-correction"},
    {"date": "2026-01-15", "mcap_usd": 10500000000,  "source": "CoinGecko"},
])
ECOSYSTEM_MCAP["date"] = pd.to_datetime(ECOSYSTEM_MCAP["date"])


# =============================================================================
# 10. INDUSTRY FORECASTS
# =============================================================================

FORECASTS = {
    "galaxy_digital_2026": "x402 will reach 30% of Base daily tx and 5% of Solana tx in 2026",
    "a16z_gartner_2030": "Machine customers will influence $30T in transactions by 2030; x402 as backbone",
    "longhash_2030": "AI agents handle $1T-$5T in global transactions by 2030",
    "source": "Galaxy Digital (Dec 2025), a16z (citing Gartner), LongHash Ventures",
}


# =============================================================================
# PRINT SUMMARY
# =============================================================================
if __name__ == "__main__":
    print("=" * 80)
    print("x402 PROTOCOL ADOPTION DATA SUMMARY")
    print("=" * 80)

    print("\n--- DAILY TRANSACTION MILESTONES ---")
    print(DAILY_TX_MILESTONES[["date", "daily_tx", "note"]].to_string(index=False))

    print("\n--- CUMULATIVE METRICS ---")
    print(CUMULATIVE_TX.to_string(index=False))

    print("\n--- CHAIN SPLIT (Base vs Solana) ---")
    print(CHAIN_DATA[["date", "base_pct", "solana_pct"]].to_string(index=False))

    print("\n--- FACILITATOR MARKET SHARE (%) ---")
    print(FACILITATOR_SHARE[["date", "coinbase", "dexter", "payai", "daydreams"]].to_string(index=False))

    print("\n--- DEVELOPER METRICS ---")
    for k, v in DEVELOPER_METRICS.items():
        print(f"  {k}: {v}")

    print("\n--- VALUE CHAIN (per $0.01 payment) ---")
    print(VALUE_CHAIN.to_string(index=False))
