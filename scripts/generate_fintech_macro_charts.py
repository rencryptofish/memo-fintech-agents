"""
Generate additional fintech macro charts that are referenced in memos but were
not previously visualized.

Charts:
  1) fintech_market_size_projection.png
  2) fintech_vc_vs_deals_trend.png

Data source:
  - memos/fintech-market-analysis.md (sections: Global Market Sizing, Funding Trends)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "charts" / "fintech"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def chart_market_size_projection() -> None:
    """Fintech market size trajectory with anchor points from the memo."""
    # Anchor points from memo table (IMARC Group).
    anchor_years = np.array([2024, 2025, 2026, 2033], dtype=float)
    anchor_sizes = np.array([340.1, 394.9, 460.8, 828.4], dtype=float)

    # Interpolate intermediate years for readability only.
    years = np.arange(2024, 2034)
    sizes = np.interp(years, anchor_years, anchor_sizes)

    fig, ax = plt.subplots(figsize=(14, 8), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    ax.plot(years, sizes, color="#2563EB", linewidth=3, zorder=3)
    ax.scatter(anchor_years, anchor_sizes, s=80, color="#1D4ED8", edgecolor="white", linewidth=1.4, zorder=4)

    # Highlight the long forward gap (2027-2032 are interpolated).
    ax.axvspan(2026.5, 2032.5, color="#DBEAFE", alpha=0.45, zorder=0)
    ax.text(2029.5, 510, "Interpolated bridge\n(2027-2032)", ha="center", va="center",
            fontsize=9, color="#1E3A8A")

    ax.text(2024.1, 660, "Growth context:\nFintech revenue growth (2024): 21%\nTraditional banking growth: 6%",
            fontsize=10, color="#111827",
            bbox=dict(boxstyle="round,pad=0.45", facecolor="#F9FAFB", edgecolor="#D1D5DB"))

    labels = {
        2024: "$340.1B",
        2025: "$394.9B",
        2026: "$460.8B",
        2033: "$828.4B",
    }
    for yr, val in zip(anchor_years, anchor_sizes):
        ax.annotate(
            labels[int(yr)],
            xy=(yr, val),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            fontsize=10,
            color="#1E3A8A",
            fontweight="bold",
        )

    ax.set_title("Global Fintech Market Size Trajectory", fontsize=20, fontweight="bold", color="#111827", pad=16)
    ax.text(0.5, 1.02, "Anchor values from IMARC Group; CAGR quoted in memo: 15.8% (2025-2033)",
            transform=ax.transAxes, ha="center", fontsize=10, color="#6B7280")
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Market Size (USD Billions)", fontsize=12)
    ax.set_xticks(years)
    ax.grid(axis="y", alpha=0.2, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(300, 900)

    fig.text(
        0.5,
        0.01,
        "Source: memos/fintech-market-analysis.md (IMARC Group table).",
        ha="center",
        fontsize=9,
        color="#6B7280",
        style="italic",
    )
    fig.tight_layout(rect=[0, 0.03, 1, 0.96])
    out = OUT_DIR / "fintech_market_size_projection.png"
    fig.savefig(out, dpi=260, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {out}")


def chart_vc_vs_deals_trend() -> None:
    """Global fintech funding (USD B) versus deal count (dual-axis)."""
    years = np.array([2020, 2021, 2022, 2023, 2024, 2025])
    vc_usd_b = np.array([49.0, 131.5, 88.8, 46.3, 40.8, 51.8])
    deals = np.array([3491, 4969, 6492, 3819, 4639, np.nan], dtype=float)

    fig, ax1 = plt.subplots(figsize=(14, 8), dpi=180)
    fig.patch.set_facecolor("white")
    ax1.set_facecolor("white")

    bar_colors = ["#60A5FA", "#2563EB", "#3B82F6", "#93C5FD", "#93C5FD", "#38BDF8"]
    bars = ax1.bar(years, vc_usd_b, width=0.62, color=bar_colors, edgecolor="white", linewidth=1.0, zorder=3)

    for b, v in zip(bars, vc_usd_b):
        ax1.text(b.get_x() + b.get_width() / 2, b.get_height() + 2, f"${v:.1f}B",
                 ha="center", va="bottom", fontsize=9, color="#1E3A8A", fontweight="bold")

    ax2 = ax1.twinx()
    ax2.plot(years[:-1], deals[:-1], color="#DC2626", marker="o", linewidth=2.5, markersize=7, zorder=4)
    for yr, d in zip(years[:-1], deals[:-1]):
        ax2.text(yr, d + 170, f"{int(d):,}", ha="center", fontsize=9, color="#991B1B")

    ax2.scatter([2025], [deals[-2]], s=0)  # keep right-axis range stable
    ax2.text(2025, deals[-2] - 650, "Deals: N/A", ha="center", fontsize=9, color="#991B1B", style="italic")

    ax1.annotate("Peak mania",
                 xy=(2021, 131.5), xytext=(2020.55, 122),
                 arrowprops=dict(arrowstyle="->", color="#1E3A8A", lw=1.2),
                 fontsize=9, color="#1E3A8A")
    ax1.annotate("Funding winter",
                 xy=(2023, 46.3), xytext=(2022.5, 76),
                 arrowprops=dict(arrowstyle="->", color="#1E3A8A", lw=1.2),
                 fontsize=9, color="#1E3A8A")
    ax1.annotate("Recovery",
                 xy=(2025, 51.8), xytext=(2024.35, 82),
                 arrowprops=dict(arrowstyle="->", color="#1E3A8A", lw=1.2),
                 fontsize=9, color="#1E3A8A")

    ax1.set_title("Global Fintech VC Funding vs Deal Volume (2020-2025)", fontsize=20, fontweight="bold", color="#111827", pad=16)
    ax1.text(0.5, 1.02, "Bars: annual VC funding (USD billions)  |  Line: annual deal count",
             transform=ax1.transAxes, ha="center", fontsize=10, color="#6B7280")
    ax1.set_xlabel("Year", fontsize=12)
    ax1.set_ylabel("VC Funding (USD Billions)", fontsize=12, color="#1E3A8A")
    ax2.set_ylabel("Deal Count", fontsize=12, color="#991B1B")
    ax1.tick_params(axis="y", colors="#1E3A8A")
    ax2.tick_params(axis="y", colors="#991B1B")
    ax1.set_xticks(years)
    ax1.set_ylim(0, 150)
    ax2.set_ylim(3000, 7000)
    ax1.grid(axis="y", alpha=0.2, linestyle="--")
    ax1.spines["top"].set_visible(False)
    ax2.spines["top"].set_visible(False)

    fig.text(
        0.5,
        0.01,
        "Source: memos/fintech-market-analysis.md (Funding Trends table).",
        ha="center",
        fontsize=9,
        color="#6B7280",
        style="italic",
    )
    fig.tight_layout(rect=[0, 0.03, 1, 0.96])
    out = OUT_DIR / "fintech_vc_vs_deals_trend.png"
    fig.savefig(out, dpi=260, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    print("Generating additional fintech macro charts...")
    chart_market_size_projection()
    chart_vc_vs_deals_trend()
    print("Done.")
