"""
Generate a category-to-company map chart for fintech trajectory categories.

Outputs:
  - charts/fintech/fintech_category_company_map.png

Input:
  - data/category_company_map.csv
"""

from pathlib import Path
import textwrap

import matplotlib.pyplot as plt
import pandas as pd


def _wrap_company_list(raw: str, width: int = 48) -> str:
    items = [x.strip() for x in raw.split(";") if x.strip()]
    joined = ", ".join(items)
    return textwrap.fill(joined, width=width)


def generate_chart():
    root = Path(__file__).resolve().parent.parent
    csv_path = root / "data" / "category_company_map.csv"
    out_dir = root / "charts" / "fintech"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "fintech_category_company_map.png"

    df = pd.read_csv(csv_path)

    # Keep display order as defined in CSV.
    rows = []
    for _, row in df.iterrows():
        rows.append(
            [
                row["display_category"],
                str(row["start_year"]),
                row["cohort"],
                _wrap_company_list(row["companies"]),
            ]
        )

    col_labels = ["Category", "Start", "Cohort", "Company Basket (for chart category)"]

    fig, ax = plt.subplots(figsize=(20, 10.5))
    ax.axis("off")

    table = ax.table(
        cellText=rows,
        colLabels=col_labels,
        colLoc="left",
        cellLoc="left",
        colWidths=[0.18, 0.06, 0.22, 0.54],
        loc="center",
    )

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.75)

    # Header style.
    for col in range(len(col_labels)):
        hcell = table[0, col]
        hcell.set_text_props(weight="bold", color="white")
        hcell.set_facecolor("#1f2937")
        hcell.set_edgecolor("#111827")
        hcell.set_linewidth(1.0)

    # Row style with highlight on the intersection category.
    n_rows = len(rows)
    for r in range(1, n_rows + 1):
        row_label = rows[r - 1][0]
        is_intersection = row_label == "Agentic Fintech Intersection"
        for c in range(len(col_labels)):
            cell = table[r, c]
            base = "#ffffff" if r % 2 else "#f8fafc"
            if is_intersection:
                cell.set_facecolor("#e2e8f0")
                cell.set_edgecolor("#334155")
                cell.set_linewidth(1.4)
                if c == 0:
                    cell.set_text_props(weight="bold", color="#0f172a")
            else:
                cell.set_facecolor(base)
                cell.set_edgecolor("#e5e7eb")
                cell.set_linewidth(0.8)

    fig.suptitle(
        "Fintech Trajectory Category Map: Company Baskets",
        fontsize=20,
        fontweight="bold",
        color="#111827",
        y=0.97,
    )
    fig.text(
        0.5,
        0.945,
        "Category baskets aligned to the fintech funding-vs-revenue trajectory and breakdown charts",
        ha="center",
        fontsize=10,
        color="#4b5563",
    )
    fig.text(
        0.5,
        0.015,
        "Source: data/category_company_map.csv  |  Highlighted row = Agentic Fintech Intersection",
        ha="center",
        fontsize=8,
        color="#6b7280",
        style="italic",
    )

    plt.tight_layout(rect=[0.01, 0.03, 0.99, 0.93])
    fig.savefig(out_path, dpi=260, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out_path


if __name__ == "__main__":
    save_path = generate_chart()
    print(f"Saved: {save_path}")
