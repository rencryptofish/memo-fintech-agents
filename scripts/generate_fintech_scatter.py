"""
Fintech: Funding vs Revenue Trajectory by Category (2019-2026)
Scatter plot with connected lines showing each category's evolution
through the boom/bust/recovery cycle.

X-axis: Cumulative VC raised by top companies in category ($B)
Y-axis: Combined estimated revenue of top companies ($M)
Lines connect each category across 4 time snapshots.
"""

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
from matplotlib.lines import Line2D
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# DATA: Fintech Categories — Top-Company Funding & Revenue at Snapshots
#
# Sources: fintech-market-analysis.md, fintech-investment-opportunities-2026.md,
#          Crunchbase, PitchBook, SEC filings, company earnings reports
#
# Funding = cumulative VC raised by top 3-5 companies in category
# Revenue = combined annual revenue/ARR of those companies
# ─────────────────────────────────────────────────────────────────────────────

TIME_POINTS = ["End 2019", "End 2021", "End 2023", "Early 2026"]
TIME_POINT_SHORT = ["2019", "2021", "2023", "2026"]
TIME_POINT_MARKERS = ["o", "s", "D", "^"]

# {category: [(funding_B, revenue_M), ...]} — one tuple per time point
CATEGORIES = {
    "B2B Payments\n(Stripe, Adyen, Checkout)": [
        # 2019: Stripe ~$1.6B raised, ~$1.5B rev; Adyen ~€200M raised (pre-IPO), ~€500M rev;
        #   Checkout.com ~$230M raised, ~$200M rev
        (2.0, 2200),
        # 2021: Stripe ~$4.4B raised, ~$3B net rev; Checkout.com ~$830M raised;
        #   Adyen public (€500M rev)
        (5.5, 5500),
        # 2023: Stripe ~$8.7B raised (incl $6.5B secondary), ~$4B net rev;
        #   Checkout.com ~$1.8B raised; Plaid $750M raised, $300M ARR
        (11.5, 8500),
        # 2026: Stripe $5.1B net rev (+28% YoY → ~$6.5B); Checkout.com ~$1.2B;
        #   Plaid $390M ARR. Stripe dominates.
        (12.0, 13000),
    ],
    "Neobanks\n(Nubank, Revolut, Chime)": [
        # 2019: Nubank ~$1.4B raised, ~$1B rev; Revolut ~$840M raised, ~$200M rev;
        #   Chime ~$800M raised, ~$200M rev; Monzo ~$400M raised
        (3.5, 1500),
        # 2021: Nubank IPO ($2.3B raised, ~$4B rev); Revolut ~$1.7B raised, ~$1B;
        #   Chime $2.3B raised, ~$800M rev
        (6.5, 6000),
        # 2023: Minimal new VC (most raised or public); Nubank ~$8B rev;
        #   Revolut ~$2.5B; Chime ~$1.3B
        (8.0, 12500),
        # 2026: Nubank $11.5B rev; Revolut $4B; Chime $1.67B; Monzo £113.9M profit
        (8.5, 18000),
    ],
    "Crypto / Blockchain\n(Coinbase, Circle, Chainalysis)": [
        # 2019: Coinbase ~$550M raised, ~$500M rev; Circle ~$250M raised;
        #   Chainalysis ~$50M raised
        (0.85, 550),
        # 2021: Coinbase IPO ($550M raised, ~$7.8B rev — peak); Circle ~$440M;
        #   Chainalysis ~$370M raised
        (1.4, 8500),
        # 2023: Crypto winter; Coinbase ~$3B rev (down from $7.8B); Circle ~$1.5B rev;
        #   Chainalysis ~$200M ARR
        (1.6, 5000),
        # 2026: Coinbase recovering ~$4-5B rev; Circle $2.6B projected;
        #   Chainalysis ~$300M ARR
        (2.0, 7500),
    ],
    "BNPL\n(Klarna, Affirm)": [
        # 2019: Klarna ~$1.6B raised, ~$800M rev; Affirm ~$800M raised, ~$300M rev
        (2.4, 1100),
        # 2021: Klarna $3.5B+ raised ($45.6B val), ~$1.5B rev; Affirm IPO, ~$900M
        (4.5, 2400),
        # 2023: Klarna valuation crashed to $6.7B; ~$2B rev; Affirm ~$1.6B rev
        (5.0, 3600),
        # 2026: Klarna IPO at $14B, ~$3B rev; Affirm ~$2.5B rev
        (5.5, 5500),
    ],
    "CFO Stack\n(Ramp, Brex, Mercury)": [
        # 2019: Brex ~$300M raised, ~$50M rev; Ramp just founded; Mercury early
        (0.35, 60),
        # 2021: Brex ~$1B raised, ~$200M rev; Ramp ~$400M raised, ~$100M;
        #   Mercury ~$100M raised, ~$50M
        (1.5, 350),
        # 2023: Ramp ~$800M raised, ~$500M rev; Brex ~$1.2B raised, ~$500M;
        #   Mercury ~$160M raised, ~$400M
        (2.5, 1400),
        # 2026: Ramp $1.6B+ raised, $1B annualized rev; Mercury $650M rev;
        #   Brex $700M (being acquired by Capital One $5.15B)
        (3.5, 2350),
    ],
    "Insurtech\n(Lemonade, Root, Oscar)": [
        # 2019: Lemonade ~$480M raised, ~$100M rev; Oscar ~$1.3B raised, ~$500M;
        #   Root ~$525M raised, ~$400M
        (2.3, 1000),
        # 2021: All IPO'd; combined ~$3B rev; significant new capital raised
        (4.5, 3000),
        # 2023: Stock prices crashed 70-90%; combined rev ~$4B but heavy losses
        (5.0, 4000),
        # 2026: Maturing; Oscar ~$6.5B rev; Lemonade ~$500M; Root ~$700M
        (5.5, 7500),
    ],
    "Lending / Credit\n(SoFi, Upstart)": [
        # 2019: SoFi ~$2.5B raised, ~$500M rev; Upstart ~$160M raised, ~$160M;
        #   LendingClub ~$400M raised
        (3.0, 900),
        # 2021: SoFi SPAC ($8.6B), ~$1B rev; Upstart IPO, ~$850M rev
        (3.5, 2000),
        # 2023: Rate hikes hit hard; SoFi ~$2.1B rev; Upstart ~$500M (crashed)
        (3.5, 2600),
        # 2026: SoFi ~$2.7B rev; Upstart recovering (62.8% growth); LendingClub ~$1B
        (3.5, 4500),
    ],
    "Wealthtech\n(Robinhood, eToro)": [
        # 2019: Robinhood ~$860M raised, ~$280M rev; eToro growing
        (1.2, 500),
        # 2021: Robinhood IPO, ~$1.8B rev (peak meme stocks); eToro ~$600M
        (3.5, 2400),
        # 2023: Robinhood ~$1.9B rev; eToro ~$500M; down from peaks
        (3.5, 2400),
        # 2026: Robinhood ~$3B+ rev (S&P 500 inclusion); eToro growing
        (3.5, 3500),
    ],
    "Cross-Border\n(Wise, Remitly)": [
        # 2019: Wise (TransferWise) ~$400M raised, ~$300M rev; Remitly ~$400M raised
        (0.8, 500),
        # 2021: Wise IPO (~$1B rev); Remitly IPO; Nium growing
        (1.0, 1500),
        # 2023: Wise ~$1.3B rev; Remitly ~$900M rev
        (1.2, 2200),
        # 2026: Wise ~$2B+ rev (£495M operating income); Remitly ~$1.2B
        (1.5, 3200),
    ],
    "Embedded Finance\n(Marqeta, Lithic, Unit)": [
        # 2019: Marqeta ~$300M raised, ~$200M rev; Unit, Lithic very early
        (0.4, 250),
        # 2021: Marqeta IPO (~$500M rev); Unit, Lithic, Synctera raised
        (1.2, 700),
        # 2023: Marqeta ~$700M rev; Synapse collapsed; BaaS under pressure
        (1.5, 800),
        # 2026: Marqeta ~$800M rev; Lithic $800M val; Synctera surviving;
        #   post-Synapse BaaS 2.0 emerging
        (1.8, 1000),
    ],
    "Regtech\n(Chainalysis, ComplyAdv)": [
        # 2019: Chainalysis ~$50M raised; ComplyAdvantage ~$50M; early category
        (0.15, 60),
        # 2021: Chainalysis ~$370M raised, ~$100M ARR; ComplyAdvantage growing
        (0.6, 250),
        # 2023: Chainalysis ~$540M raised; valuation cut; ~$200M ARR
        (0.7, 350),
        # 2026: Growing with regulation; GENIUS Act driving demand
        (0.9, 500),
    ],
    "Stablecoin Infra\n(Circle, Bridge, BVNK)": [
        # 2019: Circle ~$250M raised; stablecoins < $5B circulation; minimal rev
        (0.3, 30),
        # 2021: Circle ~$440M raised; USDC $42B circ; Circle ~$400M rev
        (0.5, 450),
        # 2023: USDC ~$24B circ (down from peak); Circle ~$1.5B rev (interest)
        (0.6, 1600),
        # 2026: Circle IPO, $2.6B rev; Bridge acquired $1.1B; BVNK $50M raised;
        #   $300B+ stablecoin circulation
        (1.0, 3000),
    ],
    "Agentic Fintech Intersection\n(Payments, Wallets, Identity)": [
        # 2019: effectively pre-category; minimal investment and revenue
        (0.005, 1),
        # 2021: early pilots and tooling; still tiny compared with core fintech
        (0.020, 3),
        # 2023: pre-inflection, category taking shape but still early
        (0.090, 12),
        # 2026: meaningful funding velocity with still-early revenue base
        # (memo estimate: ~$1.1B+ startup funding across intersection layers)
        (1.100, 90),
    ],
}

