"""
Generate missing visualization set for the fintech x agent intersection.

Charts:
  1) 01_protocol_launch_timeline.png
  2) 02_protocol_capability_matrix.png
  3) 03_layer_funding_heatmap.png
  4) 04_agent_commerce_readiness_roadmap.png

Data sources:
  - memos/fintech-agents-intersection.md
  - research/market-map.md
"""

from datetime import datetime
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "charts" / "intersection"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BG = "#0F172A"
CARD = "#111827"
GRID = "#334155"
TEXT = "#E5E7EB"
MUTED = "#94A3B8"


def _style_dark(ax: plt.Axes) -> None:
    ax.set_facecolor(CARD)
    ax.grid(True, color=GRID, linestyle="--", alpha=0.35, linewidth=0.8)
    ax.tick_params(colors=TEXT)
    for spine in ax.spines.values():
        spine.set_color(GRID)


def chart_protocol_launch_timeline() -> None:
    """Chronological launch map across key protocols/platforms."""
    events = [
        ("Mastercard Agent Pay", datetime(2025, 4, 1), "card"),
        ("x402 v1", datetime(2025, 5, 6), "crypto"),
        ("ACP", datetime(2025, 9, 1), "fiat"),
        ("AP2", datetime(2025, 9, 15), "orchestration"),
        ("TAP", datetime(2025, 10, 13), "identity"),
        ("PayPal Agent Ready", datetime(2025, 10, 20), "fiat"),
        ("x402 v2", datetime(2025, 12, 11), "crypto"),
        ("UCP", datetime(2026, 1, 15), "orchestration"),
        ("FIS AI Transaction Platform", datetime(2026, 2, 1), "banking"),
    ]
    colors = {
        "crypto": "#22D3EE",
        "fiat": "#60A5FA",
        "orchestration": "#A78BFA",
        "identity": "#FBBF24",
        "card": "#34D399",
        "banking": "#FB7185",
    }

    fig, ax = plt.subplots(figsize=(15, 7), dpi=170)
    fig.patch.set_facecolor(BG)
    _style_dark(ax)

    y_base = 0.0
    ax.hlines(y_base, datetime(2025, 3, 1), datetime(2026, 3, 15), color=GRID, linewidth=2.0)

    for idx, (label, dt, group) in enumerate(events):
        y = 0.18 if idx % 2 == 0 else -0.18
        ax.vlines(dt, y_base, y, color=colors[group], linewidth=2.2, alpha=0.9)
        ax.scatter([dt], [y], s=90, color=colors[group], edgecolor="white", linewidth=1.2, zorder=5)
        ax.text(dt, y + (0.05 if y > 0 else -0.05), label, color=TEXT, fontsize=9,
                ha="center", va="bottom" if y > 0 else "top", fontweight="bold")

    ax.axvline(datetime(2026, 2, 9), color="#F87171", linestyle=":", linewidth=1.6)
    ax.text(datetime(2026, 2, 9), 0.29, "Current snapshot\n(Feb 9, 2026)", color="#FCA5A5",
            fontsize=9, ha="center")

    ax.set_title("Agentic Payments Stack: Protocol Launch Timeline", fontsize=20, fontweight="bold", color=TEXT, pad=16)
    ax.text(0.5, 1.02, "From first protocol release (Apr/May 2025) to cross-stack rollout (Q1 2026)",
            transform=ax.transAxes, ha="center", color=MUTED, fontsize=10)

    ax.set_yticks([])
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right", color=TEXT)
    ax.set_xlim(datetime(2025, 3, 1), datetime(2026, 3, 15))
    ax.set_ylim(-0.35, 0.35)

    fig.text(0.5, 0.01, "Source: memos/fintech-agents-intersection.md (protocol launch timeline notes).",
             ha="center", color=MUTED, fontsize=9, style="italic")
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    out = OUT_DIR / "01_protocol_launch_timeline.png"
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"Saved: {out}")


