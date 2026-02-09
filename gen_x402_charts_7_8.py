"""
Generate x402 Charts 7 & 8:
  Chart 7: Developer Adoption Funnel
  Chart 8: Buyer-to-Seller Ratio
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from x402_data import DEVELOPER_METRICS, USER_METRICS

# ---------------------------------------------------------------------------
# Chart 7: Developer Adoption Funnel
# ---------------------------------------------------------------------------

def chart_7():
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")

    # Funnel data (top = largest, bottom = smallest)
    labels = [
        "GitHub Stars",
        "GitHub Forks",
        "Hackathon Submissions",
        "Ecosystem Projects",
        "Live Services",
        "Facilitators",
        "npm Dependent Projects",
    ]
    values = [
        DEVELOPER_METRICS["github_stars"],           # 5400
        DEVELOPER_METRICS["github_forks"],           # 1000
        DEVELOPER_METRICS["hackathon_submissions_total"],  # 600
        DEVELOPER_METRICS["total_ecosystem_projects"],     # 117
        DEVELOPER_METRICS["live_services_endpoints"],      # 31
        DEVELOPER_METRICS["facilitator_count"],            # 19
        DEVELOPER_METRICS["npm_dependent_projects"],       # 19
    ]

    n = len(labels)
    y_pos = np.arange(n)

    # Color gradient: bright cyan at top -> muted teal at bottom
    colors = []
    for i in range(n):
        t = i / (n - 1)  # 0..1
        r = 0.0 + t * 0.18
        g = 0.90 - t * 0.45
        b = 0.95 - t * 0.30
        a = 1.0 - t * 0.25
        colors.append((r, g, b, a))

    bars = ax.barh(y_pos, values, color=colors, edgecolor="white", linewidth=0.4, height=0.65)

    # Value labels on each bar
    for i, (bar, val) in enumerate(zip(bars, values)):
        label_x = bar.get_width() + max(values) * 0.015
        ax.text(
            label_x, bar.get_y() + bar.get_height() / 2,
            f"{val:,}",
            va="center", ha="left",
            fontsize=14, fontweight="bold", color="white",
        )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=13, color="white")
    ax.invert_yaxis()  # largest at top

    ax.set_xlabel("Count", fontsize=12, color="#aaaacc")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.tick_params(axis="x", colors="#888899", labelsize=10)
    ax.grid(axis="x", color="#333355", linewidth=0.5, alpha=0.6)
    ax.set_axisbelow(True)

    # Remove top/right spines
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#555577")
    ax.spines["left"].set_color("#555577")

    # Title & subtitle
    fig.suptitle(
        "x402 Developer Adoption Funnel",
        fontsize=22, fontweight="bold", color="white",
        x=0.5, y=0.96,
    )
    ax.set_title(
        "Broad interest (5.4K stars) but narrow production usage (31 live services)",
        fontsize=13, color="#aaaacc", pad=14,
    )

    # Add a conversion annotation
    conversion = values[-1] / values[0] * 100
    ax.annotate(
        f"Top-to-bottom conversion: {conversion:.1f}%",
        xy=(0.98, 0.04), xycoords="axes fraction",
        ha="right", va="bottom",
        fontsize=11, color="#66ddaa",
        bbox=dict(boxstyle="round,pad=0.4", fc="#1a1a2e", ec="#66ddaa", lw=1),
    )

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig("charts/x402_07_developer_adoption.png", facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    print("Saved charts/x402_07_developer_adoption.png")


# ---------------------------------------------------------------------------
# Chart 8: Buyer-to-Seller Ratio
# ---------------------------------------------------------------------------

def chart_8():
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.set_aspect("equal")
    ax.axis("off")

    buyers = int(USER_METRICS.loc[USER_METRICS["date"] == "2025-10-26", "buyers"].values[0])
    sellers = int(USER_METRICS.loc[USER_METRICS["date"] == "2025-10-26", "sellers"].values[0])
    ratio = buyers / sellers  # ~52.7

    # Proportional circles: area proportional to count
    # buyer area / seller area = 74000 / 1405 ~ 52.7
    # radius ratio = sqrt(52.7) ~ 7.26
    max_radius = 3.2  # buyer circle radius
    seller_radius = max_radius / np.sqrt(ratio)

    buyer_color = "#3b82f6"
    seller_color = "#f59e0b"

    # Position circles
    buyer_cx, buyer_cy = 5.0, 4.2
    seller_cx, seller_cy = 12.2, 4.2

    # Draw buyer circle
    buyer_circle = plt.Circle(
        (buyer_cx, buyer_cy), max_radius,
        fc=buyer_color, ec="white", linewidth=1.5, alpha=0.85,
    )
    ax.add_patch(buyer_circle)

    # Draw seller circle
    seller_circle = plt.Circle(
        (seller_cx, seller_cy), seller_radius,
        fc=seller_color, ec="white", linewidth=1.5, alpha=0.85,
    )
    ax.add_patch(seller_circle)

    # Labels inside/near circles
    ax.text(buyer_cx, buyer_cy + 0.3, "BUYERS", ha="center", va="center",
            fontsize=18, fontweight="bold", color="white")
    ax.text(buyer_cx, buyer_cy - 0.4, f"{buyers:,}", ha="center", va="center",
            fontsize=28, fontweight="bold", color="white")

    ax.text(seller_cx, seller_cy + seller_radius + 0.55, "SELLERS", ha="center", va="center",
            fontsize=14, fontweight="bold", color=seller_color)
    ax.text(seller_cx, seller_cy + seller_radius + 1.1, f"{sellers:,}", ha="center", va="center",
            fontsize=18, fontweight="bold", color=seller_color)

    # Central ratio stat
    ratio_cx = (buyer_cx + max_radius + seller_cx - seller_radius) / 2
    ratio_cy = buyer_cy
    ax.text(ratio_cx, ratio_cy + 0.25, "53:1", ha="center", va="center",
            fontsize=52, fontweight="bold", color="white",
            bbox=dict(boxstyle="round,pad=0.3", fc="#1a1a2e", ec="#888899", lw=1.5))
    ax.text(ratio_cx, ratio_cy - 1.0, "buyer : seller", ha="center", va="center",
            fontsize=14, color="#aaaacc")

    # Annotation: sellers have pricing power
    ax.text(8.0, 0.7,
            "Sellers have extreme pricing power -- demand outstrips supply by 53x",
            ha="center", va="center", fontsize=13, color="#f59e0b", style="italic")

    # Title & subtitle
    fig.suptitle(
        "x402 Buyer-to-Seller Ratio: Sellers Have Pricing Power",
        fontsize=22, fontweight="bold", color="white",
        x=0.5, y=0.97,
    )
    fig.text(
        0.5, 0.915,
        "74,000 buyers competing for 1,405 sellers (Oct 26, 2025)",
        ha="center", fontsize=13, color="#aaaacc",
    )

    # Area proportionality note
    fig.text(
        0.5, 0.03,
        "Circle area proportional to count",
        ha="center", fontsize=10, color="#666688",
    )

    fig.savefig("charts/x402_08_buyer_seller_ratio.png", facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    print("Saved charts/x402_08_buyer_seller_ratio.png")


if __name__ == "__main__":
    chart_7()
    chart_8()
    print("Done: Charts 7 & 8 generated.")