# Colors
COLORS = {
    "B2B Payments\n(Stripe, Adyen, Checkout)":      "#2563EB",
    "Neobanks\n(Nubank, Revolut, Chime)":            "#06B6D4",
    "Crypto / Blockchain\n(Coinbase, Circle, Chainalysis)": "#F59E0B",
    "BNPL\n(Klarna, Affirm)":                        "#EF4444",
    "CFO Stack\n(Ramp, Brex, Mercury)":              "#8B5CF6",
    "Insurtech\n(Lemonade, Root, Oscar)":            "#10B981",
    "Lending / Credit\n(SoFi, Upstart)":             "#7C3AED",
    "Wealthtech\n(Robinhood, eToro)":                "#EC4899",
    "Cross-Border\n(Wise, Remitly)":                 "#0EA5E9",
    "Embedded Finance\n(Marqeta, Lithic, Unit)":     "#14B8A6",
    "Regtech\n(Chainalysis, ComplyAdv)":             "#6366F1",
    "Stablecoin Infra\n(Circle, Bridge, BVNK)":     "#0F172A",
    "Agentic Fintech Intersection\n(Payments, Wallets, Identity)": "#334155",
}

MARKER_SIZES = [30, 60, 100, 180]

# Category metadata used for clearer cohort and start-year context
CATEGORY_META = {
    "B2B Payments\n(Stripe, Adyen, Checkout)": {
        "cohort": "Early Internet (1998-2007)",
        "start_year": 1998,
        "short": "B2B Payments",
    },
    "Neobanks\n(Nubank, Revolut, Chime)": {
        "cohort": "Neobank Wave (2013-2016)",
        "start_year": 2013,
        "short": "Neobanks",
    },
    "Crypto / Blockchain\n(Coinbase, Circle, Chainalysis)": {
        "cohort": "Post-Crisis + Crypto (2009-2013)",
        "start_year": 2012,
        "short": "Crypto / Blockchain",
    },
    "BNPL\n(Klarna, Affirm)": {
        "cohort": "Early Internet (1998-2007)",
        "start_year": 2005,
        "short": "BNPL",
    },
    "CFO Stack\n(Ramp, Brex, Mercury)": {
        "cohort": "CFO Platform Wave (2017-2020)",
        "start_year": 2017,
        "short": "CFO Stack",
    },
    "Insurtech\n(Lemonade, Root, Oscar)": {
        "cohort": "Neobank Wave (2013-2016)",
        "start_year": 2015,
        "short": "Insurtech",
    },
    "Lending / Credit\n(SoFi, Upstart)": {
        "cohort": "Early Internet (1998-2007)",
        "start_year": 2006,
        "short": "Lending / Credit",
    },
    "Wealthtech\n(Robinhood, eToro)": {
        "cohort": "Post-Crisis + Crypto (2009-2013)",
        "start_year": 2013,
        "short": "Wealthtech",
    },
    "Cross-Border\n(Wise, Remitly)": {
        "cohort": "Post-Crisis + Crypto (2009-2013)",
        "start_year": 2011,
        "short": "Cross-Border",
    },
    "Embedded Finance\n(Marqeta, Lithic, Unit)": {
        "cohort": "API / Open Banking (2016-2019)",
        "start_year": 2016,
        "short": "Embedded Finance",
    },
    "Regtech\n(Chainalysis, ComplyAdv)": {
        "cohort": "API / Open Banking (2016-2019)",
        "start_year": 2014,
        "short": "Regtech",
    },
    "Stablecoin Infra\n(Circle, Bridge, BVNK)": {
        "cohort": "CFO Platform Wave (2017-2020)",
        "start_year": 2018,
        "short": "Stablecoin Infra",
    },
    "Agentic Fintech Intersection\n(Payments, Wallets, Identity)": {
        "cohort": "AI x Fintech (2024+)",
        "start_year": 2024,
        "short": "Agentic Fintech Intersection",
    },
}

