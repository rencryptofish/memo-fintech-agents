"""
Fintech Venture Capital / Investment Funding Data by Category and Year (2015-2025)
==================================================================================

Data compiled from multiple sources:
- KPMG Pulse of Fintech (H2 reports, 2015-2024)
- CB Insights State of Fintech (2021-2024)
- Crunchbase Annual Fintech Reports (2021-2025)
- FT Partners FinTech Almanac (2020-2024)
- Gallagher Re Global InsurTech Reports (2012-2025)
- Statista FinTech Investment Databases
- Dealroom.co Fintech Guide
- BIS Quarterly Review (2021)

METHODOLOGY NOTES:
-----------------
Two parallel datasets are provided:

1. TOTAL FINTECH INVESTMENT (KPMG methodology): includes VC + PE + M&A.
   This is the broadest measure (e.g., 2021 = $210B+).

2. FINTECH VC-ONLY FUNDING (CB Insights / Crunchbase methodology): venture
   capital equity rounds only. This is the narrower measure most commonly
   cited for "startup funding" (e.g., 2021 = ~$92-132B depending on source).

The per-category data below uses the KPMG total-investment figures as the
baseline for categories where KPMG provides sector breakdowns (payments,
crypto, regtech, insurtech, wealthtech). For other categories, data is
sourced from specialist trackers or derived from known percentage shares.

Where exact figures were unavailable for a given category-year, estimates
are derived using:
  (a) Known percentage share of total * total funding, OR
  (b) Interpolation between known data points, OR
  (c) Sector-specific trackers (Gallagher Re for insurtech, etc.)

All figures are in BILLIONS of USD. Estimates are marked with comments.
"""

# =============================================================================
# TOTAL GLOBAL FINTECH INVESTMENT BY YEAR (VC + PE + M&A combined)
# Source: KPMG Pulse of Fintech
# =============================================================================
TOTAL_FINTECH_INVESTMENT_KPMG = {
    # year: (total_billions, deals, source_note)
    2015: (47.0, 1926, "KPMG Pulse of Fintech 2015 Review"),
    2016: (63.4, 1893, "KPMG Pulse of Fintech Q4 2016"),
    2017: (50.8, 2196, "KPMG Pulse of Fintech 2018 (comparison)"),
    2018: (111.8, 2196, "KPMG Pulse of Fintech 2018"),
    2019: (135.7, 2693, "KPMG Pulse of Fintech H2 2019"),
    2020: (125.0, 3674, "KPMG Pulse of Fintech H2 2020"),
    2021: (210.0, 5684, "KPMG Pulse of Fintech H2 2021 / press release"),
    2022: (164.1, 6006, "KPMG Pulse of Fintech H2 2022"),
    2023: (113.7, 4547, "KPMG Pulse of Fintech H2 2023"),
    2024: (95.6, 4639, "KPMG Pulse of Fintech H2 2024"),
    2025: (89.4, None, "KPMG H1 2025 ($44.7B) annualized + Crunchbase FY ($51.8B VC)"),
}

# =============================================================================
# GLOBAL FINTECH VC-ONLY FUNDING BY YEAR
# Sources: Statista / CB Insights / Crunchbase (VC equity rounds only)
# =============================================================================
TOTAL_FINTECH_VC_FUNDING = {
    # year: (vc_billions, source_note)
    2015: (19.4, "Statista / WEF / Dealroom"),
    2016: (24.0, "Statista; est. from growth trajectory 2015->2017"),
    2017: (27.4, "FinTech Futures: 'Global VC investment in fintech reaches record $27.4bn'"),
    2018: (40.1, "Statista / CB Insights"),
    2019: (37.9, "Statista / KPMG (VC component of $135.7B total)"),
    2020: (45.7, "Statista; KPMG VC component confirmed at $46B"),
    2021: (121.5, "Statista ($121.5B); KPMG VC=$115B; Crunchbase=$132-137B"),
    2022: (88.8, "Statista ($88.8B); KPMG VC=$80.5B; Crunchbase=$81B"),
    2023: (46.3, "Statista ($46.3B); KPMG VC=$49.2B; Crunchbase=$43B"),
    2024: (43.4, "KPMG VC=$43.4B; Crunchbase=$40.8B"),
    2025: (51.8, "Crunchbase FY 2025 ($51.8B, +27% YoY)"),
}


