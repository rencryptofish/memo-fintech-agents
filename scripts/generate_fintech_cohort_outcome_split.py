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


def write_csvs(cohort_df: pd.DataFrame) -> None:
    """Write cohort split and anchor driver CSV files."""
    cohort_path = DATA_DIR / "fintech_cohort_outcome_split_estimated.csv"
    anchors_path = DATA_DIR / "fintech_cohort_outcome_driver_anchors.csv"

    cohort_df.to_csv(cohort_path, index=False)
    pd.DataFrame(DRIVER_ANCHOR_ROWS).to_csv(anchors_path, index=False)

    print(f"Saved: {cohort_path}")
    print(f"Saved: {anchors_path}")


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


if __name__ == "__main__":
    print("Generating fintech cohort outcome split artifacts...")
    cohort_df = build_cohort_dataframe()
    write_csvs(cohort_df)
    plot_chart(cohort_df)
    print("Done.")
