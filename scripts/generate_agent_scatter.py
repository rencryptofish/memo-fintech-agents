"""
Agent Economy: Funding vs Revenue Trajectory by Category (2023-2025)
Scatter plot with connected lines showing each category's evolution.

X-axis: Cumulative category funding ($B)
Y-axis: Estimated category ARR ($M)
Lines connect each category across time snapshots.
"""

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# DATA: Agent Economy Categories — Funding & Revenue at Year-End Snapshots
#
# Sources: agent-economy-memo.md, investment-opportunities.md,
#          fintech-agents-intersection.md, Crunchbase, PitchBook, TechCrunch,
#          Bessemer State of the Cloud, company press releases
#
# Funding = cumulative VC raised by companies in the category
# Revenue = estimated combined ARR of leading companies in the category
# ─────────────────────────────────────────────────────────────────────────────

TIME_POINTS = ["End 2023", "End 2024", "Early 2026"]

# {category: [(funding_B, arr_M), ...]} — one tuple per time point
CATEGORIES = {
    "Coding Agents": [
        # 2023: Copilot ~$100M ARR, Cursor early, Tabnine ~$55M raised
        # Cumulative: Cursor ~$60M, Windsurf ~$70M, Poolside early, Augment early, Copilot (MSFT)
        (1.5, 120),
        # 2024: Cursor $100M+ ARR, Copilot $300M+, Devin $175M raised, Windsurf $300M+
        (3.5, 550),
        # Early 2026: Cursor $1B+ ARR, Copilot $500M+, Devin $2.175B raised, Augment $252M
        # Total funding: Cursor $1.1B+ + Devin $2.175B + Windsurf $300M+ + Augment $252M + Poolside $400M+ + Magic $320M + others
        (7.5, 2200),
    ],
    "CX / Support Agents": [
        # 2023: Sierra $110M raised, Decagon early, Ada $190M cumulative
        (0.5, 25),
        # 2024: Sierra $285M cumulative, Decagon $100M, others growing
        (0.8, 80),
        # Early 2026: Sierra $450M+ ($100M ARR in 7 qtrs, $10B val), Decagon, PolyAI, Parloa
        (1.2, 250),
    ],
    "Legal Agents": [
        # 2023: Harvey ~$100M raised, EvenUp ~$100M, Casetext acquired
        (0.25, 20),
        # 2024: Harvey ~$280M cumulative ($50M ARR), EvenUp $250M
        (0.55, 65),
        # Early 2026: Harvey $1B+ raised ($195M ARR, 3.9x YoY), EvenUp $385M, Spellbook
        (1.8, 350),
    ],
    "Healthcare Agents": [
        # 2023: Abridge ~$100M cumulative, others early
        (0.15, 15),
        # 2024: Abridge $300M+ raised, expanding to 150+ health systems
        (0.4, 50),
        # Early 2026: Abridge $600M+ raised ($5.3B val), 50M+ conversations
        (0.75, 150),
    ],
    "Agent Security": [
        # 2023: Protect AI ~$60M, Lakera ~$20M, others early
        (0.12, 5),
        # 2024: Noma $32M, Protect AI $108M+, Prompt Security $18M
        (0.25, 20),
        # Early 2026: Noma $132M (1,300% ARR growth), Keycard $38M, CalypsoAI $50M+
        (0.42, 120),
    ],
    "Agent Infra\n(Compute/Memory/Obs)": [
        # 2023: E2B ~$11M, Mem0 seed, Modal $100M+, Arize ~$60M
        (0.20, 8),
        # 2024: E2B $14M, Mem0 growing, Modal $164M, Arize $131M, Braintrust $36M
        (0.45, 35),
        # Early 2026: E2B $32M (7-fig/mo new rev), Mem0 $24M (186M API calls/qtr),
        # Daytona $38M (doubling every 6 wks), Modal $164M
        (0.65, 130),
    ],
    "Agent Platforms\n& Frameworks": [
        # 2023: LangChain $25M, others minimal
        (0.05, 5),
        # 2024: CrewAI $18M, Composio early, LangSmith growing
        (0.10, 25),
        # Early 2026: Composio $29M (200+ paying cos), CrewAI $18M ($3.2M rev),
        # LangChain $20-30M ARR est
        (0.20, 60),
    ],
    "HR / Recruiting\nAgents": [
        # 2023: Mercor early, Paradox ~$150M cumulative
        (0.20, 12),
        # 2024: Mercor $100M+, Paradox $200M+
        (0.35, 40),
        # Early 2026: Mercor $2B val, Paradox, HireVue, Findem
        (0.50, 90),
    ],
    "Sales / Marketing\nAgents": [
        # 2023: 11x $24M, Clay ~$30M, Artisan early
        (0.10, 8),
        # 2024: 11x $50M+, Clay $62M, Artisan $25M+, Relevance $18M
        (0.20, 30),
        # Early 2026: category growing, Clay strong traction
        (0.35, 70),
    ],
    "Agentic Payments\n(Intersection)": [
        # 2023: category barely existed
        (0.01, 0.5),
        # 2024: Kite early, Skyfire $9.5M, Catena $18M seed, x402 not yet launched
        (0.05, 2),
        # Early 2026: Kite $33M, Catena $18M, Skyfire $9.5M, Natural $9.8M,
        # Crossmint $23.6M (1,100% rev growth). x402: 140M+ txns
        (0.12, 15),
    ],
}