# =============================================================================
# FUNDING BY FINTECH CATEGORY BY YEAR (in billions USD)
# =============================================================================
# Uses KPMG total investment where available; supplemented by other sources.
# "est" in comments = estimated via % share or interpolation.

YEARS = list(range(2015, 2026))

# ---- 1. PAYMENTS ----
# Sources: KPMG Pulse of Fintech sector breakdowns (2019-2024 confirmed)
# 2015-2018 estimated from known share (~25-35% of total fintech)
PAYMENTS = {
    2015: 10.5,   # est: ~22% of $47B; early mobile payments era
    2016: 14.5,   # est: ~23% of $63.4B; Worldpay/Vantiv activity
    2017: 13.0,   # est: ~25% of $50.8B
    2018: 33.5,   # est: ~30% of $111.8B; Worldpay acquisition drove total up
    2019: 107.8,  # KPMG confirmed: payments investment $107.8B (includes Fiserv/First Data $22B M&A, FIS/Worldpay $35B M&A)
    2020: 29.1,   # KPMG confirmed
    2021: 57.1,   # KPMG confirmed (CB Insights: $51.7B)
    2022: 53.1,   # KPMG confirmed
    2023: 20.7,   # KPMG confirmed (alternate: $17.2B VC-only)
    2024: 31.0,   # KPMG confirmed ($30.8B rounded)
    2025: 18.0,   # est: KPMG H1 2025 payments=$4.6B; Crunchbase: payments led 2025 funding
}

# ---- 2. LENDING / CREDIT ----
# Sources: CB Insights, Crunchbase, derived from total minus other known sectors
# Lending was the dominant category 2015-2017 (LendingClub, SoFi, Prosper era)
LENDING_CREDIT = {
    2015: 10.2,   # est: ~22% of $47B; peak of marketplace lending era
    2016: 8.5,    # est: declining post-LendingClub scandal; ~13% of total
    2017: 7.5,    # est: ~15% of $50.8B; market correction in online lending
    2018: 10.0,   # est: ~9% of $111.8B; recovery
    2019: 5.5,    # est: ~4% of $135.7B (excl mega M&A); VC portion
    2020: 8.0,    # est: COVID drove digital lending demand; ~6% of total
    2021: 18.5,   # est: ~9% of $210B; strong VC into lending fintechs
    2022: 12.0,   # est: ~7% of $164.1B; rate hikes hit lending models
    2023: 7.5,    # Crunchbase: digital lending ~$4.9B VC; total ~$7.5B
    2024: 6.0,    # est: continued pullback; higher rates
    2025: 7.0,    # est: Crunchbase notes lending recovery in 2025
}

# ---- 3. CRYPTO / BLOCKCHAIN ----
# Sources: KPMG (2018-2024 confirmed), Statista, The Block
CRYPTO_BLOCKCHAIN = {
    2015: 0.5,    # est: pre-ICO era; minimal VC
    2016: 0.6,    # est: early blockchain VC; Bitcoin ~$400-1000
    2017: 3.0,    # est: ICO boom began; blockchain VC growing rapidly
    2018: 4.5,    # KPMG confirmed: "stayed steady at $4.5B" (also: $6.3B-$7B by other measures)
    2019: 4.7,    # KPMG confirmed ($4.7B; down from 2018 by some measures at $2.4B non-enterprise)
    2020: 5.5,    # KPMG confirmed (CB Insights: $5.5B baseline for 2021 comparison)
    2021: 30.2,   # KPMG confirmed ($30.2B; +449% YoY)
    2022: 23.1,   # KPMG confirmed ($23.1B; also reported as $33.3B including all crypto deals)
    2023: 8.0,    # KPMG confirmed (<$8B; post-FTX collapse)
    2024: 13.7,   # The Block / KPMG ($9.1B KPMG; $13.7B The Block incl. all crypto VC)
    2025: 18.0,   # PitchBook projection; Crunchbase: crypto mega-rounds (Polymarket $2B, Binance $2B)
}

