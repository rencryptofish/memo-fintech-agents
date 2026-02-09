"""
Fintech Funding Visualizations
- Stacked bar chart: funding by fintech type by year
- Market map: treemap of current fintech landscape
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# DATA: VC-Only Funding by Fintech Category by Year ($B)
# Sources: KPMG Pulse of Fintech, CB Insights, Crunchbase, Gallagher Re,
#          Tracxn, FT Partners, Statista, The Block
# ─────────────────────────────────────────────────────────────────────────────

YEARS = list(range(2015, 2026))

# Using VC-focused figures (excluding mega M&A like FIS/Worldpay)
CATEGORIES = {
    "Payments": {
        2015: 6.0, 2016: 7.5, 2017: 7.0, 2018: 12.0, 2019: 10.0,
        2020: 12.0, 2021: 29.0, 2022: 20.0, 2023: 10.0, 2024: 14.0, 2025: 14.0,
    },
    "Crypto / Blockchain": {
        2015: 0.5, 2016: 0.6, 2017: 3.0, 2018: 4.5, 2019: 4.7,
        2020: 5.5, 2021: 30.2, 2022: 23.1, 2023: 8.0, 2024: 13.7, 2025: 18.0,
    },
    "Lending / Credit": {
        2015: 6.0, 2016: 5.5, 2017: 5.0, 2018: 6.5, 2019: 5.5,
        2020: 8.0, 2021: 18.5, 2022: 12.0, 2023: 7.5, 2024: 6.0, 2025: 7.0,
    },
    "Insurtech": {
        2015: 2.6, 2016: 1.7, 2017: 3.0, 2018: 4.2, 2019: 6.4,
        2020: 7.5, 2021: 14.4, 2022: 8.6, 2023: 4.5, 2024: 4.2, 2025: 5.0,
    },
    "B2B Infrastructure": {
        2015: 2.0, 2016: 2.5, 2017: 3.0, 2018: 5.0, 2019: 5.5,
        2020: 7.0, 2021: 18.0, 2022: 12.0, 2023: 10.0, 2024: 8.0, 2025: 10.0,
    },
    "Neobanks": {
        2015: 1.5, 2016: 2.0, 2017: 3.5, 2018: 5.0, 2019: 7.0,
        2020: 5.5, 2021: 14.0, 2022: 8.0, 2023: 5.0, 2024: 3.5, 2025: 4.5,
    },
    "Regtech": {
        2015: 0.6, 2016: 0.8, 2017: 1.2, 2018: 3.7, 2019: 5.0,
        2020: 7.0, 2021: 11.8, 2022: 18.6, 2023: 4.4, 2024: 7.4, 2025: 5.0,
    },
    "Embedded Finance": {
        2015: 0.3, 2016: 0.5, 2017: 0.8, 2018: 1.5, 2019: 2.0,
        2020: 3.5, 2021: 11.2, 2022: 6.5, 2023: 3.5, 2024: 3.0, 2025: 4.0,
    },
    "Wealthtech": {
        2015: 2.0, 2016: 2.5, 2017: 2.0, 2018: 4.0, 2019: 3.5,
        2020: 3.0, 2021: 6.0, 2022: 4.5, 2023: 2.5, 2024: 2.8, 2025: 3.5,
    },
    "BNPL": {
        2015: 0.1, 2016: 0.2, 2017: 0.4, 2018: 0.8, 2019: 1.1,
        2020: 1.5, 2021: 5.0, 2022: 2.5, 2023: 1.0, 2024: 0.8, 2025: 1.2,
    },
}

# VC-only totals for reference line
VC_TOTALS = {
    2015: 19.4, 2016: 24.0, 2017: 27.4, 2018: 40.1, 2019: 37.9,
    2020: 45.7, 2021: 121.5, 2022: 88.8, 2023: 46.3, 2024: 43.4, 2025: 51.8,
}

# Color palette - distinct, colorblind-friendly-ish
COLORS = {
    "Payments":           "#2563EB",
    "Crypto / Blockchain":"#F59E0B",
    "Lending / Credit":   "#7C3AED",
    "Insurtech":          "#10B981",
    "B2B Infrastructure": "#8B5CF6",
    "Neobanks":           "#06B6D4",
    "Regtech":            "#6366F1",
    "Embedded Finance":   "#14B8A6",
    "Wealthtech":         "#EC4899",
    "BNPL":               "#EF4444",
}


def chart1_stacked_bar():
    """Stacked bar chart: fintech funding by category by year."""
    fig, ax = plt.subplots(figsize=(20, 11))

    cat_names = list(CATEGORIES.keys())
    bottom = np.zeros(len(YEARS))

    for cat in cat_names:
        values = [CATEGORIES[cat][y] for y in YEARS]
        bars = ax.bar(
            YEARS, values, bottom=bottom,
            label=cat, color=COLORS[cat],
            width=0.7, edgecolor="white", linewidth=0.3,
        )
        bottom += np.array(values)

    # VC total reference line
    vc_vals = [VC_TOTALS[y] for y in YEARS]
    ax.plot(YEARS, vc_vals, "k--", linewidth=2.5, alpha=0.6,
            label="VC-Only Total (reference)", zorder=10)
    for y, v in zip(YEARS, vc_vals):
        ax.annotate(f"${v:.0f}B", (y, v), textcoords="offset points",
                    xytext=(0, 9), ha="center", fontsize=8.8, color="#333",
                    fontweight="bold")

    # Styling
    ax.set_title(
        "Global Fintech VC Funding by Category (2015-2025)",
        fontsize=22, fontweight="bold", pad=22, color="#1a1a2e",
    )
    ax.set_xlabel("Year", fontsize=15, labelpad=10)
    ax.set_ylabel("Funding ($ Billions)", fontsize=15, labelpad=10)
    ax.set_xticks(YEARS)
    ax.set_xticklabels(YEARS, fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%.0fB"))
    ax.tick_params(axis="y", labelsize=11)

    # Annotations for key events
    annotations = [
        (2019, "FIS/Worldpay\n& Fiserv M&A era", 65),
        (2021, "Peak Mania\n$131.5B total VC", 175),
        (2022, "FTX Collapse\nRate Hikes Begin", 130),
        (2023, "Funding Winter", 65),
        (2025, "AI & Stablecoin\nRecovery", 85),
    ]
    for yr, text, y_pos in annotations:
        ax.annotate(
            text, xy=(yr, y_pos), fontsize=9, ha="center",
            color="#555", style="italic",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#f0f0f0",
                      edgecolor="#ccc", alpha=0.9),
        )

    # Legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles[::-1], labels[::-1],
        loc="upper left", fontsize=10.5, ncol=2,
        framealpha=0.95, edgecolor="#ddd",
        title="Fintech Category", title_fontsize=11,
    )

    ax.set_xlim(2014.4, 2025.6)
    ax.grid(axis="y", alpha=0.2, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Source note
    fig.text(
        0.5, 0.01,
        "Sources: KPMG Pulse of Fintech, CB Insights, Crunchbase, The Block, "
        "Gallagher Re, Tracxn, FT Partners, Statista  |  Note: Categories overlap; "
        "sum exceeds VC total",
        ha="center", fontsize=9, color="#888", style="italic",
    )

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    return fig


def chart2_market_map():
    """Treemap-style market map of the fintech landscape."""
    fig, ax = plt.subplots(figsize=(22, 13))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")

    # Title
    fig.suptitle(
        "Fintech Market Map: Categories, Key Players & 2025 Funding",
        fontsize=22, fontweight="bold", color="#1a1a2e", y=0.97,
    )

    # Market map data: (category, 2025 funding $B, key companies, color, status)
    segments = [
        # Row 1 (top) - largest categories
        {
            "name": "Payments", "funding": "$14.0B", "status": "Mature / Growing",
            "companies": "Stripe ($106.7B) | Adyen | Square\nCheckout.com | Wise | PayPal",
            "color": "#2563EB", "rect": (0, 72, 35, 28),
        },
        {
            "name": "Crypto / Blockchain", "funding": "$18.0B", "status": "Recovering",
            "companies": "Coinbase | Binance | Circle\nChainalysis | Stablecoins ($300B+)",
            "color": "#F59E0B", "rect": (36, 72, 30, 28),
        },
        {
            "name": "B2B Infrastructure", "funding": "$10.0B", "status": "Strong Growth",
            "companies": "Plaid ($6.1B) | Marqeta\nMX | Thought Machine | Unit",
            "color": "#8B5CF6", "rect": (67, 72, 33, 28),
        },
        # Row 2
        {
            "name": "Lending / Credit", "funding": "$7.0B", "status": "Recovering",
            "companies": "SoFi | Upstart | Creditas\nKabbage (AmEx) | Funding Circle",
            "color": "#7C3AED", "rect": (0, 44, 28, 27),
        },
        {
            "name": "Neobanks", "funding": "$4.5B", "status": "Consolidating",
            "companies": "Nubank (118.6M users) | Revolut ($75B)\nChime ($18.4B IPO) | Monzo | N26",
            "color": "#06B6D4", "rect": (29, 44, 28, 27),
        },
        {
            "name": "Insurtech", "funding": "$5.0B", "status": "Maturing",
            "companies": "Lemonade | Root | Oscar\nHippo | Wefox",
            "color": "#10B981", "rect": (58, 44, 21, 27),
        },
        {
            "name": "Regtech", "funding": "$5.0B", "status": "Growing",
            "companies": "Chainalysis | Onfido\nTrulioo | Fenergo",
            "color": "#6366F1", "rect": (80, 44, 20, 27),
        },
        # Row 3 (bottom)
        {
            "name": "Embedded Finance / BaaS", "funding": "$4.0B", "status": "Rebuilding",
            "companies": "Plaid | Treasury Prime | Solaris\nUnit | Synctera | (Synapse failed)",
            "color": "#14B8A6", "rect": (0, 16, 30, 27),
        },
        {
            "name": "Wealthtech", "funding": "$3.5B", "status": "Stable",
            "companies": "Betterment | Wealthfront (IPO)\nRobinhood (S&P 500) | eToro",
            "color": "#EC4899", "rect": (31, 16, 25, 27),
        },
        {
            "name": "BNPL", "funding": "$1.2B", "status": "Post-Correction",
            "companies": "Klarna ($14B IPO) | Affirm\nAfterPay (Block) | Sezzle",
            "color": "#EF4444", "rect": (57, 16, 20, 27),
        },
        {
            "name": "AI-Native Fintech\n(Emerging)", "funding": "$2.0B+", "status": "Nascent / Hot",
            "companies": "Catena Labs | Crossmint | Kira\nCFO Stack: $1.8B across 90 deals",
            "color": "#0F172A", "rect": (78, 16, 22, 27),
        },
    ]

    for seg in segments:
        x, y, w, h = seg["rect"]
        # Background rectangle
        rect = mpatches.FancyBboxPatch(
            (x + 0.4, y + 0.4), w - 0.8, h - 0.8,
            boxstyle="round,pad=0.5",
            facecolor=seg["color"], edgecolor="white",
            linewidth=2, alpha=0.88,
        )
        ax.add_patch(rect)

        cx, cy = x + w / 2, y + h / 2

        # Category name
        ax.text(
            cx, cy + h * 0.28, seg["name"],
            ha="center", va="center", fontsize=14.5, fontweight="bold",
            color="white", family="sans-serif",
            path_effects=[pe.withStroke(linewidth=2, foreground="#0f172a", alpha=0.6)],
        )

        # Funding amount and status
        ax.text(
            cx, cy + h * 0.08, f'{seg["funding"]}  •  {seg["status"]}',
            ha="center", va="center", fontsize=10,
            color=(1, 1, 1, 0.95), family="sans-serif",
            path_effects=[pe.withStroke(linewidth=1.8, foreground="#0f172a", alpha=0.55)],
        )

        # Companies
        company_font = 9.2 if w >= 28 else 8.4
        ax.text(
            cx, cy - h * 0.18, seg["companies"],
            ha="center", va="center", fontsize=company_font,
            color=(1, 1, 1, 0.95), family="monospace",
            linespacing=1.45,
            path_effects=[pe.withStroke(linewidth=1.5, foreground="#0f172a", alpha=0.55)],
        )

    # Bottom bar with summary stats (two rows for readability).
    stats_y_top = 6
    stats_y_bottom = 2.8
    stats = [
        "Total VC 2025: $51.8B",
        "69% of public fintechs profitable",
        "326 fintech unicorns globally",
        "AI adoption: 88% of top fintechs",
        "Stablecoins: $300B+ circulation",
    ]
    top_stats = stats[:3]
    bottom_stats = stats[3:]
    for i, stat in enumerate(top_stats):
        ax.text(
            17 + i * 33, stats_y_top, stat, ha="center", va="center",
            fontsize=9.8, fontweight="bold", color="#333",
            bbox=dict(boxstyle="round,pad=0.42", facecolor="#f0f4ff",
                      edgecolor="#ccc", alpha=0.92),
        )
    for i, stat in enumerate(bottom_stats):
        ax.text(
            26 + i * 36, stats_y_bottom, stat, ha="center", va="center",
            fontsize=9.8, fontweight="bold", color="#333",
            bbox=dict(boxstyle="round,pad=0.42", facecolor="#f0f4ff",
                      edgecolor="#ccc", alpha=0.92),
        )

    fig.text(
        0.5, 0.01,
        "Sources: BCG/QED 2025, CB Insights, PitchBook, Crunchbase  |  "
        "Funding figures are 2025 VC estimates  |  Valuations as of latest round",
        ha="center", fontsize=9, color="#888", style="italic",
    )

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    return fig


def chart3_heatmap():
    """Heatmap showing funding intensity by category and year."""
    fig, ax = plt.subplots(figsize=(20, 10))

    cat_names = list(CATEGORIES.keys())
    data = np.array([[CATEGORIES[cat][y] for y in YEARS] for cat in cat_names])

    im = ax.imshow(data, cmap="YlOrRd", aspect="auto", interpolation="nearest")

    ax.set_xticks(range(len(YEARS)))
    ax.set_xticklabels(YEARS, fontsize=12)
    ax.set_yticks(range(len(cat_names)))
    ax.set_yticklabels(cat_names, fontsize=12)

    # Value labels in each cell
    for i in range(len(cat_names)):
        for j in range(len(YEARS)):
            val = data[i, j]
            text_color = "white" if val > 12 else "black"
            ax.text(j, i, f"${val:.1f}B", ha="center", va="center",
                    fontsize=8.8, color=text_color, fontweight="bold")

    cbar = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label("Funding ($ Billions)", fontsize=12)

    ax.set_title(
        "Fintech Funding Heatmap by Category & Year (2015-2025)",
        fontsize=20, fontweight="bold", pad=16, color="#1a1a2e",
    )

    # Highlight peak year per category
    for i in range(len(cat_names)):
        peak_j = np.argmax(data[i])
        ax.add_patch(plt.Rectangle(
            (peak_j - 0.5, i - 0.5), 1, 1,
            fill=False, edgecolor="#000", linewidth=2.5,
        ))

    fig.text(
        0.5, 0.01,
        "Black borders indicate peak funding year per category  |  "
        "Sources: KPMG, CB Insights, Crunchbase, Gallagher Re, Tracxn, The Block",
        ha="center", fontsize=9, color="#888", style="italic",
    )

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    return fig


def chart4_stacked_percent_mix():
    """
    100% stacked bar chart:
    fintech funding mix by category by year (category-share shift over time).

    Note: each year is normalized to 100% of the summed category bucket values.
    This shows composition shift, not absolute market size.
    """
    fig, ax = plt.subplots(figsize=(20, 11))

    # Add AI-native / agentic slice to make the recent mix-shift visible.
    # Conservative estimates based on memo references (emerging through 2023,
    # then accelerating in 2024-2025).
    ai_native_agentic = {
        2015: 0.0, 2016: 0.0, 2017: 0.05, 2018: 0.08, 2019: 0.10,
        2020: 0.20, 2021: 0.45, 2022: 0.60, 2023: 0.80, 2024: 1.20, 2025: 2.00,
    }

    mix_categories = list(CATEGORIES.keys()) + ["AI-Native / Agentic Fintech"]
    mix_colors = {**COLORS, "AI-Native / Agentic Fintech": "#111827"}
    mix_values = {**CATEGORIES, "AI-Native / Agentic Fintech": ai_native_agentic}

    # Build matrix: rows=categories, cols=years
    raw = np.array([[mix_values[cat][y] for y in YEARS] for cat in mix_categories], dtype=float)
    year_sums = raw.sum(axis=0)
    pct = np.divide(raw, year_sums, out=np.zeros_like(raw), where=year_sums > 0) * 100.0

    bottom = np.zeros(len(YEARS))
    for i, cat in enumerate(mix_categories):
        vals = pct[i]
        ax.bar(
            YEARS, vals, bottom=bottom, width=0.72,
            color=mix_colors[cat], label=cat,
            edgecolor="white", linewidth=0.25,
        )
        bottom += vals

    # Styling
    ax.set_ylim(0, 100)
    ax.set_xlim(2014.4, 2025.6)
    ax.set_xticks(YEARS)
    ax.set_xticklabels(YEARS, fontsize=12)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=100))
    ax.tick_params(axis="y", labelsize=12)
    ax.set_xlabel("Year", fontsize=15, labelpad=10)
    ax.set_ylabel("Share of Category Funding Mix (%)", fontsize=15, labelpad=10)
    ax.set_title(
        "Fintech Funding Mix Shift by Category (100% Stacked, 2015-2025)",
        fontsize=22, fontweight="bold", pad=20, color="#1a1a2e",
    )

    ax.text(
        0.5, 1.02,
        "Each year normalized to 100% of summed category buckets; labels above bars show VC-only total for scale context",
        transform=ax.transAxes, ha="center", fontsize=11, color="#666",
    )

    # Add VC-only total labels on top for context (absolute scale).
    for y in YEARS:
        total = VC_TOTALS[y]
        ax.annotate(
            f"${total:.0f}B",
            xy=(y, 100), xytext=(0, 5), textcoords="offset points",
            ha="center", va="bottom", fontsize=9, color="#333", fontweight="bold",
        )

    # Key regime markers
    ax.axvline(2021, color="#555", linestyle="--", linewidth=1.1, alpha=0.6)
    ax.axvline(2023, color="#555", linestyle="--", linewidth=1.1, alpha=0.6)
    ax.text(2021, 3, "Peak", fontsize=9, color="#555", ha="center", va="bottom")
    ax.text(2023, 3, "Trough", fontsize=9, color="#555", ha="center", va="bottom")

    # Legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles[::-1], labels[::-1],
        loc="upper left", bbox_to_anchor=(1.01, 1.0),
        fontsize=10, framealpha=0.95, edgecolor="#ddd",
        title="Category", title_fontsize=11,
    )

    ax.grid(axis="y", alpha=0.18, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.text(
        0.5, 0.01,
        "Sources: KPMG Pulse, CB Insights, Crunchbase, fintech-market-analysis.md  |  "
        "AI-Native / Agentic slice is an estimated emerging bucket for mix-shift readability",
        ha="center", fontsize=9, color="#888", style="italic",
    )

    plt.tight_layout(rect=[0, 0.03, 0.86, 1])
    return fig


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "charts" / "fintech"

    print("Generating Chart 1: Stacked Bar Chart...")
    fig1 = chart1_stacked_bar()
    fig1.savefig(out / "fintech_funding_by_category.png", dpi=260, bbox_inches="tight",
                 facecolor="white")
    print(f"  Saved: {out / 'fintech_funding_by_category.png'}")

    print("Generating Chart 2: Market Map...")
    fig2 = chart2_market_map()
    fig2.savefig(out / "fintech_market_map.png", dpi=260, bbox_inches="tight",
                 facecolor="white")
    print(f"  Saved: {out / 'fintech_market_map.png'}")

    print("Generating Chart 3: Heatmap...")
    fig3 = chart3_heatmap()
    fig3.savefig(out / "fintech_funding_heatmap.png", dpi=260, bbox_inches="tight",
                 facecolor="white")
    print(f"  Saved: {out / 'fintech_funding_heatmap.png'}")

    print("Generating Chart 4: 100% Stacked Mix Shift...")
    fig4 = chart4_stacked_percent_mix()
    fig4.savefig(out / "fintech_funding_mix_percent_by_category.png", dpi=260,
                 bbox_inches="tight", facecolor="white")
    print(f"  Saved: {out / 'fintech_funding_mix_percent_by_category.png'}")

    print("\nAll charts generated successfully!")
    plt.close("all")
