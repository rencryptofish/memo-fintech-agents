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
}

MARKER_SIZES = [30, 60, 100, 180]


def generate_scatter():
    fig, ax = plt.subplots(figsize=(18, 11))

    for cat_name, points in CATEGORIES.items():
        color = COLORS[cat_name]
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]

        # Draw connecting line
        ax.plot(xs, ys, color=color, linewidth=2, alpha=0.45, zorder=1)

        # Arrows between points
        for i in range(len(xs) - 1):
            ax.annotate(
                "", xy=(xs[i + 1], ys[i + 1]), xytext=(xs[i], ys[i]),
                arrowprops=dict(
                    arrowstyle="-|>", color=color, lw=1.8,
                    mutation_scale=12, alpha=0.45,
                ),
                zorder=1,
            )

        # Scatter points (larger = more recent)
        for i, (x, y) in enumerate(points):
            ax.scatter(
                x, y, s=MARKER_SIZES[i], color=color,
                edgecolors="white", linewidth=1, zorder=3,
            )

        # Label at final point
        final_x, final_y = xs[-1], ys[-1]
        label = cat_name.replace("\n", " ")

        # Custom offsets to minimize overlap
        offsets = {
            "B2B Payments\n(Stripe, Adyen, Checkout)":      (12, 8),
            "Neobanks\n(Nubank, Revolut, Chime)":            (-15, 12),
            "Crypto / Blockchain\n(Coinbase, Circle, Chainalysis)": (12, 8),
            "BNPL\n(Klarna, Affirm)":                        (12, -10),
            "CFO Stack\n(Ramp, Brex, Mercury)":              (12, 8),
            "Insurtech\n(Lemonade, Root, Oscar)":            (12, -10),
            "Lending / Credit\n(SoFi, Upstart)":             (-15, -12),
            "Wealthtech\n(Robinhood, eToro)":                (12, -10),
            "Cross-Border\n(Wise, Remitly)":                 (-15, 8),
            "Embedded Finance\n(Marqeta, Lithic, Unit)":     (12, 8),
            "Regtech\n(Chainalysis, ComplyAdv)":             (10, -12),
            "Stablecoin Infra\n(Circle, Bridge, BVNK)":     (-15, -12),
        }
        dx, dy = offsets.get(cat_name, (10, 5))

        ax.annotate(
            label, xy=(final_x, final_y),
            xytext=(dx, dy), textcoords="offset points",
            fontsize=8.5, fontweight="bold", color=color,
            path_effects=[pe.withStroke(linewidth=3, foreground="white")],
            zorder=5,
        )

    # Log scale for readability
    ax.set_xscale("log")
    ax.set_yscale("log")

    # Axis formatting
    ax.set_xlabel("Cumulative VC Raised by Top Companies ($ Billions)", fontsize=14, labelpad=12)
    ax.set_ylabel("Combined Revenue of Top Companies ($ Millions)", fontsize=14, labelpad=12)

    x_ticks = [0.1, 0.2, 0.5, 1, 2, 5, 10, 15]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([f"${v}B" if v >= 1 else f"${int(v*1000)}M" for v in x_ticks],
                       fontsize=10)

    y_ticks = [25, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 20000]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(
        [f"${v}M" if v < 1000 else f"${v/1000:.0f}B" for v in y_ticks],
        fontsize=10,
    )

    ax.set_xlim(0.08, 20)
    ax.set_ylim(20, 30000)

    # Title
    ax.set_title(
        "Fintech: Funding vs Revenue Trajectory by Category (2019-2026)",
        fontsize=20, fontweight="bold", pad=20, color="#1a1a2e",
    )

    # Subtitle
    ax.text(
        0.5, 1.02,
        "Each dot = time snapshot (End 2019 → End 2021 → End 2023 → Early 2026)  •  "
        "Tracks top 3-5 companies per category",
        transform=ax.transAxes, ha="center", fontsize=10, color="#666",
    )

    # Grid
    ax.grid(True, alpha=0.15, which="both", linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Efficiency reference lines (revenue/funding ratio)
    for ratio, label_text in [
        (1000, "1x efficiency\n($1B rev / $1B funding)"),
        (5000, "5x efficiency"),
    ]:
        xs_ref = np.linspace(0.08, 20, 200)
        ys_ref = xs_ref * ratio
        mask = (ys_ref >= 20) & (ys_ref <= 30000)
        ax.plot(xs_ref[mask], ys_ref[mask], ":", color="#ccc", linewidth=1.5,
                alpha=0.6, zorder=0)
        mid = len(xs_ref[mask]) // 2
        if mid > 0:
            ax.text(
                xs_ref[mask][mid], ys_ref[mask][mid], label_text,
                fontsize=7.5, color="#aaa", rotation=32,
                ha="center", va="bottom", style="italic",
            )

    # Time point legend
    for i, (label, size) in enumerate(zip(TIME_POINTS, MARKER_SIZES)):
        ax.scatter([], [], s=size, c="#888", edgecolors="white",
                   linewidth=1, label=label)
    legend1 = ax.legend(
        loc="lower right", fontsize=10, title="Time Snapshot",
        title_fontsize=11, framealpha=0.95, edgecolor="#ddd",
    )
    ax.add_artist(legend1)

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
        "Sources: SEC filings, Crunchbase, PitchBook, company earnings, fintech-market-analysis.md  |  "
        "Revenue = estimates for top 3-5 VC-backed companies per category  |  Feb 2026",
        ha="center", fontsize=8, color="#888", style="italic",
    )

    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
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
    plt.close("all")