COHORT_ORDER = [
    "Early Internet (1998-2007)",
    "Post-Crisis + Crypto (2009-2013)",
    "Neobank Wave (2013-2016)",
    "API / Open Banking (2016-2019)",
    "CFO Platform Wave (2017-2020)",
    "AI x Fintech (2024+)",
]


def _format_axes(ax):
    ax.set_xscale("log")
    ax.set_yscale("log")

    x_ticks = [0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 15]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([f"${v}B" if v >= 1 else f"${int(v*1000)}M" for v in x_ticks],
                       fontsize=9)

    y_ticks = [1, 2, 5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 20000]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(
        [f"${v}M" if v < 1000 else f"${v/1000:.0f}B" for v in y_ticks],
        fontsize=9,
    )

    ax.set_xlim(0.004, 20)
    ax.set_ylim(0.8, 30000)
    ax.grid(True, alpha=0.16, which="both", linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def _draw_category_series(ax, cat_name, points, label_final=True, label_years=False):
    color = COLORS[cat_name]
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    # Trajectory line
    line_width = 2.8 if "Agentic Fintech Intersection" in cat_name else 2
    line_alpha = 0.9 if "Agentic Fintech Intersection" in cat_name else 0.55
    ax.plot(xs, ys, color=color, linewidth=line_width, alpha=line_alpha, zorder=1)

    # Arrowed flow between snapshots
    for i in range(len(xs) - 1):
        ax.annotate(
            "", xy=(xs[i + 1], ys[i + 1]), xytext=(xs[i], ys[i]),
            arrowprops=dict(
                arrowstyle="-|>", color=color, lw=1.4,
                mutation_scale=10, alpha=0.45,
            ),
            zorder=1,
        )

    # Year markers
    for i, (x, y) in enumerate(points):
        ax.scatter(
            x, y, s=MARKER_SIZES[i], color=color,
            edgecolors="white", linewidth=1, zorder=3,
            marker=TIME_POINT_MARKERS[i],
        )
        if label_years:
            ax.annotate(
                TIME_POINT_SHORT[i],
                xy=(x, y), xytext=(0, 7), textcoords="offset points",
                ha="center", fontsize=7, color="#555", zorder=4,
            )

    # Start-year label at first point
    start_year = CATEGORY_META[cat_name]["start_year"]
    ax.annotate(
        f"start {start_year}",
        xy=(xs[0], ys[0]), xytext=(-8, -10), textcoords="offset points",
        fontsize=7, color="#666", style="italic", zorder=4,
    )

    # Final label
    if label_final:
        label = CATEGORY_META[cat_name]["short"]
        offsets = {
            "B2B Payments\n(Stripe, Adyen, Checkout)":      (10, 6),
            "Neobanks\n(Nubank, Revolut, Chime)":            (-14, 10),
            "Crypto / Blockchain\n(Coinbase, Circle, Chainalysis)": (10, 6),
            "BNPL\n(Klarna, Affirm)":                        (10, -10),
            "CFO Stack\n(Ramp, Brex, Mercury)":              (10, 6),
            "Insurtech\n(Lemonade, Root, Oscar)":            (10, -10),
            "Lending / Credit\n(SoFi, Upstart)":             (-14, -11),
            "Wealthtech\n(Robinhood, eToro)":                (10, -10),
            "Cross-Border\n(Wise, Remitly)":                 (-14, 6),
            "Embedded Finance\n(Marqeta, Lithic, Unit)":     (10, 6),
            "Regtech\n(Chainalysis, ComplyAdv)":             (8, -11),
            "Stablecoin Infra\n(Circle, Bridge, BVNK)":      (-14, -11),
            "Agentic Fintech Intersection\n(Payments, Wallets, Identity)": (10, 10),
        }
        dx, dy = offsets.get(cat_name, (9, 5))
        ax.annotate(
            label, xy=(xs[-1], ys[-1]),
            xytext=(dx, dy), textcoords="offset points",
            fontsize=8.5, fontweight="bold", color=color,
            path_effects=[pe.withStroke(linewidth=3, foreground="white")],
            zorder=5,
        )


def _add_time_legend(ax, loc="lower right"):
    handles = [
        Line2D([0], [0], marker=TIME_POINT_MARKERS[i], color="#666", linestyle="",
               markerfacecolor="#888", markeredgecolor="white", markersize=7 + i,
               label=f"{TIME_POINTS[i]} ({TIME_POINT_SHORT[i]})")
        for i in range(len(TIME_POINTS))
    ]
    legend = ax.legend(
        handles=handles, loc=loc, fontsize=9, title="Snapshot Markers",
        title_fontsize=10, framealpha=0.95, edgecolor="#ddd",
    )
    ax.add_artist(legend)


def generate_scatter():
    fig, ax = plt.subplots(figsize=(18, 11))

    for cat_name, points in CATEGORIES.items():
        _draw_category_series(ax, cat_name, points, label_final=True, label_years=False)

    # Axis formatting
    _format_axes(ax)
    ax.set_xlabel("Cumulative VC Raised by Top Companies ($ Billions)", fontsize=14, labelpad=12)
    ax.set_ylabel("Combined Revenue of Top Companies ($ Millions)", fontsize=14, labelpad=12)

    # Title
    ax.set_title(
        "Fintech + Agentic Intersection: Funding vs Revenue Trajectory (2019-2026)",
        fontsize=20, fontweight="bold", pad=20, color="#1a1a2e",
    )

    # Subtitle
    ax.text(
        0.5, 1.02,
        "Year markers show 2019/2021/2023/2026 snapshots; italic tags mark category start year; "
        "highlighted line tracks early agent-fintech intersection movement",
        transform=ax.transAxes, ha="center", fontsize=10, color="#666",
    )

    # Efficiency reference lines (revenue/funding ratio)
    for ratio, label_text in [
        (1000, "1x efficiency\n($1B rev / $1B funding)"),
        (5000, "5x efficiency"),
    ]:
        xs_ref = np.linspace(0.004, 20, 200)
        ys_ref = xs_ref * ratio
        mask = (ys_ref >= 0.8) & (ys_ref <= 30000)
        ax.plot(xs_ref[mask], ys_ref[mask], ":", color="#ccc", linewidth=1.5,
                alpha=0.6, zorder=0)
        mid = len(xs_ref[mask]) // 2
        if mid > 0:
            ax.text(
                xs_ref[mask][mid], ys_ref[mask][mid], label_text,
                fontsize=7.5, color="#aaa", rotation=32,
                ha="center", va="bottom", style="italic",
            )

    _add_time_legend(ax, loc="lower right")

    # Annotation boxes for key events
    events = [
        (5.5, 22000, "2021: Peak mania\n$131.5B VC, 21% of all VC", "#888"),
        (0.15, 25000, "2022-23: Correction\nFTX collapse, rate hikes\nKlarna -85%", "#c44"),
        (10, 22000, "2025-26: AI + stablecoin era\nRamp $1B rev, Nubank $11.5B\nIPO window reopened", "#28a"),
    ]
    for x, y, text, color in events:
        ax.text(
            x, y, text, fontsize=8, color=color, ha="center", va="top",
            style="italic",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#fafafa",
                      edgecolor="#ddd", alpha=0.92),
            zorder=6,
        )

    # Source note
    fig.text(
        0.5, 0.01,
        "Sources: SEC filings, Crunchbase, PitchBook, company earnings, fintech-market-analysis.md, "
        "fintech-agents-intersection.md  |  "
        "Revenue = estimates for top 3-5 VC-backed companies per category  |  Feb 2026",
        ha="center", fontsize=8, color="#888", style="italic",
    )

    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    return fig


