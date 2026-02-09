"""
Generate x402 Charts 5 & 6:
  - Chart 5: Value Chain Waterfall (horizontal bar)
  - Chart 6: Ecosystem Token Market Cap (line + area fill)
"""

import sys
sys.path.insert(0, "/Users/cat/memo-fintech-agents")

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from x402_data import VALUE_CHAIN, ECOSYSTEM_MCAP

# ---------------------------------------------------------------------------
# Chart 5: Value Chain Waterfall
# ---------------------------------------------------------------------------

plt.style.use("dark_background")

fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
fig.patch.set_facecolor("#1a1a2e")
ax.set_facecolor("#1a1a2e")

# Select the rows to plot and their order (top to bottom = highest to lowest value)
layers = [
    "Application (seller)",
    "Facilitator",
    "Chain sequencer (Base)",
    "Chain validator (Solana)",
    "RPC provider",
    "Protocol (x402)",
    "USDC issuer (Circle)",
]

# Build ordered data
df = VALUE_CHAIN.set_index("layer").loc[layers].reset_index()
amounts = df["amount_per_001"].values
pcts = df["pct_of_payment"].values
labels = df["layer"].values

# Reverse so highest value is at top when plotted
labels = labels[::-1]
amounts = amounts[::-1]
pcts = pcts[::-1]

# Green gradient: darker = more value capture
green_light = np.array([0.0, 0.83, 0.67, 1.0])   # #00d4aa
green_dark = np.array([0.0, 0.30, 0.24, 1.0])     # #004d3d
neutral = np.array([0.25, 0.30, 0.35, 1.0])        # for zero-value layers

max_pct = max(pcts) if max(pcts) > 0 else 1
colors = []
for p in pcts:
    if p == 0:
        colors.append(tuple(neutral))
    else:
        t = (p / max_pct) ** 0.5  # sqrt scaling for better visual spread
        c = green_light * (1 - t) + green_dark * t
        colors.append(tuple(c))

y_pos = np.arange(len(labels))
bars = ax.barh(y_pos, amounts, color=colors, edgecolor="white", linewidth=0.3, height=0.6)

# Labels on each bar
for i, (bar, amt, pct) in enumerate(zip(bars, amounts, pcts)):
    w = bar.get_width()
    if amt > 0:
        label_text = f"${amt:.4f}  ({pct:.1f}%)"
        if pct >= 10:
            label_text = f"${amt:.4f}  ({pct:.0f}%)"
        # Place label inside bar if wide enough, else outside
        if pct >= 50:
            ax.text(w - 0.0002, bar.get_y() + bar.get_height() / 2,
                    label_text, va="center", ha="right", fontsize=12,
                    fontweight="bold", color="white")
        elif pct >= 5:
            ax.text(w + 0.0001, bar.get_y() + bar.get_height() / 2,
                    label_text, va="center", ha="left", fontsize=11,
                    color="white")
        else:
            ax.text(w + 0.0001, bar.get_y() + bar.get_height() / 2,
                    label_text, va="center", ha="left", fontsize=11,
                    color="white")
    else:
        ax.text(0.0001, bar.get_y() + bar.get_height() / 2,
                f"$0.0000  (0%)", va="center", ha="left", fontsize=11,
                color="#888888")

ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=12, color="white")
ax.set_xlabel("Value Captured per $0.01 Payment (USD)", fontsize=12, color="white")
ax.set_xlim(0, max(amounts) * 1.25)

# Grid
ax.xaxis.grid(True, color="#333355", linestyle="--", linewidth=0.5, alpha=0.5)
ax.yaxis.grid(False)
ax.set_axisbelow(True)

# Title and subtitle
ax.set_title("Value Capture in a $0.01 x402 Payment",
             fontsize=20, fontweight="bold", color="white", pad=20)
fig.text(0.5, 0.91,
         "The application layer captures 88% \u2014 infrastructure is a cost center",
         ha="center", fontsize=13, color="#aaaaaa", style="italic")

ax.tick_params(axis="x", colors="white", labelsize=10)
ax.tick_params(axis="y", colors="white")
for spine in ax.spines.values():
    spine.set_color("#333355")

plt.tight_layout(rect=[0, 0, 1, 0.90])
fig.savefig("/Users/cat/memo-fintech-agents/charts/x402_05_value_chain.png",
            facecolor=fig.get_facecolor(), bbox_inches="tight")
