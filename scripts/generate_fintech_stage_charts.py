"""
Generate fintech funding stage breakdown charts and CSVs.

Outputs:
  - charts/fintech/fintech_funding_by_stage_over_time.png
  - charts/fintech/fintech_category_maturity_heatmap_late_stage_share.png
  - charts/fintech/fintech_stage_mix_by_category_2025.png
  - data/fintech_funding_stage_year_category_estimated.csv
  - data/fintech_stage_breakdown_by_year_category_wide_estimated.csv
  - data/fintech_stage_totals_by_year_estimated.csv
  - data/fintech_category_maturity_late_stage_share_estimated.csv

Method:
  Base category-year funding comes from data/fintech_funding_data.py.
  Stage splits are estimated from two factors:
    1) category maturity (older/more scaled categories skew later-stage),
    2) market-cycle regime by year (mania years skew mega rounds; winter years
       skew seed/early).
"""

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CHART_OUT = ROOT / "charts" / "fintech"
DATA_OUT = ROOT / "data"
CHART_OUT.mkdir(parents=True, exist_ok=True)
DATA_OUT.mkdir(parents=True, exist_ok=True)

# Ensure project root is importable when script runs from /scripts.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.fintech_funding_data import FUNDING_BY_CATEGORY, YEARS


STAGES = [
    "Seed / Pre-Seed",
    "Early VC (Series A/B)",
    "Late VC (Series C+)",
    "Growth / Mega",
]

STAGE_COLORS = {
    "Seed / Pre-Seed": "#22C55E",
    "Early VC (Series A/B)": "#3B82F6",
    "Late VC (Series C+)": "#7C3AED",
    "Growth / Mega": "#EF4444",
}


# Relative maturity in 2015. Higher = more late-stage skew.
CATEGORY_MATURITY_2015 = {
    "Payments": 0.82,
    "Lending / Credit": 0.78,
    "Crypto / Blockchain": 0.25,
    "Insurtech": 0.30,
    "Wealthtech / Capital Markets": 0.65,
    "Neobanks / Digital Banking": 0.20,
    "BNPL": 0.05,
    "Regtech / Compliance": 0.18,
    "Embedded Finance / BaaS": 0.10,
    "B2B Fintech Infrastructure": 0.45,
}

# Annual maturity progression applied to each category.
ANNUAL_MATURITY_STEP = 0.035


# Multipliers per year capturing market regime effects on stage mix.
YEAR_STAGE_MULTIPLIERS = {
    2015: {"Seed / Pre-Seed": 1.10, "Early VC (Series A/B)": 1.05, "Late VC (Series C+)": 0.95, "Growth / Mega": 0.75},
    2016: {"Seed / Pre-Seed": 1.08, "Early VC (Series A/B)": 1.04, "Late VC (Series C+)": 0.96, "Growth / Mega": 0.80},
    2017: {"Seed / Pre-Seed": 1.05, "Early VC (Series A/B)": 1.02, "Late VC (Series C+)": 0.98, "Growth / Mega": 0.85},
    2018: {"Seed / Pre-Seed": 0.95, "Early VC (Series A/B)": 0.97, "Late VC (Series C+)": 1.05, "Growth / Mega": 1.10},
    2019: {"Seed / Pre-Seed": 0.92, "Early VC (Series A/B)": 0.95, "Late VC (Series C+)": 1.08, "Growth / Mega": 1.15},
    2020: {"Seed / Pre-Seed": 1.00, "Early VC (Series A/B)": 1.03, "Late VC (Series C+)": 0.98, "Growth / Mega": 0.95},
    2021: {"Seed / Pre-Seed": 0.80, "Early VC (Series A/B)": 0.88, "Late VC (Series C+)": 1.15, "Growth / Mega": 1.45},
    2022: {"Seed / Pre-Seed": 0.95, "Early VC (Series A/B)": 1.00, "Late VC (Series C+)": 1.05, "Growth / Mega": 1.20},
    2023: {"Seed / Pre-Seed": 1.25, "Early VC (Series A/B)": 1.15, "Late VC (Series C+)": 0.90, "Growth / Mega": 0.55},
    2024: {"Seed / Pre-Seed": 1.15, "Early VC (Series A/B)": 1.08, "Late VC (Series C+)": 0.95, "Growth / Mega": 0.70},
    2025: {"Seed / Pre-Seed": 1.02, "Early VC (Series A/B)": 1.00, "Late VC (Series C+)": 1.05, "Growth / Mega": 1.05},
}


