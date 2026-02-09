"""
Generate additional x402 strategy charts focused on sensitivity and risk.

Charts:
  1) x402_12_layer_revenue_sensitivity.png
  2) x402_13_coinbase_revenue_scenarios.png
  3) x402_14_risk_matrix.png

Data source:
  - x402-value-accrual-deep-dive.md
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "charts" / "x402"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BG = "#1a1a2e"
CARD = "#16213e"
GRID = "#2a2a4a"
TEXT = "#e0e0e0"


def _style_dark(ax: plt.Axes) -> None:
    ax.set_facecolor(CARD)
    ax.grid(True, color=GRID, linestyle="--", alpha=0.35, linewidth=0.8)
    ax.tick_params(colors=TEXT)
    for spine in ax.spines.values():
        spine.set_color(GRID)


def chart_layer_revenue_sensitivity() -> None:
    """Layer revenue sensitivity as annual x402 volume scales."""
    # Per-$1B annual volume figures from x402-value-accrual-deep-dive.md.
    per_billion = {
        "Currency (USDC)": 45.0,
        "Settlement (Base)": 10.0,
        "Application": 880.0,
        "Facilitator": 100.0,
        "Infrastructure": 1.0,
    }
    discovery_low = 20.0
    discovery_high = 80.0

    volumes = np.array([0.5, 1, 2, 5, 10], dtype=float)  # USD billions

    fig, ax = plt.subplots(figsize=(14, 8), dpi=170)
    fig.patch.set_facecolor(BG)
    _style_dark(ax)

    colors = {
        "Application": "#22D3EE",
        "Facilitator": "#F59E0B",
        "Currency (USDC)": "#34D399",
        "Settlement (Base)": "#60A5FA",
        "Infrastructure": "#A78BFA",
    }

    for layer, per_b in per_billion.items():
        ax.plot(volumes, per_b * volumes, marker="o", linewidth=2.6,
                color=colors[layer], label=layer)

    ax.fill_between(
        volumes,
        discovery_low * volumes,
        discovery_high * volumes,
        color="#FBBF24",
        alpha=0.22,
        label="Discovery range (2-8% take)",
    )
    ax.plot(volumes, ((discovery_low + discovery_high) / 2) * volumes,
            color="#FBBF24", linestyle="--", linewidth=2)

    ax.set_title("x402 Layer Revenue Sensitivity by Annual Volume", fontsize=20, fontweight="bold", color=TEXT, pad=16)
    ax.text(0.5, 1.02, "Revenues shown in USD millions per year; discovery shown as low-high assumption band",
            transform=ax.transAxes, ha="center", color="#94a3b8", fontsize=10)
    ax.set_xlabel("Annual x402 Volume (USD Billions)", fontsize=12, color=TEXT)
    ax.set_ylabel("Annual Revenue (USD Millions)", fontsize=12, color=TEXT)
    ax.set_xlim(0.4, 10.2)
    ax.set_ylim(0, 9300)
    ax.set_xticks(volumes)
    ax.legend(loc="upper left", framealpha=0.25, facecolor=BG, edgecolor=GRID, labelcolor=TEXT)

    ax.annotate("At $10B volume:\nApplication ~$8.8B\nFacilitator ~$1.0B",
                xy=(10, 8800), xytext=(6.5, 7800),
                arrowprops=dict(arrowstyle="->", color="#22D3EE", lw=1.3),
                color=TEXT, fontsize=10,
                bbox=dict(boxstyle="round,pad=0.4", facecolor=BG, edgecolor="#22D3EE", alpha=0.55))

    fig.text(0.5, 0.01, "Source: x402-value-accrual-deep-dive.md ($1B scenario table).",
             ha="center", fontsize=9, color="#94a3b8", style="italic")
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    out = OUT_DIR / "x402_12_layer_revenue_sensitivity.png"
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"Saved: {out}")


def chart_coinbase_revenue_scenarios() -> None:
    """Coinbase direct x402-linked revenue by volume scenario."""
    volumes = np.array([1, 5, 10], dtype=float)  # USD billions

    # Per-$1B assumptions from memo.
    usdc_share = 25.0
    base_fees = 7.5
    facilitator_fees = 1.0
    commerce_low = 2.0
    commerce_high = 5.0
    commerce_mid = (commerce_low + commerce_high) / 2

    usdc_vals = usdc_share * volumes
    base_vals = base_fees * volumes
    fac_vals = facilitator_fees * volumes
    comm_mid_vals = commerce_mid * volumes
    total_low = (usdc_share + base_fees + facilitator_fees + commerce_low) * volumes
    total_high = (usdc_share + base_fees + facilitator_fees + commerce_high) * volumes
    total_mid = usdc_vals + base_vals + fac_vals + comm_mid_vals

    fig, ax = plt.subplots(figsize=(13, 8), dpi=170)
    fig.patch.set_facecolor(BG)
    _style_dark(ax)

    x = np.arange(len(volumes))
    width = 0.6

    ax.bar(x, usdc_vals, width=width, color="#34D399", label="USDC reserve income share")
    ax.bar(x, base_vals, width=width, bottom=usdc_vals, color="#60A5FA", label="Base sequencer fees")
    ax.bar(x, fac_vals, width=width, bottom=usdc_vals + base_vals, color="#F59E0B", label="Facilitator fees")
    ax.bar(x, comm_mid_vals, width=width, bottom=usdc_vals + base_vals + fac_vals,
           color="#A78BFA", label="Commerce (midpoint)")

    # Add whisker for commerce uncertainty.
    yerr = (total_high - total_low) / 2
    ax.errorbar(x, total_mid, yerr=yerr, fmt="none", ecolor="#FBBF24", elinewidth=2, capsize=6, capthick=2)

    for i in range(len(x)):
        ax.text(x[i], total_high[i] + 8, f"${total_low[i]:.0f}M-${total_high[i]:.0f}M",
                ha="center", fontsize=10, color=TEXT, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels([f"${int(v)}B volume" for v in volumes], color=TEXT)
    ax.set_ylabel("Annual Coinbase Revenue (USD Millions)", color=TEXT, fontsize=12)
    ax.set_title("Coinbase x402 Revenue Scenarios (Direct Capture Only)", fontsize=20, fontweight="bold", color=TEXT, pad=16)
    ax.text(0.5, 1.02, "Error bars represent commerce contribution range ($2M-$5M per $1B volume)",
            transform=ax.transAxes, ha="center", color="#94a3b8", fontsize=10)
    ax.legend(loc="upper left", framealpha=0.25, facecolor=BG, edgecolor=GRID, labelcolor=TEXT)
    ax.set_ylim(0, 420)

    fig.text(0.5, 0.01, "Source: x402-value-accrual-deep-dive.md (Coinbase attribution table).",
             ha="center", fontsize=9, color="#94a3b8", style="italic")
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    out = OUT_DIR / "x402_13_coinbase_revenue_scenarios.png"
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"Saved: {out}")


def chart_risk_matrix() -> None:
    """Impact-probability matrix for the x402 value accrual thesis."""
    risks = [
        ("USDC rate sensitivity", 3.0, 4.0),
        ("Chain migration", 4.0, 4.0),
        ("Protocol competition", 3.0, 3.0),
        ("Regulatory crackdown", 3.5, 4.0),
        ("Volume reality check", 4.0, 4.0),
        ("Facilitator centralization", 3.0, 3.0),
    ]

    # Small offsets so overlapping points remain readable.
    offsets = {
        "Chain migration": (-0.12, 0.08),
        "Volume reality check": (0.12, -0.10),
        "Protocol competition": (-0.10, 0.10),
        "Facilitator centralization": (0.10, -0.10),
    }

    fig, ax = plt.subplots(figsize=(11, 9), dpi=170)
    fig.patch.set_facecolor(BG)
    _style_dark(ax)

    # Background risk gradient.
    grid_x, grid_y = np.meshgrid(np.linspace(1, 4, 120), np.linspace(1, 4, 120))
    z = (grid_x * grid_y) / 16.0
    ax.contourf(grid_x, grid_y, z, levels=12, cmap="magma", alpha=0.5)

    for name, prob, impact in risks:
        dx, dy = offsets.get(name, (0.0, 0.0))
        px = prob + dx
        py = impact + dy
        severity = prob * impact
        color = "#F87171" if severity >= 14 else "#FBBF24" if severity >= 10 else "#34D399"
        ax.scatter(px, py, s=160, color=color, edgecolor="white", linewidth=1.2, zorder=5)
        ax.text(px + 0.03, py + 0.03, name, color=TEXT, fontsize=9, ha="left", va="bottom")

    ax.set_xlim(1, 4.2)
    ax.set_ylim(1, 4.2)
    ax.set_xticks([1, 2, 3, 4])
    ax.set_yticks([1, 2, 3, 4])
    ax.set_xticklabels(["Low", "Medium", "Medium-High", "High"], color=TEXT)
    ax.set_yticklabels(["Low", "Medium", "Medium-High", "High"], color=TEXT)
    ax.set_xlabel("Probability", color=TEXT, fontsize=12)
    ax.set_ylabel("Impact", color=TEXT, fontsize=12)
    ax.set_title("x402 Value Accrual Risk Matrix", fontsize=20, fontweight="bold", color=TEXT, pad=16)
    ax.text(0.5, 1.02, "High-probability, high-impact cluster: chain share shifts and volume quality risk",
            transform=ax.transAxes, ha="center", color="#94a3b8", fontsize=10)

    fig.text(0.5, 0.01, "Source: x402-value-accrual-deep-dive.md (Risk Factors table). Probability/impact bins mapped for visualization.",
             ha="center", fontsize=8.5, color="#94a3b8", style="italic")
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    out = OUT_DIR / "x402_14_risk_matrix.png"
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    print("Generating additional x402 sensitivity/risk charts...")
    chart_layer_revenue_sensitivity()
    chart_coinbase_revenue_scenarios()
    chart_risk_matrix()
    print("Done.")