# ---- 4. INSURTECH ----
# Sources: KPMG (2021-2024), Gallagher Re, CB Insights, MAPFRE
INSURTECH = {
    2015: 2.6,    # Gallagher Re cumulative data: ~$2.6B (sector still nascent)
    2016: 1.7,    # Gallagher Re: dip after 2015; ~$10B cumulative by 2017
    2017: 3.0,    # Gallagher Re: $10B cumulative reached; implies ~$3B in 2017
    2018: 4.2,    # MAPFRE / Gallagher Re confirmed: ~$4.2B
    2019: 6.4,    # Gallagher Re: $20B cumulative by 2019; implies ~$6.4B
    2020: 7.5,    # est: growth continued pre-pandemic then surge; ~$20B->~$27.5B cumulative
    2021: 14.4,   # KPMG confirmed ($14.4B; record year; cumulative ~$40B by year-end per Gallagher)
    2022: 8.6,    # Gallagher Re / MAPFRE confirmed: $8.6B (second-largest year)
    2023: 4.5,    # Gallagher Re confirmed: $4.5B (-43.7% YoY)
    2024: 4.2,    # KPMG: $2.9B; MAPFRE: $4.2B (incl. later-stage); Gallagher Re: ~$4.2B
    2025: 5.0,    # est: Gallagher Re Q1 2025=$1.31B (+90% YoY); Q2=$1.09B; annualized ~$5B
}

# ---- 5. WEALTHTECH / CAPITAL MARKETS ----
# Sources: KPMG (2021, 2023-2024), FT Partners
WEALTHTECH_CAPITAL_MARKETS = {
    2015: 2.0,    # est: robo-advisor era (Betterment, Wealthfront); ~4% of total
    2016: 2.5,    # est: continued robo-advisor growth
    2017: 2.0,    # est: ~4% of $50.8B
    2018: 4.0,    # est: ~3.5% of $111.8B
    2019: 3.5,    # est: ~2.5% of total; sector matured
    2020: 3.0,    # est: COVID trading boom benefited wealthtech
    2021: 6.0,    # KPMG: wealthtech=$1.62B (narrow def); broader capital markets ~$6B est
    2022: 4.5,    # est: pulled back with markets; ~2.7% of $164.1B
    2023: 2.5,    # KPMG: wealthtech=$190M (narrow); broader incl. capital markets tech ~$2.5B
    2024: 2.8,    # KPMG: wealthtech=$400M; WealthTech deal volume +32.7% in 2024; broader ~$2.8B
    2025: 3.5,    # est: recovery; Crunchbase: wealth tech and capital markets tech rising
}

# ---- 6. NEOBANKS / DIGITAL BANKING ----
# Sources: Statista, Crunchbase, CB Insights
NEOBANKS_DIGITAL_BANKING = {
    2015: 1.5,    # est: early neobank era (N26, Monzo founding)
    2016: 2.0,    # est: neobank VC ramping up
    2017: 3.5,    # est: Revolut, Monzo, Chime gaining traction; part of $32B total 2017-2021
    2018: 5.0,    # est: major rounds (Revolut, N26); ~4.5% of $111.8B
    2019: 7.0,    # Statista: Q3 2019 peak quarter at $1.74B; annual ~$7B
    2020: 5.5,    # est: COVID initially slowed then accelerated digital banking
    2021: 14.0,   # est: $32B raised 2017-2021 (Statista); 2021 was peak => ~$14B
    2022: 8.0,    # est: CB Insights: banking funding declined 63% YoY; ~$8B
    2023: 5.0,    # est: Crunchbase: continued decline; some sources cite $15B (likely broader def)
    2024: 3.5,    # est: further pullback; focus shifted to profitability
    2025: 4.5,    # est: mild recovery with AI-powered neobanks
}