def _category_maturity_score(category: str, year: int) -> float:
    """Compute category maturity score in [0.05, 0.95]."""
    base = CATEGORY_MATURITY_2015.get(category, 0.30)
    maturity = base + ANNUAL_MATURITY_STEP * (year - min(YEARS))
    return float(np.clip(maturity, 0.05, 0.95))


def _base_stage_split_from_maturity(maturity: float) -> dict[str, float]:
    """
    Convert maturity score to baseline stage share.

    At low maturity: more seed/early.
    At high maturity: more late/growth.
    """
    split = {
        "Seed / Pre-Seed": 0.30 - 0.22 * maturity,       # 30% -> 8%
        "Early VC (Series A/B)": 0.45 - 0.18 * maturity,  # 45% -> 27%
        "Late VC (Series C+)": 0.20 + 0.20 * maturity,    # 20% -> 40%
        "Growth / Mega": 0.05 + 0.20 * maturity,          # 5%  -> 25%
    }
    total = sum(split.values())
    return {k: v / total for k, v in split.items()}


def _stage_split(category: str, year: int) -> dict[str, float]:
    """Return normalized stage split for category-year after cycle adjustment."""
    maturity = _category_maturity_score(category, year)
    base_split = _base_stage_split_from_maturity(maturity)
    multipliers = YEAR_STAGE_MULTIPLIERS[year]

    adjusted = {stage: base_split[stage] * multipliers[stage] for stage in STAGES}
    norm = sum(adjusted.values())
    return {stage: adjusted[stage] / norm for stage in STAGES}


def build_stage_dataframe() -> pd.DataFrame:
    """Build year-category-stage funding dataset."""
    rows: list[dict[str, float | int | str]] = []

    for category, yearly in FUNDING_BY_CATEGORY.items():
        for year in YEARS:
            total_b = float(yearly.get(year, 0.0))
            stage_share = _stage_split(category, year) if total_b > 0 else {s: 0.0 for s in STAGES}
            maturity_score = _category_maturity_score(category, year)

            for stage in STAGES:
                share = stage_share[stage]
                rows.append(
                    {
                        "year": year,
                        "category": category,
                        "stage": stage,
                        "funding_b": round(total_b * share, 4),
                        "stage_share_pct": round(share * 100.0, 2),
                        "category_total_b": round(total_b, 4),
                        "maturity_score": round(maturity_score, 3),
                    }
                )

    return pd.DataFrame(rows)


