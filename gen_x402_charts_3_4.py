"""
Generate x402 Charts 3 & 4:
  - Chart 3: Base vs Solana Chain Split (stacked area)
  - Chart 4: Facilitator Market Share Evolution (stacked area)
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from x402_data import CHAIN_DATA, FACILITATOR_SHARE


def make_chart3():
    """Base vs Solana Chain Split - Stacked Area Chart."""
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")

    dates = CHAIN_DATA["date"]
    base_pct = CHAIN_DATA["base_pct"]
    solana_pct = CHAIN_DATA["solana_pct"]

    ax.stackplot(
        dates,
        base_pct,
        solana_pct,
        labels=["Base", "Solana"],
        colors=["#3b82f6", "#a855f7"],
        alpha=0.85,
    )

    # Annotation: Solana flips Base daily (Jan 11)
    flip_date = pd.Timestamp("2026-01-11")
    # Find approximate solana_pct at that date via interpolation
    flip_solana_pct = np.interp(
        flip_date.value, dates.values.astype(np.int64), solana_pct.values
    )
    # Place annotation arrow pointing at the Solana region (bottom of Solana = base_pct)
    flip_base_pct = 100.0 - flip_solana_pct
    annotation_y = flip_base_pct + flip_solana_pct / 2  # middle of Solana band

    ax.annotate(
        "Solana flips Base\ndaily (Jan 11)",
        xy=(flip_date, annotation_y),
        xytext=(pd.Timestamp("2025-11-10"), 55),
        fontsize=11,
        color="white",
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="#a855f7", lw=2),
        ha="center",
    )

    ax.set_ylim(0, 100)
    ax.set_xlim(pd.Timestamp("2025-10-01"), pd.Timestamp("2026-01-31"))
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())

    ax.set_title(
        "x402 Chain Distribution: Base Dominance Eroding",
        fontsize=18,
        fontweight="bold",
        color="white",
        pad=20,
    )
    ax.set_xlabel("Date", fontsize=13, color="white")
    ax.set_ylabel("Share of Cumulative Transactions", fontsize=13, color="white")

    ax.tick_params(colors="white", labelsize=11)
    ax.grid(True, color="#333355", alpha=0.5, linewidth=0.5)

    legend = ax.legend(loc="upper right", fontsize=12, framealpha=0.3)
    for text in legend.get_texts():
        text.set_color("white")

    fig.tight_layout()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts", "x402_03_chain_split.png")
    fig.savefig(out, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    print(f"Saved: {out}")


def make_chart4():
    """Facilitator Market Share Evolution - Stacked Area Chart."""
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")

    dates = FACILITATOR_SHARE["date"]
    coinbase = FACILITATOR_SHARE["coinbase"]
    dexter = FACILITATOR_SHARE["dexter"]
    payai = FACILITATOR_SHARE["payai"]
    daydreams = FACILITATOR_SHARE["daydreams"]
    others = FACILITATOR_SHARE["others"]

    ax.stackplot(
        dates,
        coinbase,
        dexter,
        payai,
        daydreams,
        others,
        labels=["Coinbase", "Dexter", "PayAI", "DayDreams", "Others"],
        colors=["#2563eb", "#f59e0b", "#10b981", "#ec4899", "#6b7280"],
        alpha=0.85,
    )

    # Annotation 1: Dexter overtakes Coinbase (Dec 10)
    dexter_flip_date = pd.Timestamp("2025-12-10")
    ax.annotate(
        "Dexter overtakes\nCoinbase (Dec 10)",
        xy=(dexter_flip_date, 62),
        xytext=(pd.Timestamp("2025-10-20"), 78),
        fontsize=11,
        color="white",
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="#f59e0b", lw=2),
        ha="center",
    )

    # Annotation 2: Coinbase introduces fees (Jan 1)
    fees_date = pd.Timestamp("2026-01-01")
    ax.annotate(
        "Coinbase introduces\nfees (Jan 1)",
        xy=(fees_date, 14),
        xytext=(pd.Timestamp("2026-01-08"), 40),
        fontsize=11,
        color="white",
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="#2563eb", lw=2),
        ha="center",
    )

    ax.set_ylim(0, 100)
    ax.set_xlim(pd.Timestamp("2025-09-15"), pd.Timestamp("2026-01-31"))
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())

    ax.set_title(
        "Facilitator Market Share: Coinbase Losing Dominance",
        fontsize=18,
        fontweight="bold",
        color="white",
        pad=20,
    )
    ax.set_xlabel("Date", fontsize=13, color="white")
    ax.set_ylabel("Market Share (%)", fontsize=13, color="white")

    ax.tick_params(colors="white", labelsize=11)
    ax.grid(True, color="#333355", alpha=0.5, linewidth=0.5)

    legend = ax.legend(loc="upper right", fontsize=11, framealpha=0.3)
    for text in legend.get_texts():
        text.set_color("white")

    fig.tight_layout()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts", "x402_04_facilitator_share.png")
    fig.savefig(out, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    os.makedirs(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts"),
        exist_ok=True,
    )
    make_chart3()
    make_chart4()
    print("Done: Charts 3 & 4 generated.")