# ---- 7. BNPL (BUY NOW, PAY LATER) ----
# Sources: Payments Dive, CB Insights, Crunchbase
# Note: BNPL is a sub-category that overlaps with both Payments and Lending
BNPL = {
    2015: 0.1,    # est: BNPL barely existed as a VC category
    2016: 0.2,    # est: Afterpay, Klarna early stages
    2017: 0.4,    # est: growing awareness
    2018: 0.8,    # est: Klarna rounds, Afterpay growth
    2019: 1.1,    # Payments Dive: $1.1B in 2019
    2020: 1.5,    # Payments Dive confirmed: record $1.5B (+42% YoY over 2019)
    2021: 5.0,    # est: peak BNPL hype; Klarna valued at $45.6B; massive rounds
    2022: 2.5,    # est: Klarna valuation cut 85%; sector pullback
    2023: 1.0,    # est: significant decline; regulatory scrutiny
    2024: 0.8,    # est: further consolidation; Affirm, Klarna focused on IPO path
    2025: 1.2,    # est: Klarna IPO; renewed interest but cautious
}

# ---- 8. REGTECH / COMPLIANCE ----
# Sources: KPMG (2017-2024 confirmed for most years)
REGTECH_COMPLIANCE = {
    2015: 0.6,    # est: regtech as a concept was just emerging
    2016: 0.8,    # est: post-2008 regulation (Basel III, AML) driving demand
    2017: 1.2,    # KPMG confirmed: $1.2B
    2018: 3.7,    # KPMG confirmed: tripled from 2017 to $3.7B
    2019: 5.0,    # est: continued growth; KYC/AML investment surge
    2020: 7.0,    # est: COVID drove compliance digitization
    2021: 11.8,   # KPMG confirmed: $11.8B (CB Insights: $9.9B by narrower def)
    2022: 18.6,   # KPMG confirmed: $18.6B (record; driven by major deals)
    2023: 4.4,    # KPMG confirmed: $4.4B (alt report: $2.6B by narrower def)
    2024: 7.4,    # KPMG confirmed: $7.4B (alt: $8.3B)
    2025: 5.0,    # est: KPMG H1 2025=$2.1B; annualized ~$4-5B
}

# ---- 9. EMBEDDED FINANCE / BaaS ----
# Sources: Statista, Tracxn, Bain & Company
EMBEDDED_FINANCE_BAAS = {
    2015: 0.3,    # est: concept barely existed; early API banking
    2016: 0.5,    # est: Plaid early growth; API-first banking emerging
    2017: 0.8,    # est: growing recognition of embedded finance
    2018: 1.5,    # est: Plaid, Marqeta, other infra companies growing
    2019: 2.0,    # est: sector gaining identity; BaaS providers launching
    2020: 3.5,    # Statista: ~$1.5B VC narrowly; broader incl. PE/strategic ~$3.5B
    2021: 11.2,   # Tracxn confirmed: most funding ever at $11.2B
    2022: 6.5,    # est: pullback but embedded finance stayed resilient
    2023: 3.5,    # est: continued decline; some BaaS providers (Synapse) failed
    2024: 3.0,    # est: regulatory scrutiny on BaaS; partner bank issues
    2025: 4.0,    # est: recovery; embedded payments and lending growing
}