# Colors for each category
COLORS = {
    "Coding Agents":               "#2563EB",
    "CX / Support Agents":         "#10B981",
    "Legal Agents":                 "#7C3AED",
    "Healthcare Agents":           "#EC4899",
    "Agent Security":              "#EF4444",
    "Agent Infra\n(Compute/Memory/Obs)": "#F59E0B",
    "Agent Platforms\n& Frameworks": "#8B5CF6",
    "HR / Recruiting\nAgents":     "#06B6D4",
    "Sales / Marketing\nAgents":   "#14B8A6",
    "Agentic Payments\n(Intersection)": "#0F172A",
}

# Marker sizes by time point (bigger = more recent)
MARKER_SIZES = [40, 80, 180]


def _annotate_non_overlapping_labels(ax, label_queue, min_gap_px=18):
    if not label_queue:
        return

    px_per_pt = ax.figure.dpi / 72.0
    y_min = ax.bbox.y0 + 10
    y_max = ax.bbox.y1 - 10

    grouped = {"right": [], "left": []}
    for item in label_queue:
        _, y_disp = ax.transData.transform((item["x"], item["y"]))
        row = {**item, "y_disp": y_disp, "base_y": y_disp + item["dy"] * px_per_pt}
        side = "right" if item["dx"] >= 0 else "left"
        grouped[side].append(row)

    for side_items in grouped.values():
        side_items.sort(key=lambda row: row["base_y"])
        prev_y = -1e9
        for row in side_items:
            placed_y = max(row["base_y"], prev_y + min_gap_px)
            row["placed_y"] = placed_y
            prev_y = placed_y

        if side_items:
            overflow = side_items[-1]["placed_y"] - y_max
            if overflow > 0:
                for row in side_items:
                    row["placed_y"] -= overflow

            underflow = y_min - side_items[0]["placed_y"]
            if underflow > 0:
                for row in side_items:
                    row["placed_y"] += underflow

        for row in side_items:
            dy_points = (row["placed_y"] - row["y_disp"]) / px_per_pt
            ha = "left" if row["dx"] >= 0 else "right"
            ax.annotate(
                row["label"],
                xy=(row["x"], row["y"]),
                xytext=(row["dx"], dy_points), textcoords="offset points",
                ha=ha,
                fontsize=10, fontweight="bold", color=row["color"],
                path_effects=[pe.withStroke(linewidth=3, foreground="white")],
                bbox=dict(boxstyle="round,pad=0.22", facecolor="white", edgecolor="none", alpha=0.78),
                zorder=5,
            )