def generate_cohort_subplots():
    cohort_to_categories = {c: [] for c in COHORT_ORDER}
    for category_name in CATEGORIES:
        cohort = CATEGORY_META[category_name]["cohort"]
        cohort_to_categories[cohort].append(category_name)

    nrows, ncols = 2, 3
    fig, axes = plt.subplots(nrows, ncols, figsize=(20, 12), sharex=True, sharey=True)
    flat_axes = axes.flatten()

    for idx, cohort in enumerate(COHORT_ORDER):
        ax = flat_axes[idx]
        members = cohort_to_categories[cohort]

        for cat_name in members:
            _draw_category_series(
                ax,
                cat_name,
                CATEGORIES[cat_name],
                label_final=True,
                label_years=True,
            )

        _format_axes(ax)
        ax.set_title(
            f"{cohort}\n{len(members)} categories",
            fontsize=12, fontweight="bold", color="#1a1a2e",
        )

    # Hide empty panel
    for idx in range(len(COHORT_ORDER), len(flat_axes)):
        flat_axes[idx].axis("off")

    # Global labels and title
    fig.suptitle(
        "Fintech Funding vs Revenue Trajectories by Cohort",
        fontsize=20, fontweight="bold", color="#1a1a2e", y=0.98,
    )
    fig.text(
        0.5, 0.955,
        "Shared log-log axes across subplots; inline year labels (2019/2021/2023/2026) and start-year tags",
        ha="center", fontsize=10, color="#666",
    )
    fig.text(0.5, 0.03, "Cumulative VC Raised by Top Companies ($ Billions)",
             ha="center", fontsize=12)
    fig.text(0.01, 0.5, "Combined Revenue of Top Companies ($ Millions)",
             va="center", rotation="vertical", fontsize=12)

    # Figure-level time marker legend
    handles = [
        Line2D([0], [0], marker=TIME_POINT_MARKERS[i], color="#666", linestyle="",
               markerfacecolor="#888", markeredgecolor="white", markersize=7 + i,
               label=TIME_POINT_SHORT[i])
        for i in range(len(TIME_POINTS))
    ]
    fig.legend(
        handles=handles,
        loc="lower center",
        ncol=4,
        frameon=True,
        framealpha=0.95,
        title="Year Marker",
        title_fontsize=10,
        fontsize=9,
        bbox_to_anchor=(0.5, 0.0),
    )

    fig.text(
        0.5, 0.01,
        "Sources: SEC filings, Crunchbase, PitchBook, company earnings, fintech-market-analysis.md  |  "
        "Revenue = estimates for top 3-5 VC-backed companies per category  |  Feb 2026",
        ha="center", fontsize=8, color="#888", style="italic",
    )

    plt.tight_layout(rect=[0.03, 0.06, 1, 0.93])
    return fig


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    out = root / "charts" / "fintech"
    out.mkdir(parents=True, exist_ok=True)
    print("Generating Fintech Scatter: Funding vs Revenue Trajectory...")
    fig = generate_scatter()
    save_path = out / "fintech_funding_vs_revenue.png"
    fig.savefig(save_path, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"  Saved: {save_path}")
    plt.close(fig)

    print("Generating Fintech Cohort Subplots: Funding vs Revenue Trajectory...")
    fig = generate_cohort_subplots()
    save_path = out / "fintech_funding_vs_revenue_by_cohort.png"
    fig.savefig(save_path, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"  Saved: {save_path}")
    plt.close("all")
