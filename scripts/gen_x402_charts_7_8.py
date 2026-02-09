"""
Generate Chart 7 (Developer Adoption) and Chart 8 (Buyer/Seller Ratio)
for the x402 protocol adoption analysis.

Usage: uv run python gen_x402_charts_7_8.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "data"))

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
import numpy as np
from x402_data import DEVELOPER_METRICS, USER_METRICS

# ---------------------------------------------------------------------------
# Global style
# ---------------------------------------------------------------------------
plt.style.use("dark_background")

BG = "#1a1a2e"
GRID_COLOR = "#333355"


# =========================================================================
# CHART 7 -- Developer Adoption Funnel
# =========================================================================

def build_chart_7():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    # Data: ordered from broad interest -> narrow production usage
    labels = [
        "GitHub Stars",
        "GitHub Forks",
        "npm Downloads/wk",
        "Ecosystem Projects",
        "Infra/Tooling",
        "Live Services",
        "Facilitators",
    ]
    values = [
        DEVELOPER_METRICS["github_stars"],           # 5400
        DEVELOPER_METRICS["github_forks"],           # 1000
        DEVELOPER_METRICS["npm_weekly_downloads_coinbase_x402"],  # 2826
        DEVELOPER_METRICS["total_ecosystem_projects"],  # 117
        DEVELOPER_METRICS["infra_tooling_projects"],    # 48
        DEVELOPER_METRICS["live_services_endpoints"],   # 31
        DEVELOPER_METRICS["facilitator_count"],         # 19
    ]

    # Color gradient from bright cyan (broad) to deep purple (narrow)
    colors = ["#00d4aa", "#00c4b8", "#22b8db", "#4fc3f7", "#7c7cf7", "#a855f7", "#d946ef"]

    bars = ax.barh(labels[::-1], values[::-1], color=colors[::-1], edgecolor="white",
                   linewidth=0.5, height=0.65, zorder=5)

    # Value labels on bars
    for bar, val in zip(bars, values[::-1]):
        width = bar.get_width()
        ax.text(width + max(values) * 0.015, bar.get_y() + bar.get_height() / 2,
                f"{val:,}", va="center", ha="left", fontsize=14,
                fontweight="bold", color="white")

    ax.set_title("x402 Developer Adoption Funnel",
                 fontsize=18, fontweight="bold", color="white", pad=16)
    ax.set_xlabel("Count", fontsize=13, color="white")
    ax.tick_params(colors="white", labelsize=12)
    ax.grid(True, axis="x", color=GRID_COLOR, linewidth=0.5, alpha=0.7)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)

    # Annotate the funnel story
    ax.annotate("Broad interest\n(awareness)",
                xy=(5400, 6), xytext=(5400 + 300, 6.4),
                fontsize=10, color="#00d4aa", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#00d4aa", lw=1.2))
    ax.annotate("Narrow production\nusage (traction)",
                xy=(19, 0), xytext=(1200, -0.1),
                fontsize=10, color="#d946ef", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#d946ef", lw=1.2))

    # Conversion ratio callout
    ax.text(0.97, 0.50,
            "Funnel conversion:\n5,400 stars -> 31 live services\n= 0.6% to production",
            transform=ax.transAxes, fontsize=11, color="white",
            ha="right", va="center",
            bbox=dict(boxstyle="round,pad=0.5", fc=BG, ec="#4fc3f7", alpha=0.9))

    fig.tight_layout()
    fig.savefig(str(ROOT / "charts/x402/x402_07_developer_adoption.png"),
                facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    print("Saved charts/x402_07_developer_adoption.png")


# =========================================================================
# CHART 8 -- Buyer/Seller Ratio
# =========================================================================

def build_chart_8():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    # Latest data point: Oct 26 2025
    row = USER_METRICS.iloc[-1]
    buyers = int(row["buyers"])    # 74,000
    sellers = int(row["sellers"])  # 1,405
    ratio = buyers / sellers       # ~52.7

    # Proportional area circles
    # Area proportional to count; radius ~ sqrt(count)
    max_r = 3.5
    buyer_r = max_r
    seller_r = max_r * np.sqrt(sellers / buyers)

    buyer_circle = plt.Circle((5.5, 5), buyer_r, color="#4fc3f7", alpha=0.85, zorder=5)
    seller_circle = plt.Circle((12.5, 5), seller_r, color="#ff6b6b", alpha=0.85, zorder=5)

    ax.add_patch(buyer_circle)
    ax.add_patch(seller_circle)

    # Labels inside/near circles
    ax.text(5.5, 5, f"{buyers:,}\nBuyers", ha="center", va="center",
            fontsize=22, fontweight="bold", color="white", zorder=10)
    ax.text(12.5, 5, f"{sellers:,}\nSellers", ha="center", va="center",
            fontsize=14, fontweight="bold", color="white", zorder=10)

    # Giant ratio number
    ax.text(9.0, 8.8, f"{ratio:.0f}:1", ha="center", va="center",
            fontsize=64, fontweight="bold", color="#00d4aa", zorder=10)
    ax.text(9.0, 7.7, "Buyer-to-Seller Ratio", ha="center", va="center",
            fontsize=16, color="white", zorder=10)

    # Arrow connecting them
    ax.annotate("", xy=(12.5 - seller_r - 0.3, 5), xytext=(5.5 + buyer_r + 0.3, 5),
                arrowprops=dict(arrowstyle="->", color="#00d4aa", lw=2.5))

    # Insight callout
    ax.text(9.0, 1.5,
            "Massive demand surplus: sellers have pricing power.\n"
            "70,000 buyers added in just 3 days (Oct 23-26, 2025).",
            ha="center", va="center", fontsize=12, color="#cccccc",
            bbox=dict(boxstyle="round,pad=0.6", fc=BG, ec=GRID_COLOR, alpha=0.9))

    ax.set_xlim(0, 18)
    ax.set_ylim(0, 10.5)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.set_title("x402 Buyer vs. Seller Imbalance",
                 fontsize=18, fontweight="bold", color="white", pad=16)

    fig.tight_layout()
    fig.savefig(str(ROOT / "charts/x402/x402_08_buyer_seller_ratio.png"),
                facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    print("Saved charts/x402_08_buyer_seller_ratio.png")


# =========================================================================
# Main
# =========================================================================

if __name__ == "__main__":
    build_chart_7()
    build_chart_8()
    print("Done -- both charts generated.")