def generate_scatter():
    fig, ax = plt.subplots(figsize=(20, 12))

    final_label_queue = []
    for cat_name, points in CATEGORIES.items():
        color = COLORS[cat_name]
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]

        # Draw connecting line
        ax.plot(xs, ys, color=color, linewidth=2, alpha=0.5, zorder=1)

        # Draw arrows between points to show direction
        for i in range(len(xs) - 1):
            ax.annotate(
                "", xy=(xs[i + 1], ys[i + 1]), xytext=(xs[i], ys[i]),
                arrowprops=dict(
                    arrowstyle="-|>", color=color, lw=1.8,
                    mutation_scale=12, alpha=0.5,
                ),
                zorder=1,
            )

        # Draw scatter points (larger for more recent)
        for i, (x, y) in enumerate(points):
            ax.scatter(
                x, y, s=MARKER_SIZES[i], color=color,
                edgecolors="white", linewidth=1, zorder=3,
                marker="o",
            )

        # Label at the final (most recent) point
        final_x, final_y = xs[-1], ys[-1]
        # Clean name for label (remove newlines)
        label = cat_name.replace("\n", " ")

        # Offset labels to avoid overlap
        offsets = {
            "Coding Agents": (20, -8),
            "CX / Support Agents": (14, 12),
            "Legal Agents": (16, 10),
            "Healthcare Agents": (14, 8),
            "Agent Security": (14, 10),
            "Agent Infra\n(Compute/Memory/Obs)": (14, -14),
            "Agent Platforms\n& Frameworks": (12, 10),
            "HR / Recruiting\nAgents": (14, -12),
            "Sales / Marketing\nAgents": (12, -14),
            "Agentic Payments\n(Intersection)": (12, -14),
        }
        dx, dy = offsets.get(cat_name, (10, 5))
        final_label_queue.append(
            {
                "x": final_x,
                "y": final_y,
                "label": label,
                "color": color,
                "dx": dx,
                "dy": dy,
            }
        )

    # Log scale on both axes for readability (funding spans 0.01-7.5B, ARR 0.5-2200M)
    ax.set_xscale("log")
    ax.set_yscale("log")

    # Axis formatting
    ax.set_xlabel("Cumulative Category Funding ($ Billions)", fontsize=14, labelpad=12)
    ax.set_ylabel("Estimated Category ARR ($ Millions)", fontsize=14, labelpad=12)

    # Custom tick labels
    x_ticks = [0.01, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([f"${v}B" if v >= 1 else f"${int(v*1000)}M" for v in x_ticks],
                       fontsize=10)

    y_ticks = [1, 5, 10, 25, 50, 100, 250, 500, 1000, 2500]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([f"${v}M" if v < 1000 else f"${v/1000:.1f}B" for v in y_ticks],
                       fontsize=10)

    ax.set_xlim(0.008, 12)
    ax.set_ylim(0.3, 4000)
    _annotate_non_overlapping_labels(ax, final_label_queue, min_gap_px=22)

    # Title
    ax.set_title(
        "AI Agent Economy: Funding vs Revenue Trajectory by Category",
        fontsize=22, fontweight="bold", pad=22, color="#1a1a2e",
    )

    # Subtitle
    ax.text(
        0.5, 1.02,
        "Each dot = time snapshot (End 2023 → End 2024 → Early 2026)  •  "
        "Arrows show direction  •  Larger dots = more recent",
        transform=ax.transAxes, ha="center", fontsize=11, color="#666",
    )

    # Grid
    ax.grid(True, alpha=0.15, which="both", linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Time point legend (dot sizes)
    for i, (label, size) in enumerate(zip(TIME_POINTS, MARKER_SIZES)):
        ax.scatter([], [], s=size, c="#888", edgecolors="white",
                   linewidth=1, label=label)
    legend1 = ax.legend(
        loc="lower right", fontsize=11, title="Time Snapshot",
        title_fontsize=12, framealpha=0.95, edgecolor="#ddd",
    )
    ax.add_artist(legend1)

    # Efficiency reference lines (ARR/Funding ratio)
    for ratio, label_text in [(100, "1x efficiency\n($100M ARR / $100M funding)"),
                               (500, "5x efficiency")]:
        xs_ref = np.linspace(0.008, 12, 100)
        ys_ref = xs_ref * ratio  # $B * ratio = $M ARR
        mask = (ys_ref >= 0.3) & (ys_ref <= 4000) & (xs_ref >= 0.008) & (xs_ref <= 12)
        ax.plot(xs_ref[mask], ys_ref[mask], ":", color="#ccc", linewidth=1.5,
                alpha=0.6, zorder=0)
        # Find a good spot for the label
        mid = len(xs_ref[mask]) // 2
        if mid > 0:
            ax.text(
                xs_ref[mask][mid], ys_ref[mask][mid], label_text,
                fontsize=8.5, color="#aaa", rotation=30,
                ha="center", va="bottom", style="italic",
            )

    # Source note
    fig.text(
        0.5, 0.01,
        "Sources: Crunchbase, PitchBook, TechCrunch, Bessemer, company press releases  |  "
        "Revenue figures are estimates based on publicly available data  |  Feb 2026",
        ha="center", fontsize=9, color="#888", style="italic",
    )

    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    return fig


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent
    print("Generating Agent Economy Scatter: Funding vs Revenue Trajectory...")
    fig = generate_scatter()
    save_path = out / "charts/agent-economy/agent_economy_funding_vs_revenue.png"
    fig.savefig(save_path, dpi=260, bbox_inches="tight", facecolor="white")
    print(f"  Saved: {save_path}")
    plt.close("all")