def chart_stage_over_time(df: pd.DataFrame) -> None:
    """Global funding by stage over time (stacked bars + late-stage share line)."""
    stage_year = (
        df.groupby(["year", "stage"], as_index=False)["funding_b"]
        .sum()
        .pivot(index="year", columns="stage", values="funding_b")
        .reindex(index=YEARS, columns=STAGES, fill_value=0.0)
    )

    fig, ax = plt.subplots(figsize=(18, 10), dpi=180)
    bottoms = np.zeros(len(stage_year))
    x = np.arange(len(stage_year))

    for stage in STAGES:
        vals = stage_year[stage].values
        ax.bar(
            x,
            vals,
            bottom=bottoms,
            width=0.72,
            color=STAGE_COLORS[stage],
            edgecolor="white",
            linewidth=0.35,
            label=stage,
        )
        bottoms += vals

    totals = stage_year.sum(axis=1)
    late_growth_share = (stage_year["Late VC (Series C+)"] + stage_year["Growth / Mega"]) / totals * 100.0

    ax2 = ax.twinx()
    ax2.plot(x, late_growth_share.values, color="#111827", linewidth=2.2, marker="o", markersize=5.5)
    ax2.set_ylim(20, 80)
    ax2.set_ylabel("Late+Growth Share (%)", fontsize=12, color="#111827")
    ax2.tick_params(axis="y", labelcolor="#111827")

    for idx in [0, 3, 6, 8, 10]:
        ax2.annotate(
            f"{late_growth_share.iloc[idx]:.1f}%",
            xy=(idx, late_growth_share.iloc[idx]),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=8,
            color="#111827",
            fontweight="bold",
        )

    ax.set_title("Global Fintech VC Funding by Stage (Estimated, 2015-2025)", fontsize=20, fontweight="bold", pad=18)
    ax.text(
        0.5,
        1.02,
        "Stage split estimated from category maturity and market-cycle regime",
        transform=ax.transAxes,
        ha="center",
        fontsize=10,
        color="#6B7280",
    )
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Funding ($ Billions)", fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(stage_year.index.astype(str))
    ax.grid(axis="y", alpha=0.2, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax2.spines["top"].set_visible(False)
    ax.legend(loc="upper left", fontsize=10, framealpha=0.95, edgecolor="#DDD")

    fig.text(
        0.5,
        0.01,
        "Base totals: data/fintech_funding_data.py (category-year VC estimates). "
        "Stage splits are modeled estimates for analytical comparison.",
        ha="center",
        fontsize=8.5,
        color="#6B7280",
        style="italic",
    )
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    out = CHART_OUT / "fintech_funding_by_stage_over_time.png"
    fig.savefig(out, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {out}")


def chart_category_maturity_heatmap(df: pd.DataFrame) -> None:
    """Heatmap of late-stage share by category and year as maturity proxy."""
    late = (
        df[df["stage"].isin(["Late VC (Series C+)", "Growth / Mega"])]
        .groupby(["year", "category"], as_index=False)["funding_b"]
        .sum()
        .rename(columns={"funding_b": "late_plus_growth_b"})
    )
    totals = (
        df.groupby(["year", "category"], as_index=False)["category_total_b"]
        .max()
    )

    merged = late.merge(totals, on=["year", "category"], how="left")
    merged["late_stage_share_pct"] = np.where(
        merged["category_total_b"] > 0,
        merged["late_plus_growth_b"] / merged["category_total_b"] * 100.0,
        0.0,
    )

    pivot = (
        merged.pivot(index="category", columns="year", values="late_stage_share_pct")
        .reindex(columns=YEARS)
    )

    # Sort by latest year maturity descending.
    pivot = pivot.sort_values(by=YEARS[-1], ascending=False)

    fig, ax = plt.subplots(figsize=(18, 9), dpi=180)
    im = ax.imshow(pivot.values, cmap="YlGnBu", aspect="auto", vmin=20, vmax=80)

    ax.set_xticks(np.arange(len(YEARS)))
    ax.set_xticklabels(YEARS, fontsize=10)
    ax.set_yticks(np.arange(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=10)

    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            val = pivot.iloc[i, j]
            color = "white" if val >= 55 else "#111827"
            ax.text(j, i, f"{val:.0f}%", ha="center", va="center", fontsize=8, color=color, fontweight="bold")

    cbar = plt.colorbar(im, ax=ax, shrink=0.88, pad=0.015)
    cbar.set_label("Late + Growth Stage Share (%)", fontsize=11)

    ax.set_title("Fintech Category Maturity by Year (Late-Stage Share, Estimated)", fontsize=19, fontweight="bold", pad=14)
    ax.text(
        0.5,
        1.02,
        "Higher percentages indicate category funding skewed to later-stage rounds",
        transform=ax.transAxes,
        ha="center",
        fontsize=10,
        color="#6B7280",
    )

    fig.text(
        0.5,
        0.01,
        "Maturity proxy = (Late VC + Growth/Mega) / category-year funding. "
        "Stage mix estimated from modeled stage distributions.",
        ha="center",
        fontsize=8.5,
        color="#6B7280",
        style="italic",
    )
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    out = CHART_OUT / "fintech_category_maturity_heatmap_late_stage_share.png"
    fig.savefig(out, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {out}")


def chart_stage_mix_latest_year(df: pd.DataFrame, year: int = 2025) -> None:
    """Horizontal stacked bars showing stage mix by category in latest year."""
    latest = df[df["year"] == year].copy()
    pivot = (
        latest.pivot_table(index="category", columns="stage", values="funding_b", aggfunc="sum")
        .reindex(columns=STAGES)
        .fillna(0.0)
    )

    totals = pivot.sum(axis=1)
    pct = pivot.div(totals, axis=0) * 100.0
    sort_key = pct["Late VC (Series C+)"] + pct["Growth / Mega"]
    pct = pct.loc[sort_key.sort_values(ascending=False).index]
    totals = totals.loc[pct.index]

    fig, ax = plt.subplots(figsize=(18, 10), dpi=180)
    y_pos = np.arange(len(pct.index))
    left = np.zeros(len(pct.index))

    for stage in STAGES:
        vals = pct[stage].values
        ax.barh(
            y_pos,
            vals,
            left=left,
            color=STAGE_COLORS[stage],
            edgecolor="white",
            linewidth=0.35,
            label=stage,
        )
        left += vals

    for i, category in enumerate(pct.index):
        ax.text(
            101.0,
            i,
            f"${totals.loc[category]:.1f}B",
            va="center",
            fontsize=9,
            color="#111827",
            fontweight="bold",
        )

    ax.set_xlim(0, 110)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(pct.index, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Stage Mix (%)", fontsize=12)
    ax.set_title(f"Fintech Funding Stage Mix by Category ({year}, Estimated)", fontsize=19, fontweight="bold", pad=14)
    ax.text(
        0.5,
        1.02,
        "Categories sorted by Late+Growth share (maturity proxy)",
        transform=ax.transAxes,
        ha="center",
        fontsize=10,
        color="#6B7280",
    )
    ax.grid(axis="x", alpha=0.2, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="lower right", fontsize=9.5, framealpha=0.95, edgecolor="#DDD")

    fig.text(
        0.5,
        0.01,
        "Right-side labels show absolute category funding in the selected year.",
        ha="center",
        fontsize=8.5,
        color="#6B7280",
        style="italic",
    )
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    out = CHART_OUT / "fintech_stage_mix_by_category_2025.png"
    fig.savefig(out, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {out}")


def export_csvs(df: pd.DataFrame) -> None:
    """Export detailed and summary stage datasets."""
    full_out = DATA_OUT / "fintech_funding_stage_year_category_estimated.csv"
    df.to_csv(full_out, index=False)
    print(f"Saved: {full_out}")

    wide = (
        df.pivot_table(
            index=["year", "category", "category_total_b"],
            columns="stage",
            values="funding_b",
            aggfunc="sum",
        )
        .reset_index()
        .rename_axis(None, axis=1)
    )
    wide["late_plus_growth_b"] = wide["Late VC (Series C+)"] + wide["Growth / Mega"]
    wide["late_stage_share_pct"] = np.where(
        wide["category_total_b"] > 0,
        wide["late_plus_growth_b"] / wide["category_total_b"] * 100.0,
        0.0,
    )
    wide = wide.sort_values(["year", "category"])
    wide_out = DATA_OUT / "fintech_stage_breakdown_by_year_category_wide_estimated.csv"
    wide.to_csv(wide_out, index=False)
    print(f"Saved: {wide_out}")

    stage_totals = (
        df.groupby(["year", "stage"], as_index=False)["funding_b"]
        .sum()
        .sort_values(["year", "stage"])
    )
    stage_totals_out = DATA_OUT / "fintech_stage_totals_by_year_estimated.csv"
    stage_totals.to_csv(stage_totals_out, index=False)
    print(f"Saved: {stage_totals_out}")

    maturity = (
        df[df["stage"].isin(["Late VC (Series C+)", "Growth / Mega"])]
        .groupby(["year", "category"], as_index=False)["funding_b"]
        .sum()
        .rename(columns={"funding_b": "late_plus_growth_b"})
        .merge(
            df.groupby(["year", "category"], as_index=False)["category_total_b"].max(),
            on=["year", "category"],
            how="left",
        )
    )
    maturity["late_stage_share_pct"] = np.where(
        maturity["category_total_b"] > 0,
        maturity["late_plus_growth_b"] / maturity["category_total_b"] * 100.0,
        0.0,
    )
    maturity = maturity.sort_values(["category", "year"])
    maturity_out = DATA_OUT / "fintech_category_maturity_late_stage_share_estimated.csv"
    maturity.to_csv(maturity_out, index=False)
    print(f"Saved: {maturity_out}")


def main() -> None:
    print("Building fintech stage model dataset...")
    df = build_stage_dataframe()
    export_csvs(df)

    print("Generating chart: stage over time...")
    chart_stage_over_time(df)

    print("Generating chart: category maturity heatmap...")
    chart_category_maturity_heatmap(df)

    print("Generating chart: category stage mix (2025)...")
    chart_stage_mix_latest_year(df, year=2025)

    print("Done.")


if __name__ == "__main__":
    main()
