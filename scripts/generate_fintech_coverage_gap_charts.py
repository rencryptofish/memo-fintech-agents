"""
Generate additional fintech charts/CSVs for high-value coverage gaps:
1) Geography dashboard
2) Failure-risk KPI dashboard
3) Value creation vs destruction case comparison

Source basis:
- memos/fintech-market-analysis.md
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CHART_DIR = ROOT / "charts" / "fintech"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)


def build_geography_data() -> pd.DataFrame:
    """Regional/hub metrics that were previously only in prose tables."""
    rows = [
        # Regional indicators (percent-style).
        {"metric_group": "share_indicator_pct", "label": "North America market share (2024)", "value": 35.8, "unit": "percent"},
        {"metric_group": "share_indicator_pct", "label": "Brazil share of LatAm fintechs", "value": 58.7, "unit": "percent"},
        {"metric_group": "share_indicator_pct", "label": "Singapore share of ASEAN fintechs", "value": 40.0, "unit": "percent"},
        # India growth trajectory.
        {"metric_group": "india_market_size", "label": "India fintech market (2024)", "value": 111.0, "unit": "usd_b"},
        {"metric_group": "india_market_size", "label": "India fintech market (2029)", "value": 421.0, "unit": "usd_b"},
        # Africa hub activity + funding.
        {"metric_group": "africa_hubs", "label": "Lagos", "value": 503.0, "unit": "active_firms"},
        {"metric_group": "africa_hubs", "label": "Lagos funding", "value": 6.03, "unit": "usd_b"},
        {"metric_group": "africa_hubs", "label": "Nairobi", "value": 210.0, "unit": "active_firms"},
        {"metric_group": "africa_hubs", "label": "Nairobi funding", "value": 4.64, "unit": "usd_b"},
    ]
    return pd.DataFrame(rows)


def chart_geography_dashboard(df: pd.DataFrame) -> None:
    """Three-panel geography chart for regional share, India growth, and Africa hubs."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=180)
    fig.patch.set_facecolor("white")

    # Panel 1: share indicators.
    share = df[df["metric_group"] == "share_indicator_pct"].copy()
    share = share.sort_values("value", ascending=True)
    ax = axes[0]
    ax.barh(share["label"], share["value"], color=["#1D4ED8", "#2563EB", "#60A5FA"], edgecolor="white")
    ax.set_xlim(0, 70)
    ax.set_xlabel("Percent (%)")
    ax.set_title("Regional Share Signals", fontsize=12, fontweight="bold")
    ax.grid(axis="x", alpha=0.2, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for i, v in enumerate(share["value"]):
        ax.text(v + 1.0, i, f"{v:.1f}%", va="center", fontsize=9, color="#1F2937")

    # Panel 2: India growth.
    india = df[df["metric_group"] == "india_market_size"].copy()
    years = np.array([2024, 2029])
    vals = india["value"].to_numpy()
    ax = axes[1]
    ax.plot(years, vals, color="#0EA5E9", linewidth=3, marker="o", markersize=7)
    ax.fill_between(years, vals, color="#BAE6FD", alpha=0.35)
    ax.set_xticks(years)
    ax.set_ylim(90, 450)
    ax.set_ylabel("USD Billions")
    ax.set_title("India Fintech Market Growth", fontsize=12, fontweight="bold")
    ax.grid(axis="y", alpha=0.2, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for x, y in zip(years, vals):
        ax.annotate(f"${y:.0f}B", (x, y), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=9)
    cagr = (vals[1] / vals[0]) ** (1 / (years[1] - years[0])) - 1
    ax.text(2026.5, 410, f"Implied CAGR: {cagr * 100:.2f}%", ha="center", fontsize=9, color="#0C4A6E")

    # Panel 3: Africa hub activity vs funding.
    hub_rows = [
        ("Lagos", 503, 6.03),
        ("Nairobi", 210, 4.64),
    ]
    ax = axes[2]
    for hub, firms, funding in hub_rows:
        ax.scatter(firms, funding, s=150, alpha=0.9, edgecolor="white", linewidth=1.1, label=hub)
        ax.annotate(hub, (firms, funding), xytext=(6, 6), textcoords="offset points", fontsize=9)
    ax.set_xlabel("Active Fintech Firms")
    ax.set_ylabel("Funding ($B)")
    ax.set_title("Africa Hub Funding vs Activity", fontsize=12, fontweight="bold")
    ax.grid(alpha=0.2, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlim(150, 560)
    ax.set_ylim(4.0, 6.4)

    fig.suptitle("Fintech Geography Coverage Dashboard (Previously Under-Charted)", fontsize=16, fontweight="bold", y=0.98)
    fig.text(
        0.5,
        0.01,
        "Source: memos/fintech-market-analysis.md (Regional Dynamics + Geographic Founding Patterns).",
        ha="center",
        fontsize=9,
        color="#6B7280",
        style="italic",
    )
    fig.tight_layout(rect=[0.02, 0.04, 0.98, 0.94])
    out = CHART_DIR / "fintech_geographic_opportunity_dashboard.png"
    fig.savefig(out, dpi=260, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {out}")


def build_failure_risk_data() -> pd.DataFrame:
    """Failure/risk KPIs that appear in memo prose but lacked a dedicated chart."""
    rows = [
        {"kpi": "Fintech startups failing from poor unit economics", "value_pct": 67.0},
        {"kpi": "Startups facing serious regulatory challenges", "value_pct": 73.0},
        {"kpi": "Cross-border expansions failing on compliance", "value_pct": 58.0},
        {"kpi": "Failures with banking partnership issues", "value_pct": 42.0},
        {"kpi": "Digital banks reaching breakeven", "value_pct": 5.0},
        {"kpi": "Challenger banks profitable (92 of 650)", "value_pct": 92.0 / 650.0 * 100.0},
        {"kpi": "BNPL users late on payments (2025)", "value_pct": 41.0},
        {"kpi": "Average value destruction in fintech SPACs", "value_pct": 67.0},
    ]
    return pd.DataFrame(rows)


def chart_failure_risk_dashboard(df: pd.DataFrame) -> None:
    """Horizontal ranking of risk KPIs + CAC side panel."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), dpi=180, gridspec_kw={"width_ratios": [3.2, 1.2]})
    fig.patch.set_facecolor("white")

    # Main risk KPI bars.
    rank = df.sort_values("value_pct", ascending=True)
    ax = axes[0]
    colors = ["#FCA5A5" if v < 20 else "#F87171" if v < 50 else "#EF4444" for v in rank["value_pct"]]
    ax.barh(rank["kpi"], rank["value_pct"], color=colors, edgecolor="white")
    ax.set_xlim(0, 80)
    ax.set_xlabel("Percent (%)")
    ax.set_title("Failure & Risk KPI Coverage", fontsize=14, fontweight="bold")
    ax.grid(axis="x", alpha=0.2, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for i, v in enumerate(rank["value_pct"]):
        ax.text(v + 1.0, i, f"{v:.1f}%", va="center", fontsize=8.5, color="#111827")

    # Side panel for CAC signal.
    ax = axes[1]
    cac_low, cac_high, cac_avg = 25.0, 35.0, 1450.0
    ax.bar(["CAC growth range"], [cac_high - cac_low], bottom=[cac_low], color="#FB923C", width=0.55)
    ax.scatter([0], [cac_avg / 100.0], color="#C2410C", s=55, zorder=3)  # scaled for shared % axis
    ax.set_ylim(0, 40)
    ax.set_ylabel("Percent / Scaled marker")
    ax.set_title("CAC Pressure", fontsize=13, fontweight="bold")
    ax.text(0, cac_high + 1.2, "25-35%/yr\nCAC growth", ha="center", fontsize=9)
    ax.text(0, (cac_low + cac_high) / 2, "Avg CAC\n$1,450", ha="center", va="center", fontsize=9, color="#7C2D12")
    ax.grid(axis="y", alpha=0.2, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.suptitle("Fintech Failure-Risk Dashboard (Previously Missing)", fontsize=16, fontweight="bold", y=0.98)
    fig.text(
        0.5,
        0.01,
        "Source: memos/fintech-market-analysis.md (What Failed + Common Failure Patterns).",
        ha="center",
        fontsize=9,
        color="#6B7280",
        style="italic",
    )
    fig.tight_layout(rect=[0.02, 0.04, 0.98, 0.94])
    out = CHART_DIR / "fintech_failure_risk_kpi_dashboard.png"
    fig.savefig(out, dpi=260, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {out}")


def build_value_creation_vs_destruction_data() -> pd.DataFrame:
    """Comparable case metrics for winners vs failure events."""
    rows = [
        # Value creation proxies (valuation/status snapshots, USD billions).
        {"side": "value_creation", "label": "Stripe valuation", "amount_b": 106.7},
        {"side": "value_creation", "label": "Revolut valuation", "amount_b": 75.0},
        {"side": "value_creation", "label": "Nubank 2024 revenue", "amount_b": 11.5},
        {"side": "value_creation", "label": "Chime IPO valuation", "amount_b": 18.4},
        {"side": "value_creation", "label": "Plaid valuation", "amount_b": 6.1},
        # Value destruction proxies (capital/value wiped).
        {"side": "value_destruction", "label": "Klarna valuation drop", "amount_b": 45.6 - 6.7},
        {"side": "value_destruction", "label": "FTX valuation collapse", "amount_b": 32.0},
        {"side": "value_destruction", "label": "Wirecard fraud hole", "amount_b": 1.9},
        {"side": "value_destruction", "label": "Synapse funds affected", "amount_b": 0.265},
    ]
    return pd.DataFrame(rows)


def chart_value_creation_vs_destruction(df: pd.DataFrame) -> None:
    """Mirror bars comparing winner scale vs failure destruction scale."""
    created = df[df["side"] == "value_creation"].sort_values("amount_b", ascending=True)
    destroyed = df[df["side"] == "value_destruction"].sort_values("amount_b", ascending=True)

    fig, axes = plt.subplots(1, 2, figsize=(16, 7), dpi=180, sharex=False)
    fig.patch.set_facecolor("white")

    # Left: value creation.
    ax = axes[0]
    ax.barh(created["label"], created["amount_b"], color="#2563EB", edgecolor="white")
    ax.set_title("Value Creation Cases", fontsize=14, fontweight="bold")
    ax.set_xlabel("USD Billions")
    ax.grid(axis="x", alpha=0.2, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for i, v in enumerate(created["amount_b"]):
        ax.text(v + 0.8, i, f"${v:.1f}B", va="center", fontsize=9)

    # Right: value destruction.
    ax = axes[1]
    ax.barh(destroyed["label"], destroyed["amount_b"], color="#EF4444", edgecolor="white")
    ax.set_title("Value Destruction Cases", fontsize=14, fontweight="bold")
    ax.set_xlabel("USD Billions")
    ax.grid(axis="x", alpha=0.2, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for i, v in enumerate(destroyed["amount_b"]):
        ax.text(v + 0.5, i, f"${v:.1f}B", va="center", fontsize=9)

    fig.suptitle("Fintech Case Outcomes: Created vs Destroyed Value", fontsize=16, fontweight="bold", y=0.98)
    fig.text(
        0.5,
        0.01,
        "Source: memos/fintech-market-analysis.md (Top Success Stories + Major Failure Case Studies).",
        ha="center",
        fontsize=9,
        color="#6B7280",
        style="italic",
    )
    fig.tight_layout(rect=[0.02, 0.04, 0.98, 0.94])
    out = CHART_DIR / "fintech_value_creation_vs_destruction_cases.png"
    fig.savefig(out, dpi=260, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {out}")


def write_csv(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False)
    print(f"Saved: {path}")


if __name__ == "__main__":
    print("Generating fintech coverage-gap datasets and charts...")

    geo = build_geography_data()
    write_csv(geo, DATA_DIR / "fintech_geographic_opportunity_metrics.csv")
    chart_geography_dashboard(geo)

    risk = build_failure_risk_data()
    write_csv(risk, DATA_DIR / "fintech_failure_risk_kpis.csv")
    chart_failure_risk_dashboard(risk)

    cases = build_value_creation_vs_destruction_data()
    write_csv(cases, DATA_DIR / "fintech_value_creation_vs_destruction_cases.csv")
    chart_value_creation_vs_destruction(cases)

    print("Done.")