# ---- 10. B2B FINTECH INFRASTRUCTURE ----
# Sources: Crunchbase, Plaid/Stripe data, FT Partners
# Includes: core banking infra, API platforms, developer tools, data/analytics
# Note: This category overlaps with embedded finance but focuses on pure infra plays
B2B_FINTECH_INFRA = {
    2015: 2.0,    # est: Stripe ($5B val), Plaid early, core banking modernization beginning
    2016: 2.5,    # est: growing VC interest in B2B fintech
    2017: 3.0,    # est: ~6% of $50.8B
    2018: 5.0,    # est: Stripe mega-round; ~4.5% of $111.8B
    2019: 5.5,    # est: Plaid, MX, Thought Machine gaining traction
    2020: 7.0,    # est: COVID accelerated B2B digitization; ~5.6% of $125B
    2021: 18.0,   # est: Stripe $600M at $95B; FT Partners: FMS=24% share; ~8.5% of $210B
    2022: 12.0,   # est: still strong but declining; B2B players=60% of largest payments investments
    2023: 10.0,   # est: Stripe $6.5B round (secondary); infrastructure remained resilient
    2024: 8.0,    # est: continued infrastructure investment; Plaid $575M
    2025: 10.0,   # est: Crunchbase: "real sense of momentum in B2B infrastructure"; AI-native fintech
}


# =============================================================================
# CONSOLIDATED DATA DICTIONARY (for easy charting)
# =============================================================================
FUNDING_BY_CATEGORY = {
    "Payments": PAYMENTS,
    "Lending / Credit": LENDING_CREDIT,
    "Crypto / Blockchain": CRYPTO_BLOCKCHAIN,
    "Insurtech": INSURTECH,
    "Wealthtech / Capital Markets": WEALTHTECH_CAPITAL_MARKETS,
    "Neobanks / Digital Banking": NEOBANKS_DIGITAL_BANKING,
    "BNPL": BNPL,
    "Regtech / Compliance": REGTECH_COMPLIANCE,
    "Embedded Finance / BaaS": EMBEDDED_FINANCE_BAAS,
    "B2B Fintech Infrastructure": B2B_FINTECH_INFRA,
}


# =============================================================================
# HELPER: Build a pandas DataFrame
# =============================================================================
def get_funding_dataframe():
    """Return a pandas DataFrame with years as rows and categories as columns."""
    import pandas as pd

    data = {}
    for category, yearly_data in FUNDING_BY_CATEGORY.items():
        data[category] = {year: yearly_data.get(year, 0) for year in YEARS}

    df = pd.DataFrame(data, index=YEARS)
    df.index.name = "Year"

    # Add totals
    df["Category Sum"] = df.sum(axis=1)

    # Add KPMG total for reference
    df["KPMG Total (VC+PE+M&A)"] = [
        TOTAL_FINTECH_INVESTMENT_KPMG[y][0] for y in YEARS
    ]

    # Add VC-only total for reference
    df["VC-Only Total"] = [
        TOTAL_FINTECH_VC_FUNDING[y][0] for y in YEARS
    ]

    return df


# =============================================================================
# SAMPLE CHART CODE (stacked area chart)
# =============================================================================
def plot_stacked_area_chart(save_path=None):
    """Generate a stacked area chart of fintech funding by category."""
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    import pandas as pd

    df = get_funding_dataframe()

    # Select only the category columns (not totals)
    categories = list(FUNDING_BY_CATEGORY.keys())
    plot_df = df[categories]

    # Color palette
    colors = [
        "#2563EB",  # Payments - blue
        "#7C3AED",  # Lending - purple
        "#F59E0B",  # Crypto - amber
        "#10B981",  # Insurtech - green
        "#EC4899",  # Wealthtech - pink
        "#3B82F6",  # Neobanks - lighter blue
        "#EF4444",  # BNPL - red
        "#6366F1",  # Regtech - indigo
        "#14B8A6",  # Embedded Finance - teal
        "#8B5CF6",  # B2B Infra - violet
    ]

    fig, ax = plt.subplots(figsize=(16, 9))

    ax.stackplot(
        YEARS,
        [plot_df[cat].values for cat in categories],
        labels=categories,
        colors=colors,
        alpha=0.85,
    )

    # Add KPMG total line for reference
    kpmg_totals = [TOTAL_FINTECH_INVESTMENT_KPMG[y][0] for y in YEARS]
    ax.plot(
        YEARS, kpmg_totals, "k--", linewidth=2, label="KPMG Total (VC+PE+M&A)", alpha=0.7
    )

    ax.set_title(
        "Global Fintech Investment by Category (2015-2025)",
        fontsize=18,
        fontweight="bold",
        pad=20,
    )
    ax.set_xlabel("Year", fontsize=13)
    ax.set_ylabel("Investment ($ Billions)", fontsize=13)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%.0fB"))
    ax.set_xticks(YEARS)
    ax.legend(loc="upper left", fontsize=9, ncol=2)
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Chart saved to {save_path}")
    else:
        plt.show()

    return fig, ax


