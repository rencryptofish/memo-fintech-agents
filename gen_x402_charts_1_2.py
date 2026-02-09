"""
Generate Chart 1 (Daily Transaction Trajectory) and Chart 2 (Cumulative Growth)
for the x402 protocol adoption analysis.

Usage: uv run python gen_x402_charts_1_2.py
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
from x402_data import DAILY_TX_MILESTONES, CUMULATIVE_TX

# ---------------------------------------------------------------------------
# Global style
# ---------------------------------------------------------------------------
plt.style.use("dark_background")

BG = "#1a1a2e"
GRID_COLOR = "#333355"
CYAN = "#00d4aa"
BLUE = "#4fc3f7"
GREEN = "#66bb6a"


def style_ax(ax, title, xlabel, ylabel):
    """Apply shared styling to an axis."""
    ax.set_facecolor(BG)
    ax.set_title(title, fontsize=18, fontweight="bold", color="white", pad=16)
    ax.set_xlabel(xlabel, fontsize=13, color="white")
    ax.set_ylabel(ylabel, fontsize=13, color="white")
    ax.tick_params(colors="white", labelsize=11)
    ax.grid(True, color=GRID_COLOR, linewidth=0.5, alpha=0.7)
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)


# =========================================================================
# CHART 1 -- Daily Transaction Trajectory (log scale)
# =========================================================================

def build_chart_1():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor(BG)

    dates = DAILY_TX_MILESTONES["date"]
    txs = DAILY_TX_MILESTONES["daily_tx"]

    ax.plot(dates, txs, color=CYAN, linewidth=2.4, marker="o", markersize=7,
            markerfacecolor="white", markeredgecolor=CYAN, markeredgewidth=1.5,
            zorder=5)

    # Fill area under curve for visual weight
    ax.fill_between(dates, txs, alpha=0.08, color=CYAN)

    ax.set_yscale("log")
    style_ax(ax,
             "x402 Daily Transactions: Launch to Feb 2026",
             "Date", "Daily Transactions (log scale)")

    # Y-axis formatting
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(
        lambda x, _: f"{int(x):,}" if x < 1000 else
                      f"{x/1_000:.0f}K" if x < 1_000_000 else
                      f"{x/1_000_000:.1f}M"))

    # X-axis formatting
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    fig.autofmt_xdate(rotation=30)

    # --- Annotations ---
    annotations = [
        ("2025-05-06", "Launch",                 (40,  40)),
        ("2025-09-23", "Foundation\nannounced",   (30,  50)),
        ("2025-10-18", "First spike:\n240K/day",  (-100, 45)),
        ("2025-11-02", "ATH: 3M/day",            (20,  35)),
        ("2025-11-25", "Trough:\n200K/day",       (40,  -50)),
        ("2025-12-11", "V2 Release",              (30,  45)),
        ("2026-01-11", "Solana flips\nBase",      (-110, 40)),
    ]

    for date_str, label, offset in annotations:
        row = DAILY_TX_MILESTONES[DAILY_TX_MILESTONES["date"] == date_str]
        if row.empty:
            continue
        x = row["date"].values[0]
        y = row["daily_tx"].values[0]
        ax.annotate(
            label,
            xy=(x, y),
            xytext=offset,
            textcoords="offset points",
            fontsize=10,
            fontweight="bold",
            color="white",
            arrowprops=dict(arrowstyle="->", color=CYAN, lw=1.5),
            ha="center",
            va="bottom",
            bbox=dict(boxstyle="round,pad=0.3", fc=BG, ec=CYAN, alpha=0.85),
        )

    ax.set_ylim(bottom=30)
    fig.tight_layout()
    fig.savefig("/Users/cat/memo-fintech-agents/charts/x402_01_daily_tx_trajectory.png",
                facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    print("Saved charts/x402_01_daily_tx_trajectory.png")


# =========================================================================
# CHART 2 -- Cumulative Growth (dual y-axis)
# =========================================================================

def format_num(val, is_usd=False):
    """Human-friendly label for data points."""
    if val == 0:
        return "$0" if is_usd else "0"
    if is_usd:
        if val >= 1_000_000_000:
            return f"${val/1e9:.1f}B"
        if val >= 1_000_000:
            return f"${val/1e6:.0f}M"
        if val >= 1_000:
            return f"${val/1e3:.0f}K"
        return f"${val:.0f}"
    else:
        if val >= 1_000_000_000:
            return f"{val/1e9:.1f}B"
        if val >= 1_000_000:
            return f"{val/1e6:.0f}M"
        if val >= 1_000:
            return f"{val/1e3:.0f}K"
        return f"{val:.0f}"


def build_chart_2():
    fig, ax1 = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor(BG)

    dates = CUMULATIVE_TX["date"]
    cum_tx = CUMULATIVE_TX["cumulative_tx"]
    cum_vol = CUMULATIVE_TX["cumulative_volume_usd"]

    # Left axis -- cumulative transactions
    ax1.set_facecolor(BG)
    line1, = ax1.plot(dates, cum_tx, color=BLUE, linewidth=2.4, marker="D",
                      markersize=8, markerfacecolor="white", markeredgecolor=BLUE,
                      markeredgewidth=1.5, label="Cumulative Transactions", zorder=5)
    ax1.fill_between(dates, cum_tx, alpha=0.06, color=BLUE)

    ax1.set_xlabel("Date", fontsize=13, color="white")
    ax1.set_ylabel("Cumulative Transactions", fontsize=13, color=BLUE)
    ax1.tick_params(axis="y", colors=BLUE, labelsize=11)
    ax1.tick_params(axis="x", colors="white", labelsize=11)
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(
        lambda x, _: format_num(x)))

    # Data labels -- transactions
    for i, (d, t) in enumerate(zip(dates, cum_tx)):
        offset_y = 12 if i < len(dates) - 1 else -22
        ax1.annotate(format_num(t), xy=(d, t),
                     xytext=(0, offset_y), textcoords="offset points",
                     fontsize=9, fontweight="bold", color=BLUE, ha="center")

    # Right axis -- cumulative volume USD
    ax2 = ax1.twinx()
    line2, = ax2.plot(dates, cum_vol, color=GREEN, linewidth=2.4, marker="s",
                      markersize=8, markerfacecolor="white", markeredgecolor=GREEN,
                      markeredgewidth=1.5, label="Cumulative Volume (USD)", zorder=5)
    ax2.fill_between(dates, cum_vol, alpha=0.06, color=GREEN)

    ax2.set_ylabel("Cumulative Volume (USD)", fontsize=13, color=GREEN)
    ax2.tick_params(axis="y", colors=GREEN, labelsize=11)
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(
        lambda x, _: format_num(x, is_usd=True)))

    # Data labels -- volume
    for i, (d, v) in enumerate(zip(dates, cum_vol)):
        offset_y = -22 if i < len(dates) - 1 else 12
        ax2.annotate(format_num(v, is_usd=True), xy=(d, v),
                     xytext=(0, offset_y), textcoords="offset points",
                     fontsize=9, fontweight="bold", color=GREEN, ha="center")

    # Title, grid, legend
    ax1.set_title("x402 Cumulative Growth: Transactions & Volume",
                  fontsize=18, fontweight="bold", color="white", pad=16)
    ax1.grid(True, color=GRID_COLOR, linewidth=0.5, alpha=0.7)
    for spine in ax1.spines.values():
        spine.set_color(GRID_COLOR)
    for spine in ax2.spines.values():
        spine.set_color(GRID_COLOR)

    # X-axis formatting
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    fig.autofmt_xdate(rotation=30)

    # Combined legend
    lines = [line1, line2]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="upper left", fontsize=12,
               facecolor=BG, edgecolor=GRID_COLOR, labelcolor="white")

    fig.tight_layout()
    fig.savefig("/Users/cat/memo-fintech-agents/charts/x402_02_cumulative_growth.png",
                facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    print("Saved charts/x402_02_cumulative_growth.png")


# =========================================================================
# Main
# =========================================================================

if __name__ == "__main__":
    build_chart_1()
    build_chart_2()
    print("Done -- both charts generated.")
