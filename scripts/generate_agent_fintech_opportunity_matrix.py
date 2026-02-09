"""
Generate a weighted startup opportunity matrix for the agent-fintech overlap.

Outputs:
  - data/agent_fintech_startup_opportunity_matrix.csv
  - charts/intersection/05_startup_opportunity_scorecard.png
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CHART_DIR = ROOT / "charts" / "intersection"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)


# Weights sum to 1.0
WEIGHTS = {
    "market_size": 0.22,
    "startup_capture_potential": 0.25,
    "moat_durability": 0.20,
    "time_to_revenue": 0.13,
    "regulatory_tailwind": 0.10,
    "path_dependence_leverage": 0.10,
}


OPPORTUNITIES = [
    {
        "opportunity": "Agent Compliance + Audit Infrastructure",
        "stack_layer": "Layer 6",
        "lifecycle_phase": "Pre-tx checks -> Monitoring -> Audit",
        "market_size": 8.5,
        "startup_capture_potential": 8.0,
        "moat_durability": 9.5,
        "time_to_revenue": 8.0,
        "regulatory_tailwind": 9.5,
        "path_dependence_leverage": 8.5,
        "why_now": "Compliance spend is mandatory and growing as agent transactions move into regulated workflows.",
        "key_risk": "Large incumbent bundling into broader risk stacks.",
    },
    {
        "opportunity": "Cross-Protocol Payment Orchestration",
        "stack_layer": "Layer 7",
        "lifecycle_phase": "Discover route -> Authorize -> Settle",
        "market_size": 9.5,
        "startup_capture_potential": 7.5,
        "moat_durability": 8.0,
        "time_to_revenue": 6.5,
        "regulatory_tailwind": 6.0,
        "path_dependence_leverage": 9.5,
        "why_now": "Protocol fragmentation is high and no neutral default router exists.",
        "key_risk": "Incumbents (Stripe/Google/Visa/Coinbase) can bundle routing.",
    },
    {
        "opportunity": "Vertical Agentic Finance Workflows (CFO stack/AP-AR/Treasury)",
        "stack_layer": "Application Layer",
        "lifecycle_phase": "Intent -> Execution -> Reconciliation",
        "market_size": 9.0,
        "startup_capture_potential": 8.0,
        "moat_durability": 8.5,
        "time_to_revenue": 9.0,
        "regulatory_tailwind": 7.0,
        "path_dependence_leverage": 8.0,
        "why_now": "B2B adoption and budget ownership are strongest in finance ops workflows.",
        "key_risk": "Category crowding and rapid feature convergence.",
    },
    {
        "opportunity": "Agent Identity + Authorization (KYA)",
        "stack_layer": "Layers 2-3",
        "lifecycle_phase": "Identity -> Delegation -> Permissioning",
        "market_size": 8.5,
        "startup_capture_potential": 7.5,
        "moat_durability": 9.0,
        "time_to_revenue": 7.5,
        "regulatory_tailwind": 8.5,
        "path_dependence_leverage": 9.0,
        "why_now": "Trust and liability controls are required before autonomous spend scales.",
        "key_risk": "Standard-setting could drift toward incumbent-led closed systems.",
    },
    {
        "opportunity": "Agent Service Discovery + Reputation Marketplaces",
        "stack_layer": "Layer 5",
        "lifecycle_phase": "Service discovery -> Selection -> Trust scoring",
        "market_size": 9.0,
        "startup_capture_potential": 8.5,
        "moat_durability": 8.5,
        "time_to_revenue": 5.5,
        "regulatory_tailwind": 5.5,
        "path_dependence_leverage": 9.5,
        "why_now": "Owning discovery defaults can create winner-take-most data flywheels.",
        "key_risk": "Cold-start dynamics and potential platform capture by existing app ecosystems.",
    },
    {
        "opportunity": "Dispute Resolution + Recovery for Agent Transactions",
        "stack_layer": "Post-Settlement",
        "lifecycle_phase": "Fulfillment verification -> Dispute -> Recovery",
        "market_size": 7.5,
        "startup_capture_potential": 8.0,
        "moat_durability": 8.0,
        "time_to_revenue": 7.0,
        "regulatory_tailwind": 8.5,
        "path_dependence_leverage": 7.0,
        "why_now": "Autonomous finance needs machine-native chargeback/dispute rails.",
        "key_risk": "Slow standardization of liability frameworks across rails.",
    },
    {
        "opportunity": "Agent Wallet Abstraction + Policy Controls",
        "stack_layer": "Layer 0",
        "lifecycle_phase": "Credentialing -> Spend control -> Key management",
        "market_size": 7.0,
        "startup_capture_potential": 6.0,
        "moat_durability": 6.5,
        "time_to_revenue": 7.0,
        "regulatory_tailwind": 6.0,
        "path_dependence_leverage": 6.5,
        "why_now": "Every agent needs a wallet and policy guardrails.",
        "key_risk": "Platform dependency on dominant wallet/SDK ecosystems.",
    },
    {
        "opportunity": "Pure Settlement Facilitation (No Compliance Layer)",
        "stack_layer": "Layer 1",
        "lifecycle_phase": "Transaction relay",
        "market_size": 6.0,
        "startup_capture_potential": 5.0,
        "moat_durability": 3.0,
        "time_to_revenue": 6.5,
        "regulatory_tailwind": 4.5,
        "path_dependence_leverage": 3.0,
        "why_now": "Exists where transport demand grows, but fees compress quickly.",
        "key_risk": "Commoditization and near-zero switching costs.",
    },
]


def build_matrix() -> pd.DataFrame:
    df = pd.DataFrame(OPPORTUNITIES)

    weighted = (
        df["market_size"] * WEIGHTS["market_size"]
        + df["startup_capture_potential"] * WEIGHTS["startup_capture_potential"]
        + df["moat_durability"] * WEIGHTS["moat_durability"]
        + df["time_to_revenue"] * WEIGHTS["time_to_revenue"]
        + df["regulatory_tailwind"] * WEIGHTS["regulatory_tailwind"]
        + df["path_dependence_leverage"] * WEIGHTS["path_dependence_leverage"]
    )
    df["weighted_score_100"] = (weighted * 10).round(1)
    df = df.sort_values("weighted_score_100", ascending=False).reset_index(drop=True)
    df["rank"] = df.index + 1

    # Round display fields
    score_cols = [
        "market_size",
        "startup_capture_potential",
        "moat_durability",
        "time_to_revenue",
        "regulatory_tailwind",
        "path_dependence_leverage",
    ]
    for col in score_cols:
        df[col] = df[col].round(1)

    ordered_cols = [
        "rank",
        "opportunity",
        "stack_layer",
        "lifecycle_phase",
        "weighted_score_100",
        "market_size",
        "startup_capture_potential",
        "moat_durability",
        "time_to_revenue",
        "regulatory_tailwind",
        "path_dependence_leverage",
        "why_now",
        "key_risk",
    ]
    return df[ordered_cols]


def write_csv(df: pd.DataFrame) -> Path:
    out = DATA_DIR / "agent_fintech_startup_opportunity_matrix.csv"
    df.to_csv(out, index=False)
    print(f"Saved: {out}")
    return out


def plot_chart(df: pd.DataFrame) -> Path:
    chart_df = df.sort_values("weighted_score_100", ascending=True)

    fig, ax = plt.subplots(figsize=(14, 8), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    colors = ["#93C5FD"] * len(chart_df)
    if len(colors) >= 3:
        colors[-1] = "#1D4ED8"
        colors[-2] = "#2563EB"
        colors[-3] = "#3B82F6"

    bars = ax.barh(chart_df["opportunity"], chart_df["weighted_score_100"], color=colors, edgecolor="white")

    for b, v in zip(bars, chart_df["weighted_score_100"]):
        ax.text(v + 0.5, b.get_y() + b.get_height() / 2, f"{v:.1f}", va="center", fontsize=9, color="#111827")

    ax.set_xlim(0, 100)
    ax.set_xlabel("Weighted Opportunity Score (0-100)")
    ax.set_title("Agent-Fintech Startup Opportunity Scorecard", fontsize=18, fontweight="bold", pad=16)
    ax.text(
        0.5,
        1.02,
        "Weights: Market 22% | Startup Capture 25% | Moat 20% | Time-to-Revenue 13% | Regulatory 10% | Path Dependence 10%",
        transform=ax.transAxes,
        ha="center",
        fontsize=9,
        color="#6B7280",
    )
    ax.grid(axis="x", alpha=0.2, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.text(
        0.5,
        0.01,
        "Source basis: memos/agent-fintech-intersection-deep-dive.md, memos/fintech-agents-intersection.md, memos/investment-opportunities.md",
        ha="center",
        fontsize=8,
        color="#6B7280",
        style="italic",
    )
    fig.tight_layout(rect=[0.02, 0.04, 0.98, 0.95])

    out = CHART_DIR / "05_startup_opportunity_scorecard.png"
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {out}")
    return out


if __name__ == "__main__":
    print("Generating agent-fintech startup opportunity matrix...")
    matrix = build_matrix()
    write_csv(matrix)
    plot_chart(matrix)
    print("Done.")