def plot_category_heatmap(save_path=None):
    """Generate a heatmap showing funding intensity by category and year."""
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    df = get_funding_dataframe()
    categories = list(FUNDING_BY_CATEGORY.keys())
    plot_df = df[categories]

    fig, ax = plt.subplots(figsize=(16, 8))

    im = ax.imshow(plot_df.T.values, cmap="YlOrRd", aspect="auto")

    ax.set_xticks(range(len(YEARS)))
    ax.set_xticklabels(YEARS)
    ax.set_yticks(range(len(categories)))
    ax.set_yticklabels(categories)

    # Add value labels
    for i in range(len(categories)):
        for j in range(len(YEARS)):
            val = plot_df.iloc[j, i]
            text_color = "white" if val > 15 else "black"
            ax.text(j, i, f"${val:.1f}B", ha="center", va="center",
                    fontsize=7, color=text_color, fontweight="bold")

    plt.colorbar(im, ax=ax, label="Investment ($ Billions)")
    ax.set_title(
        "Fintech Investment Heatmap by Category and Year (2015-2025)",
        fontsize=16,
        fontweight="bold",
        pad=15,
    )

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Heatmap saved to {save_path}")
    else:
        plt.show()

    return fig, ax


def plot_grouped_bar_chart(save_path=None):
    """Generate a grouped bar chart comparing category funding across key years."""
    import matplotlib.pyplot as plt
    import numpy as np

    key_years = [2015, 2018, 2020, 2021, 2022, 2023, 2024, 2025]
    categories = list(FUNDING_BY_CATEGORY.keys())

    x = np.arange(len(categories))
    width = 0.1
    n_years = len(key_years)

    fig, ax = plt.subplots(figsize=(18, 9))

    for i, year in enumerate(key_years):
        values = [FUNDING_BY_CATEGORY[cat][year] for cat in categories]
        offset = (i - n_years / 2 + 0.5) * width
        ax.bar(x + offset, values, width, label=str(year), alpha=0.85)

    ax.set_xlabel("Fintech Category", fontsize=13)
    ax.set_ylabel("Investment ($ Billions)", fontsize=13)
    ax.set_title(
        "Fintech Investment by Category Across Key Years",
        fontsize=16,
        fontweight="bold",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=35, ha="right", fontsize=9)
    ax.legend(title="Year")
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Chart saved to {save_path}")
    else:
        plt.show()

    return fig, ax


# =============================================================================
# DATA CONFIDENCE RATINGS
# =============================================================================
# H = High confidence (directly from named report with exact figure)
# M = Medium confidence (derived from % share or cross-referenced sources)
# L = Low confidence (interpolated or estimated)