plt.close(fig)
print("Saved charts/x402_05_value_chain.png")


# ---------------------------------------------------------------------------
# Chart 6: Ecosystem Token Market Cap
# ---------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
fig.patch.set_facecolor("#1a1a2e")
ax.set_facecolor("#1a1a2e")

dates = ECOSYSTEM_MCAP["date"]
mcap = ECOSYSTEM_MCAP["mcap_usd"] / 1e9  # in billions

# Plot line
ax.plot(dates, mcap, color="#7c3aed", linewidth=3, zorder=5)

# Gradient area fill using imshow
# Create a mesh for the gradient
x_num = mdates.date2num(dates)
x_fine = np.linspace(x_num.min(), x_num.max(), 500)
mcap_fine = np.interp(x_fine, x_num, mcap)

# Fill with gradient using multiple fills at different alpha levels
n_layers = 40
for i in range(n_layers):
    frac_bottom = i / n_layers
    frac_top = (i + 1) / n_layers
    alpha = 0.02 + 0.4 * (frac_top)  # increasing alpha toward top
    y_bottom = mcap_fine * frac_bottom
    y_top = mcap_fine * frac_top
    ax.fill_between(mdates.num2date(x_fine), y_bottom, y_top,
                     color="#7c3aed", alpha=alpha, linewidth=0)

# Annotate key moments
# Peak: ~$12B
peak_date = dates.iloc[2]
peak_val = mcap.iloc[2]
ax.annotate("Memecoin mania:\n1300% in 2 weeks",
            xy=(peak_date, peak_val),
            xytext=(peak_date + np.timedelta64(-20, "D"), peak_val + 1.0),
            fontsize=12, fontweight="bold", color="#ff6b6b",
            arrowprops=dict(arrowstyle="->", color="#ff6b6b", lw=1.5),
            ha="center")

# Correction dip: ~$5B
dip_date = dates.iloc[3]
dip_val = mcap.iloc[3]
ax.annotate("Correction",
            xy=(dip_date, dip_val),
            xytext=(dip_date + np.timedelta64(10, "D"), dip_val - 1.5),
            fontsize=12, fontweight="bold", color="#ffa94d",
            arrowprops=dict(arrowstyle="->", color="#ffa94d", lw=1.5),
            ha="center")

# Recovery: $10.5B
end_date = dates.iloc[4]
end_val = mcap.iloc[4]
ax.annotate("Recovery: $10.5B",
            xy=(end_date, end_val),
            xytext=(end_date + np.timedelta64(-5, "D"), end_val + 1.5),
            fontsize=12, fontweight="bold", color="#51cf66",
            arrowprops=dict(arrowstyle="->", color="#51cf66", lw=1.5),
            ha="center")

# Scatter points at data points
ax.scatter(dates, mcap, color="white", s=60, zorder=6, edgecolor="#7c3aed", linewidth=2)

# Y axis formatting
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}B"))
ax.set_ylim(bottom=0, top=max(mcap) * 1.3)

# X axis
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.xaxis.set_major_locator(mdates.MonthLocator())
plt.xticks(rotation=30, ha="right")

# Grid
ax.yaxis.grid(True, color="#333355", linestyle="--", linewidth=0.5, alpha=0.5)
ax.xaxis.grid(True, color="#333355", linestyle="--", linewidth=0.5, alpha=0.3)
ax.set_axisbelow(True)

# Title and subtitle
ax.set_title("x402 Ecosystem Token Market Cap",
             fontsize=20, fontweight="bold", color="white", pad=20)
fig.text(0.5, 0.91,
         "Driven primarily by speculative memecoins, not protocol revenue",
         ha="center", fontsize=13, color="#aaaaaa", style="italic")

ax.tick_params(axis="both", colors="white", labelsize=11)
for spine in ax.spines.values():
    spine.set_color("#333355")

plt.tight_layout(rect=[0, 0, 1, 0.90])
fig.savefig("/Users/cat/memo-fintech-agents/charts/x402_06_ecosystem_mcap.png",
            facecolor=fig.get_facecolor(), bbox_inches="tight")
plt.close(fig)
print("Saved charts/x402_06_ecosystem_mcap.png")
