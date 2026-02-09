"""
Generate an estimated fintech cohort outcome split:
- CSV: cohort-level funding split (did well vs not well)
- CSV: anchor drivers used to ground the estimate
- Chart: stacked bars by cohort

Method:
1) Start from cohort-level VC pool estimates (from memo tables and prior synthesis).
2) Apply an estimated "did well" share per cohort.
3) Keep explicit company/category anchors in a separate CSV to show where the
   directional assumptions come from.
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


COHORT_SPLIT_ROWS = [
    {
        "cohort_order": 1,
        "cohort": "1. Pre-2008",
        "era": "1982-2007",
        "funding_pool_b": 5.0,
        "did_well_share": 0.35,
    },
    {
        "cohort_order": 2,
        "cohort": "2. Post-Crisis",
        "era": "2008-2012",
        "funding_pool_b": 20.0,
        "did_well_share": 0.75,
    },
    {
        "cohort_order": 3,
        "cohort": "3. Boom",
        "era": "2013-2015",
        "funding_pool_b": 48.4,
        "did_well_share": 0.65,
    },
    {
        "cohort_order": 4,
        "cohort": "4. Maturation",
        "era": "2016-2018",
        "funding_pool_b": 91.5,
        "did_well_share": 0.30,
    },
    {
        "cohort_order": 5,
        "cohort": "5. COVID",
        "era": "2019-2020",
        "funding_pool_b": 83.6,
        "did_well_share": 0.55,
    },
    {
        "cohort_order": 6,
        "cohort": "6. Peak Mania",
        "era": "2021",
        "funding_pool_b": 131.5,
        "did_well_share": 0.35,
    },
    {
        "cohort_order": 7,
        "cohort": "7. Correction",
        "era": "2022-2023",
        "funding_pool_b": 135.1,
        "did_well_share": 0.45,
    },
    {
        "cohort_order": 8,
        "cohort": "8. New Era",
        "era": "2024-2026 est",
        "funding_pool_b": 148.6,
        "did_well_share": 0.65,
    },
]


DRIVER_ANCHOR_ROWS = [
    # Pre-2008
    {"cohort": "1. Pre-2008", "outcome": "did_well", "driver": "PayPal", "driver_type": "company", "amount_b": 1.5},
    {"cohort": "1. Pre-2008", "outcome": "did_well", "driver": "Adyen", "driver_type": "company", "amount_b": 0.2},
    {"cohort": "1. Pre-2008", "outcome": "not_well", "driver": "Klarna (overfunding/repricing cycle)", "driver_type": "company", "amount_b": 3.5},
    {"cohort": "1. Pre-2008", "outcome": "not_well", "driver": "LendingClub (model stress/pivot)", "driver_type": "company", "amount_b": 0.4},
    # Post-Crisis
    {"cohort": "2. Post-Crisis", "outcome": "did_well", "driver": "Stripe", "driver_type": "company", "amount_b": 8.7},
    {"cohort": "2. Post-Crisis", "outcome": "did_well", "driver": "SoFi", "driver_type": "company", "amount_b": 2.5},
    {"cohort": "2. Post-Crisis", "outcome": "did_well", "driver": "Chime", "driver_type": "company", "amount_b": 2.3},
    {"cohort": "2. Post-Crisis", "outcome": "did_well", "driver": "Plaid", "driver_type": "company", "amount_b": 0.75},
    {"cohort": "2. Post-Crisis", "outcome": "did_well", "driver": "Coinbase", "driver_type": "company", "amount_b": 0.55},
    {"cohort": "2. Post-Crisis", "outcome": "did_well", "driver": "Wise", "driver_type": "company", "amount_b": 0.4},
    {"cohort": "2. Post-Crisis", "outcome": "did_well", "driver": "Square", "driver_type": "company", "amount_b": 0.2},
    {"cohort": "2. Post-Crisis", "outcome": "not_well", "driver": "Oscar", "driver_type": "company", "amount_b": 1.3},
    {"cohort": "2. Post-Crisis", "outcome": "not_well", "driver": "Affirm", "driver_type": "company", "amount_b": 0.8},
    # Boom
    {"cohort": "3. Boom", "outcome": "did_well", "driver": "Nubank", "driver_type": "company", "amount_b": 2.3},
    {"cohort": "3. Boom", "outcome": "did_well", "driver": "Revolut", "driver_type": "company", "amount_b": 1.7},
    {"cohort": "3. Boom", "outcome": "did_well", "driver": "Robinhood", "driver_type": "company", "amount_b": 0.86},
    {"cohort": "3. Boom", "outcome": "did_well", "driver": "Monzo", "driver_type": "company", "amount_b": 0.4},
    {"cohort": "3. Boom", "outcome": "not_well", "driver": "Root", "driver_type": "company", "amount_b": 0.525},
    {"cohort": "3. Boom", "outcome": "not_well", "driver": "Lemonade", "driver_type": "company", "amount_b": 0.48},
    # Maturation
    {"cohort": "4. Maturation", "outcome": "did_well", "driver": "Brex", "driver_type": "company", "amount_b": 1.2},
    {"cohort": "4. Maturation", "outcome": "did_well", "driver": "Mercury", "driver_type": "company", "amount_b": 0.3},
    {"cohort": "4. Maturation", "outcome": "not_well", "driver": "ICO funding wave (2018)", "driver_type": "category", "amount_b": 7.8},
    {"cohort": "4. Maturation", "outcome": "not_well", "driver": "ICO funding wave (2017)", "driver_type": "category", "amount_b": 6.2},
    # COVID
    {"cohort": "5. COVID", "outcome": "did_well", "driver": "Ramp", "driver_type": "company", "amount_b": 1.6},
    {"cohort": "5. COVID", "outcome": "did_well", "driver": "Stripe (2020 round)", "driver_type": "company", "amount_b": 0.6},
    {"cohort": "5. COVID", "outcome": "did_well", "driver": "Robinhood (2020 round)", "driver_type": "company", "amount_b": 0.28},
    {"cohort": "5. COVID", "outcome": "not_well", "driver": "FTX", "driver_type": "company", "amount_b": 1.0},
    # Peak mania
    {"cohort": "6. Peak Mania", "outcome": "did_well", "driver": "Nubank (2021 round)", "driver_type": "company", "amount_b": 1.1},
    {"cohort": "6. Peak Mania", "outcome": "did_well", "driver": "Chime (2021 round)", "driver_type": "company", "amount_b": 1.1},
    {"cohort": "6. Peak Mania", "outcome": "not_well", "driver": "Klarna (2021 round)", "driver_type": "company", "amount_b": 1.2},
    {"cohort": "6. Peak Mania", "outcome": "not_well", "driver": "FTX (2021 round)", "driver_type": "company", "amount_b": 1.0},
    # New era
    {"cohort": "8. New Era", "outcome": "did_well", "driver": "AI-native fintech", "driver_type": "category", "amount_b": 2.0},
    {"cohort": "8. New Era", "outcome": "did_well", "driver": "CFO stack funding (Q4 2025)", "driver_type": "category", "amount_b": 1.8},
    {"cohort": "8. New Era", "outcome": "did_well", "driver": "Stablecoin infra VC", "driver_type": "category", "amount_b": 1.5},
]


COHORT_TYPE_CLASSIFICATION_ROWS = [
    {
        "cohort_order": 1,
        "cohort": "1. Pre-2008",
        "era": "1982-2007",
        "company_type": "Internet-native transaction rails",
        "type_group": "Payments / Brokerage / Early Lending",
        "examples": "PayPal, E*Trade, Adyen, LendingClub, Klarna",
        "profile": "Early digitization of core financial transactions on web and e-commerce rails.",
    },
    {
        "cohort_order": 2,
        "cohort": "2. Post-Crisis",
        "era": "2008-2012",
        "company_type": "API-first fintech infrastructure",
        "type_group": "Payments infra / Data APIs / Neobanks / Crypto exchanges",
        "examples": "Stripe, Plaid, Square, Wise, Coinbase, Chime, SoFi",
        "profile": "Smartphone + post-crisis trust reset favored developer tools and modern financial interfaces.",
    },
    {
        "cohort_order": 3,
        "cohort": "3. Boom",
        "era": "2013-2015",
        "company_type": "Consumer growth fintech",
        "type_group": "Neobanks / BNPL / Insurtech / Commission-free investing",
        "examples": "Nubank, Revolut, Robinhood, Monzo, N26, Afterpay, Lemonade, Root",
        "profile": "Mobile adoption and abundant capital favored rapid user-growth consumer models.",
    },
    {
        "cohort_order": 4,
        "cohort": "4. Maturation",
        "era": "2016-2018",
        "company_type": "Open-banking and startup-finance infrastructure",
        "type_group": "Corporate cards / Startup banking / Open banking APIs / BaaS",
        "examples": "Brex, Mercury, TrueLayer (+ broader ICO and embedded finance buildout)",
        "profile": "Regulatory openings (PSD2/Open Banking) and API maturity shifted focus back to rails and infra.",
    },
    {
        "cohort_order": 5,
        "cohort": "5. COVID",
        "era": "2019-2020",
        "company_type": "Digital-first scale-up cohort",
        "type_group": "Neobanks / Digital payments / Vertical SaaS + fintech / BNPL acceleration",
        "examples": "Chime, Stripe, Robinhood, Cash App ecosystem, Klarna/Afterpay acceleration",
        "profile": "Pandemic behavior shifts accelerated usage and funding for already-launched digital platforms.",
    },
    {
        "cohort_order": 6,
        "cohort": "6. Peak Mania",
        "era": "2021",
        "company_type": "Mega-round, valuation-expansion cohort",
        "type_group": "Cross-category megadeals (Payments / Crypto / BNPL / Neobanks / SPACs)",
        "examples": "Nubank, Chime, Klarna, FTX, Generate",
        "profile": "Low rates and risk-on capital favored large financings across both durable and speculative models.",
    },
    {
        "cohort_order": 7,
        "cohort": "7. Correction",
        "era": "2022-2023",
        "company_type": "Profitability and resilience cohort",
        "type_group": "Cost-disciplined survivors / Consolidators / Compliance-first operators",
        "examples": "Monzo, Revolut, SoFi, Robinhood survivors; Synapse/FTX-style failures on weak models",
        "profile": "Rate shock and fraud unwind re-priced growth models and selected for unit economics quality.",
    },
    {
        "cohort_order": 8,
        "cohort": "8. New Era",
        "era": "2024-2026 est",
        "company_type": "AI-native and programmable-money infrastructure",
        "type_group": "AI-native fintech / Stablecoin infra / CFO stack / Embedded finance 2.0",
        "examples": "Ramp, Circle, stablecoin infra stack, AI-first accounting/treasury/payroll startups",
        "profile": "AI platform shift plus stablecoin regulatory clarity is driving a new infrastructure-heavy wave.",
    },
]


TYPE_GROUP_MIX_SHARES = [
    # Shares are estimated composition of each cohort's funding pool by company type group.
    {"cohort_order": 1, "type_group": "Payments & Infrastructure", "share": 0.45},
    {"cohort_order": 1, "type_group": "Consumer Banking & Wealth", "share": 0.20},
    {"cohort_order": 1, "type_group": "Lending & BNPL", "share": 0.35},
    {"cohort_order": 1, "type_group": "Insurtech", "share": 0.00},
    {"cohort_order": 1, "type_group": "Crypto & Web3", "share": 0.00},
    {"cohort_order": 1, "type_group": "AI-Native / Stablecoin / CFO", "share": 0.00},
    {"cohort_order": 2, "type_group": "Payments & Infrastructure", "share": 0.45},
    {"cohort_order": 2, "type_group": "Consumer Banking & Wealth", "share": 0.25},
    {"cohort_order": 2, "type_group": "Lending & BNPL", "share": 0.15},
    {"cohort_order": 2, "type_group": "Insurtech", "share": 0.00},
    {"cohort_order": 2, "type_group": "Crypto & Web3", "share": 0.15},
    {"cohort_order": 2, "type_group": "AI-Native / Stablecoin / CFO", "share": 0.00},
    {"cohort_order": 3, "type_group": "Payments & Infrastructure", "share": 0.10},
    {"cohort_order": 3, "type_group": "Consumer Banking & Wealth", "share": 0.45},
    {"cohort_order": 3, "type_group": "Lending & BNPL", "share": 0.25},
    {"cohort_order": 3, "type_group": "Insurtech", "share": 0.20},
    {"cohort_order": 3, "type_group": "Crypto & Web3", "share": 0.00},
    {"cohort_order": 3, "type_group": "AI-Native / Stablecoin / CFO", "share": 0.00},
    {"cohort_order": 4, "type_group": "Payments & Infrastructure", "share": 0.25},
    {"cohort_order": 4, "type_group": "Consumer Banking & Wealth", "share": 0.10},
    {"cohort_order": 4, "type_group": "Lending & BNPL", "share": 0.05},
    {"cohort_order": 4, "type_group": "Insurtech", "share": 0.00},
    {"cohort_order": 4, "type_group": "Crypto & Web3", "share": 0.60},
    {"cohort_order": 4, "type_group": "AI-Native / Stablecoin / CFO", "share": 0.00},
    {"cohort_order": 5, "type_group": "Payments & Infrastructure", "share": 0.35},
    {"cohort_order": 5, "type_group": "Consumer Banking & Wealth", "share": 0.35},
    {"cohort_order": 5, "type_group": "Lending & BNPL", "share": 0.25},
    {"cohort_order": 5, "type_group": "Insurtech", "share": 0.03},
    {"cohort_order": 5, "type_group": "Crypto & Web3", "share": 0.02},
    {"cohort_order": 5, "type_group": "AI-Native / Stablecoin / CFO", "share": 0.00},
    {"cohort_order": 6, "type_group": "Payments & Infrastructure", "share": 0.20},
    {"cohort_order": 6, "type_group": "Consumer Banking & Wealth", "share": 0.25},
    {"cohort_order": 6, "type_group": "Lending & BNPL", "share": 0.20},
    {"cohort_order": 6, "type_group": "Insurtech", "share": 0.10},
    {"cohort_order": 6, "type_group": "Crypto & Web3", "share": 0.25},
    {"cohort_order": 6, "type_group": "AI-Native / Stablecoin / CFO", "share": 0.00},
    {"cohort_order": 7, "type_group": "Payments & Infrastructure", "share": 0.25},
    {"cohort_order": 7, "type_group": "Consumer Banking & Wealth", "share": 0.20},
    {"cohort_order": 7, "type_group": "Lending & BNPL", "share": 0.15},
    {"cohort_order": 7, "type_group": "Insurtech", "share": 0.10},
    {"cohort_order": 7, "type_group": "Crypto & Web3", "share": 0.20},
    {"cohort_order": 7, "type_group": "AI-Native / Stablecoin / CFO", "share": 0.10},
    {"cohort_order": 8, "type_group": "Payments & Infrastructure", "share": 0.20},
    {"cohort_order": 8, "type_group": "Consumer Banking & Wealth", "share": 0.10},
    {"cohort_order": 8, "type_group": "Lending & BNPL", "share": 0.10},
    {"cohort_order": 8, "type_group": "Insurtech", "share": 0.05},
    {"cohort_order": 8, "type_group": "Crypto & Web3", "share": 0.20},
    {"cohort_order": 8, "type_group": "AI-Native / Stablecoin / CFO", "share": 0.35},
]


def build_cohort_dataframe() -> pd.DataFrame:
    """Compute did-well and not-well amounts from cohort pools and shares."""
    df = pd.DataFrame(COHORT_SPLIT_ROWS).sort_values("cohort_order").reset_index(drop=True)
    df["did_well_b"] = (df["funding_pool_b"] * df["did_well_share"]).round(1)
    df["not_well_b"] = (df["funding_pool_b"] - df["did_well_b"]).round(1)
    df["did_well_share_pct"] = (df["did_well_share"] * 100).round(1)
    df["not_well_share_pct"] = (100 - df["did_well_share_pct"]).round(1)
    df["method"] = "estimated_split"
    return df[
        [
            "cohort_order",
            "cohort",
            "era",
            "funding_pool_b",
            "did_well_b",
            "not_well_b",
            "did_well_share_pct",
            "not_well_share_pct",
            "method",
        ]
    ]


def build_type_group_mix_dataframe(cohort_df: pd.DataFrame) -> pd.DataFrame:
    """Build estimated type-group composition by cohort."""
    mix = pd.DataFrame(TYPE_GROUP_MIX_SHARES)
    merged = mix.merge(
        cohort_df[["cohort_order", "cohort", "era", "funding_pool_b"]],
        on="cohort_order",
        how="left",
    )
    merged["share_pct"] = (merged["share"] * 100).round(1)
    merged["funding_b"] = (merged["funding_pool_b"] * merged["share"]).round(2)
    merged["method"] = "estimated_mix"

    return merged[
        [
            "cohort_order",
            "cohort",
            "era",
            "type_group",
            "share_pct",
            "funding_b",
            "method",
        ]
    ].sort_values(["cohort_order", "type_group"])


def write_csvs(cohort_df: pd.DataFrame, type_mix_df: pd.DataFrame) -> None:
    """Write cohort split and anchor driver CSV files."""
    cohort_path = DATA_DIR / "fintech_cohort_outcome_split_estimated.csv"
    anchors_path = DATA_DIR / "fintech_cohort_outcome_driver_anchors.csv"
    cohort_types_path = DATA_DIR / "fintech_cohort_company_type_classification.csv"
    type_mix_path = DATA_DIR / "fintech_cohort_type_group_mix_estimated.csv"

    cohort_df.to_csv(cohort_path, index=False)
    pd.DataFrame(DRIVER_ANCHOR_ROWS).to_csv(anchors_path, index=False)
    pd.DataFrame(COHORT_TYPE_CLASSIFICATION_ROWS).sort_values("cohort_order").to_csv(cohort_types_path, index=False)
    type_mix_df.to_csv(type_mix_path, index=False)

    print(f"Saved: {cohort_path}")
    print(f"Saved: {anchors_path}")
    print(f"Saved: {cohort_types_path}")
    print(f"Saved: {type_mix_path}")


def plot_chart(cohort_df: pd.DataFrame) -> None:
    """Stacked bar chart of cohort-level did-well vs not-well funding."""
    labels = [f"{row['cohort']}\n{row['era']}" for _, row in cohort_df.iterrows()]
    did_well = cohort_df["did_well_b"].to_numpy()
    not_well = cohort_df["not_well_b"].to_numpy()
    share = cohort_df["did_well_share_pct"].to_numpy()
    x = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(16, 9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    color_well = "#1D4ED8"
    color_not = "#EF4444"

    bars_well = ax.bar(x, did_well, width=0.68, label="Did well", color=color_well, edgecolor="white", linewidth=0.8)
    bars_not = ax.bar(
        x,
        not_well,
        width=0.68,
        bottom=did_well,
        label="Not well",
        color=color_not,
        edgecolor="white",
        linewidth=0.8,
    )

    for bw, bn, pct in zip(bars_well, bars_not, share):
        top = bw.get_height() + bn.get_height()
        ax.text(
            bw.get_x() + bw.get_width() / 2,
            top + 2.0,
            f"{pct:.0f}% did well",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#111827",
            fontweight="bold",
        )

    ax.set_title("Estimated Fintech Funding Split by Cohort: Did Well vs Not Well", fontsize=20, fontweight="bold", pad=16)
    ax.text(
        0.5,
        1.02,
        "Cohort pools are estimated from memo funding tables; shares are scenario assumptions grounded by listed company/category outcomes.",
        transform=ax.transAxes,
        ha="center",
        fontsize=10,
        color="#6B7280",
    )
    ax.set_ylabel("Funding (USD Billions)", fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.grid(axis="y", alpha=0.2, linestyle="--")
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="upper left", frameon=False, fontsize=11)
    ax.set_ylim(0, float((did_well + not_well).max() + 18))

    total_pool = float(cohort_df["funding_pool_b"].sum())
    total_well = float(cohort_df["did_well_b"].sum())
    total_not = float(cohort_df["not_well_b"].sum())
    summary = (
        f"Total pool: ${total_pool:.1f}B  |  "
        f"Did well: ${total_well:.1f}B ({100 * total_well / total_pool:.1f}%)  |  "
        f"Not well: ${total_not:.1f}B ({100 * total_not / total_pool:.1f}%)"
    )
    ax.text(
        0.5,
        -0.17,
        summary,
        transform=ax.transAxes,
        ha="center",
        fontsize=10,
        color="#111827",
        fontweight="bold",
    )

    fig.text(
        0.5,
        0.01,
        "Sources: memos/fintech-market-analysis.md, data/fintech_funding_data.py, scripts/generate_fintech_scatter.py",
        ha="center",
        fontsize=9,
        color="#6B7280",
        style="italic",
    )
    fig.tight_layout(rect=[0.02, 0.05, 0.98, 0.95])

    out_path = CHART_DIR / "fintech_cohort_outcome_split_estimated.png"
    fig.savefig(out_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {out_path}")


def plot_type_group_mix_chart(type_mix_df: pd.DataFrame) -> None:
    """Stacked chart of estimated type-group composition by cohort."""
    chart_df = type_mix_df.copy()
    chart_df["label"] = chart_df["cohort"] + "\n" + chart_df["era"]

    pivot = chart_df.pivot_table(
        index=["cohort_order", "label"],
        columns="type_group",
        values="funding_b",
        aggfunc="sum",
        fill_value=0.0,
    ).sort_index()

    labels = [idx[1] for idx in pivot.index]
    x = np.arange(len(labels))

    colors = {
        "Payments & Infrastructure": "#2563EB",
        "Consumer Banking & Wealth": "#06B6D4",
        "Lending & BNPL": "#F59E0B",
        "Insurtech": "#10B981",
        "Crypto & Web3": "#7C3AED",
        "AI-Native / Stablecoin / CFO": "#111827",
    }

    fig, ax = plt.subplots(figsize=(16, 9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    bottom = np.zeros(len(labels))
    order = list(colors.keys())
    for group in order:
        vals = pivot[group].to_numpy() if group in pivot.columns else np.zeros(len(labels))
        ax.bar(
            x,
            vals,
            bottom=bottom,
            width=0.72,
            label=group,
            color=colors[group],
            edgecolor="white",
            linewidth=0.7,
        )
        bottom += vals

    ax.set_title("Estimated Company-Type Mix by Fintech Cohort", fontsize=20, fontweight="bold", pad=16)
    ax.text(
        0.5,
        1.02,
        "Stacked by estimated type-group funding contribution within each cohort pool.",
        transform=ax.transAxes,
        ha="center",
        fontsize=10,
        color="#6B7280",
    )
    ax.set_ylabel("Funding (USD Billions)", fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.grid(axis="y", alpha=0.2, linestyle="--")
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(
        ncol=3,
        loc="upper left",
        bbox_to_anchor=(0.0, 1.0),
        frameon=False,
        fontsize=10,
    )

    fig.text(
        0.5,
        0.01,
        "Source basis: memos/fintech-market-analysis.md cohort taxonomy; mix is an estimated decomposition.",
        ha="center",
        fontsize=9,
        color="#6B7280",
        style="italic",
    )
    fig.tight_layout(rect=[0.02, 0.05, 0.98, 0.95])

    out_path = CHART_DIR / "fintech_cohort_type_group_mix_estimated.png"
    fig.savefig(out_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    print("Generating fintech cohort outcome split artifacts...")
    cohort_df = build_cohort_dataframe()
    type_mix_df = build_type_group_mix_dataframe(cohort_df)
    write_csvs(cohort_df, type_mix_df)
    plot_chart(cohort_df)
    plot_type_group_mix_chart(type_mix_df)
    print("Done.")