CONFIDENCE = {
    "Payments": {
        2015: "L", 2016: "L", 2017: "L", 2018: "M",
        2019: "H", 2020: "H", 2021: "H", 2022: "H",
        2023: "H", 2024: "H", 2025: "M",
    },
    "Lending / Credit": {
        2015: "M", 2016: "M", 2017: "L", 2018: "L",
        2019: "L", 2020: "L", 2021: "M", 2022: "M",
        2023: "M", 2024: "M", 2025: "L",
    },
    "Crypto / Blockchain": {
        2015: "L", 2016: "L", 2017: "M", 2018: "H",
        2019: "H", 2020: "H", 2021: "H", 2022: "H",
        2023: "H", 2024: "H", 2025: "M",
    },
    "Insurtech": {
        2015: "M", 2016: "M", 2017: "M", 2018: "H",
        2019: "M", 2020: "M", 2021: "H", 2022: "H",
        2023: "H", 2024: "H", 2025: "M",
    },
    "Wealthtech / Capital Markets": {
        2015: "L", 2016: "L", 2017: "L", 2018: "L",
        2019: "L", 2020: "L", 2021: "M", 2022: "L",
        2023: "M", 2024: "M", 2025: "L",
    },
    "Neobanks / Digital Banking": {
        2015: "L", 2016: "L", 2017: "L", 2018: "M",
        2019: "M", 2020: "M", 2021: "M", 2022: "M",
        2023: "M", 2024: "L", 2025: "L",
    },
    "BNPL": {
        2015: "L", 2016: "L", 2017: "L", 2018: "L",
        2019: "H", 2020: "H", 2021: "M", 2022: "M",
        2023: "M", 2024: "L", 2025: "L",
    },
    "Regtech / Compliance": {
        2015: "L", 2016: "L", 2017: "H", 2018: "H",
        2019: "M", 2020: "M", 2021: "H", 2022: "H",
        2023: "H", 2024: "H", 2025: "M",
    },
    "Embedded Finance / BaaS": {
        2015: "L", 2016: "L", 2017: "L", 2018: "L",
        2019: "L", 2020: "M", 2021: "H", 2022: "M",
        2023: "M", 2024: "M", 2025: "L",
    },
    "B2B Fintech Infrastructure": {
        2015: "L", 2016: "L", 2017: "L", 2018: "M",
        2019: "M", 2020: "M", 2021: "M", 2022: "M",
        2023: "M", 2024: "M", 2025: "M",
    },
}


# =============================================================================
# PRINT SUMMARY TABLE
# =============================================================================
if __name__ == "__main__":
    print("=" * 130)
    print("GLOBAL FINTECH INVESTMENT BY CATEGORY ($ BILLIONS)")
    print("=" * 130)

    # Header
    header = f"{'Category':<30}"
    for y in YEARS:
        header += f"{y:>8}"
    header += f"{'Total':>10}"
    print(header)
    print("-" * 130)

    grand_total_by_year = {y: 0 for y in YEARS}

    for cat_name, cat_data in FUNDING_BY_CATEGORY.items():
        row = f"{cat_name:<30}"
        row_total = 0
        for y in YEARS:
            val = cat_data.get(y, 0)
            row += f"{val:>8.1f}"
            row_total += val
            grand_total_by_year[y] += val
        row += f"{row_total:>10.1f}"
        print(row)

    print("-" * 130)

    # Category sum row
    row = f"{'CATEGORY SUM':<30}"
    for y in YEARS:
        row += f"{grand_total_by_year[y]:>8.1f}"
    row += f"{sum(grand_total_by_year.values()):>10.1f}"
    print(row)

    # KPMG total row
    row = f"{'KPMG Total (VC+PE+M&A)':<30}"
    for y in YEARS:
        row += f"{TOTAL_FINTECH_INVESTMENT_KPMG[y][0]:>8.1f}"
    print(row)

    # VC-only row
    row = f"{'VC-Only Total':<30}"
    for y in YEARS:
        row += f"{TOTAL_FINTECH_VC_FUNDING[y][0]:>8.1f}"
    print(row)

    print("=" * 130)
    print()
    print("Note: Categories overlap (e.g., BNPL straddles Payments & Lending;")
    print("Embedded Finance overlaps with B2B Infrastructure). Category sum will")
    print("exceed actual totals. The KPMG Total line is the authoritative reference.")