def chart_protocol_capability_matrix() -> None:
    """Heatmap of protocol capability coverage (0-2 scoring)."""
    protocols = ["x402", "ACP", "AP2", "TAP", "UCP"]
    capabilities = [
        "A2A\nMicropay",
        "Consumer\nCheckout",
        "Rail\nAgnostic",
        "Identity\nTrust",
        "Policy\nAudit",
        "Service\nDiscovery",
        "Dynamic\nNegotiation",
    ]

    # 0 = none, 1 = partial/indirect, 2 = core strength.
    matrix = np.array([
        [2, 0, 1, 0, 0, 1, 0],  # x402
        [0, 2, 0, 1, 1, 0, 0],  # ACP
        [1, 1, 2, 1, 2, 1, 1],  # AP2
        [0, 1, 0, 2, 1, 0, 0],  # TAP
        [0, 2, 1, 1, 1, 2, 1],  # UCP (negotiation is roadmap)
    ])

    fig, ax = plt.subplots(figsize=(14, 8), dpi=170)
    fig.patch.set_facecolor(BG)
    _style_dark(ax)

    im = ax.imshow(matrix, cmap="YlGnBu", vmin=0, vmax=2, aspect="auto")

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            val = int(matrix[i, j])
            txt = "Core" if val == 2 else "Partial" if val == 1 else "None"
            ax.text(j, i, txt, ha="center", va="center", fontsize=8.5,
                    color="#0F172A" if val >= 1 else TEXT, fontweight="bold")

    ax.set_xticks(np.arange(len(capabilities)))
    ax.set_yticks(np.arange(len(protocols)))
    ax.set_xticklabels(capabilities, fontsize=10, color=TEXT)
    ax.set_yticklabels(protocols, fontsize=11, color=TEXT)
    plt.setp(ax.get_xticklabels(), rotation=0)

    ax.set_title("Protocol Capability Matrix: Complementary Roles, Not Direct Substitutes",
                 fontsize=18, fontweight="bold", color=TEXT, pad=16)
    ax.text(0.5, 1.02, "Scoring synthesized from memo descriptions (0 none, 1 partial, 2 core)",
            transform=ax.transAxes, ha="center", color=MUTED, fontsize=10)

    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_ticks([0, 1, 2])
    cbar.set_ticklabels(["None", "Partial", "Core"])
    cbar.ax.tick_params(colors=TEXT)
    cbar.outline.set_edgecolor(GRID)

    fig.text(0.5, 0.01, "Source: memos/fintech-agents-intersection.md (protocol table + narrative).",
             ha="center", color=MUTED, fontsize=9, style="italic")
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    out = OUT_DIR / "02_protocol_capability_matrix.png"
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"Saved: {out}")


def chart_layer_funding_heatmap() -> None:
    """Funding concentration/whitespace by intersection stack layer."""
    layers = [
        "L0 Wallets",
        "L1 Settlement",
        "L2 Authorization",
        "L3 Identity",
        "L4 Commerce",
        "L5 Discovery",
        "L6 Compliance",
        "L7 Orchestration",
    ]
    funding_m = np.array([30, 480, 43, 260, 35, 0, 230, 0], dtype=float)
    assessments = [
        "Underfunded",
        "Well-funded",
        "Underfunded",
        "Best-funded",
        "Underfunded",
        "Severely underfunded",
        "Well-funded",
        "Zero dedicated funding",
    ]

    fig, ax = plt.subplots(figsize=(14, 8), dpi=170)
    fig.patch.set_facecolor(BG)
    _style_dark(ax)

    y = np.arange(len(layers))
    colors = plt.cm.magma((funding_m + 30) / (funding_m.max() + 30))
    bars = ax.barh(y, funding_m, color=colors, edgecolor="#E5E7EB", linewidth=0.6)

    for i, (bar, val, tag) in enumerate(zip(bars, funding_m, assessments)):
        label = f"${val:.0f}M" if val > 0 else "$0M"
        ax.text(bar.get_width() + 8, bar.get_y() + bar.get_height() / 2,
                f"{label}  |  {tag}", va="center", fontsize=9, color=TEXT)

    ax.set_yticks(y)
    ax.set_yticklabels(layers, color=TEXT)
    ax.invert_yaxis()
    ax.set_xlabel("Total Startup Funding (USD Millions)", color=TEXT, fontsize=12)
    ax.set_title("Agent-Fintech Stack Funding Heat Map", fontsize=20, fontweight="bold", color=TEXT, pad=16)
    ax.text(0.5, 1.02, "White-space signal: Discovery (L5) and Orchestration (L7) remain structurally unfunded",
            transform=ax.transAxes, ha="center", color=MUTED, fontsize=10)
    ax.set_xlim(0, 560)

    fig.text(0.5, 0.01, "Source: research/market-map.md (Funding Heat Map table).",
             ha="center", color=MUTED, fontsize=9, style="italic")
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    out = OUT_DIR / "03_layer_funding_heatmap.png"
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"Saved: {out}")


def chart_agent_commerce_readiness_roadmap() -> None:
    """Roadmap/Gantt view of maturity stages from current to 2028."""
    items = [
        ("API call micropayments (x402)", 2025.35, 2026.10, "Live at scale"),
        ("Merchant purchase (ACP/TAP)", 2025.75, 2026.50, "Live, limited"),
        ("Agent-agent negotiation", 2026.55, 2027.50, "Prototype"),
        ("Agent hires contractor agent", 2027.00, 2028.10, "Conceptual"),
        ("Complex multi-party transactions", 2027.00, 2028.00, "Research"),
    ]
    status_colors = {
        "Live at scale": "#10B981",
        "Live, limited": "#22C55E",
        "Prototype": "#F59E0B",
        "Conceptual": "#FB7185",
        "Research": "#A78BFA",
    }

    fig, ax = plt.subplots(figsize=(14, 8), dpi=170)
    fig.patch.set_facecolor(BG)
    _style_dark(ax)

    y = np.arange(len(items))
    for i, (label, start, end, status) in enumerate(items):
        ax.barh(i, end - start, left=start, height=0.6, color=status_colors[status], edgecolor="white", linewidth=0.8)
        ax.text(end + 0.03, i, status, va="center", color=TEXT, fontsize=9)

    ax.axvline(2026.11, color="#F87171", linestyle=":", linewidth=1.5)
    ax.text(2026.11, -0.55, "Feb 2026", color="#FCA5A5", ha="center", fontsize=9)

    ax.set_yticks(y)
    ax.set_yticklabels([x[0] for x in items], color=TEXT, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlim(2025.2, 2028.3)
    ax.set_xticks([2025.5, 2026.0, 2026.5, 2027.0, 2027.5, 2028.0])
    ax.set_xticklabels(["H1'25", "H1'26", "H2'26", "H1'27", "H2'27", "H1'28"], color=TEXT)
    ax.set_title("Agent-to-Agent Commerce Readiness Roadmap", fontsize=20, fontweight="bold", color=TEXT, pad=16)
    ax.text(0.5, 1.02, "Simple transactions are production-ready; complex multi-agent commerce remains 12-24 months out",
            transform=ax.transAxes, ha="center", color=MUTED, fontsize=10)

    fig.text(0.5, 0.01, "Source: memos/fintech-agents-intersection.md (\"How Close to Reality?\" table).",
             ha="center", color=MUTED, fontsize=9, style="italic")
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    out = OUT_DIR / "04_agent_commerce_readiness_roadmap.png"
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    print("Generating intersection chart pack...")
    chart_protocol_launch_timeline()
    chart_protocol_capability_matrix()
    chart_layer_funding_heatmap()
    chart_agent_commerce_readiness_roadmap()
    print("Done.")
