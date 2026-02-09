"""
x402 Value Accrual Visualizations
1. Buyer-to-Seller Ratio Over Time (with projection)
2. Full Market Stack Value Accrual Diagram
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
from datetime import datetime

# =============================================================================
# STYLING
# =============================================================================
BG_COLOR = '#1a1a2e'
CARD_COLOR = '#16213e'
GRID_COLOR = '#2a2a4a'
TEXT_COLOR = '#e0e0e0'
CYAN = '#00d4ff'
PURPLE = '#b44aff'
AMBER = '#ffb347'
GREEN = '#4ecdc4'
RED = '#ff6b6b'
PINK = '#ff69b4'
LIGHT_BLUE = '#87ceeb'
DARK_CYAN = '#008b8b'

plt.rcParams.update({
    'figure.facecolor': BG_COLOR,
    'axes.facecolor': CARD_COLOR,
    'axes.edgecolor': GRID_COLOR,
    'axes.labelcolor': TEXT_COLOR,
    'text.color': TEXT_COLOR,
    'xtick.color': TEXT_COLOR,
    'ytick.color': TEXT_COLOR,
    'grid.color': GRID_COLOR,
    'grid.alpha': 0.3,
    'font.family': 'sans-serif',
})


# =============================================================================
# CHART 1: BUYER-TO-SELLER RATIO OVER TIME
# =============================================================================
def chart_buyer_seller_ratio():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 14), height_ratios=[3, 2])
    fig.subplots_adjust(hspace=0.35)

    # --- Data ---
    # Historical data points
    dates_hist = [
        datetime(2025, 5, 6),   # Launch
        datetime(2025, 7, 1),   # Early
        datetime(2025, 9, 1),   # Pre-foundation
        datetime(2025, 10, 23), # First Dune snapshot
        datetime(2025, 10, 26), # Spike (70K buyers in 3 days)
        datetime(2025, 11, 15), # Post-peak
        datetime(2025, 12, 15), # V2 era
        datetime(2026, 1, 15),  # Recent
    ]
    buyers_hist =  [50,    500,   2000,  4000,   74000,   120000,  250000,  406700]
    sellers_hist = [10,    80,    400,   1078,   1405,    8000,    40000,   81000]
    ratios_hist =  [5.0,   6.25,  5.0,   3.71,   52.67,   15.0,    6.25,    5.02]

    # Projected data points
    dates_proj = [
        datetime(2026, 6, 1),
        datetime(2026, 12, 1),
        datetime(2027, 6, 1),
        datetime(2027, 12, 1),
    ]
    buyers_proj =  [800000,   1500000,  3000000,  5000000]
    sellers_proj = [200000,   500000,   1200000,  2000000]
    ratios_proj =  [4.0,      3.0,      2.5,      2.5]

    # --- Top panel: Absolute counts (log scale) ---
    ax1.set_yscale('log')

    # Historical
    ax1.plot(dates_hist, buyers_hist, color=CYAN, linewidth=2.5, marker='o',
             markersize=8, zorder=5, label='Buyers (historical)')
    ax1.plot(dates_hist, sellers_hist, color=RED, linewidth=2.5, marker='s',
             markersize=8, zorder=5, label='Sellers (historical)')

    # Projected
    all_buyer_dates = dates_hist + dates_proj
    all_buyer_vals = buyers_hist + buyers_proj
    all_seller_dates = dates_hist + dates_proj
    all_seller_vals = sellers_hist + sellers_proj

    ax1.plot(dates_proj, buyers_proj, color=CYAN, linewidth=2, linestyle='--',
             marker='o', markersize=6, alpha=0.5, zorder=4)
    ax1.plot(dates_proj, sellers_proj, color=RED, linewidth=2, linestyle='--',
             marker='s', markersize=6, alpha=0.5, zorder=4)

    # Connect historical to projected
    ax1.plot([dates_hist[-1], dates_proj[0]], [buyers_hist[-1], buyers_proj[0]],
             color=CYAN, linewidth=2, linestyle='--', alpha=0.5)
    ax1.plot([dates_hist[-1], dates_proj[0]], [sellers_hist[-1], sellers_proj[0]],
             color=RED, linewidth=2, linestyle='--', alpha=0.5)

    # Fill between
    ax1.fill_between(dates_hist, buyers_hist, sellers_hist, alpha=0.08, color=CYAN)

    # Annotate the spike
    ax1.annotate('70K buyers added\nin 3 days\n(ratio hits 53:1)',
                 xy=(datetime(2025, 10, 26), 74000),
                 xytext=(datetime(2025, 8, 15), 200000),
                 fontsize=10, color=AMBER, fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color=AMBER, lw=1.5),
                 ha='center')

    # Annotate current
    ax1.annotate(f'Today: 407K buyers\n81K sellers (5:1)',
                 xy=(datetime(2026, 1, 15), 406700),
                 xytext=(datetime(2025, 12, 1), 1500000),
                 fontsize=10, color=GREEN, fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5),
                 ha='center')

    # Projection zone
    ax1.axvspan(datetime(2026, 2, 1), datetime(2028, 1, 1), alpha=0.05, color=PURPLE)
    ax1.text(datetime(2026, 9, 1), 30, 'PROJECTED', fontsize=11, color=PURPLE,
             alpha=0.6, ha='center', fontstyle='italic')

    ax1.set_ylabel('Unique Addresses (log scale)', fontsize=12, fontweight='bold')
    ax1.set_title('x402 Protocol: Buyer vs. Seller Growth Over Time',
                  fontsize=16, fontweight='bold', pad=15)
    ax1.legend(loc='upper left', fontsize=10, framealpha=0.3)
    ax1.grid(True, alpha=0.2)
    ax1.set_xlim(datetime(2025, 4, 1), datetime(2028, 1, 1))

    # --- Bottom panel: Ratio over time ---
    all_dates = dates_hist + dates_proj
    all_ratios = ratios_hist + ratios_proj

    # Historical bars
    bar_width = 25  # days
    colors_hist = []
    for r in ratios_hist:
        if r > 20:
            colors_hist.append(RED)
        elif r > 8:
            colors_hist.append(AMBER)
        elif r > 4:
            colors_hist.append(CYAN)
        else:
            colors_hist.append(GREEN)

    ax2.bar(dates_hist, ratios_hist, width=bar_width, color=colors_hist,
            alpha=0.8, edgecolor='white', linewidth=0.5, zorder=3)

    # Projected bars
    colors_proj = [GREEN] * len(ratios_proj)
    ax2.bar(dates_proj, ratios_proj, width=bar_width, color=colors_proj,
            alpha=0.35, edgecolor='white', linewidth=0.5, linestyle='--', zorder=3)

    # Reference lines
    ax2.axhline(y=5, color=CYAN, linestyle=':', alpha=0.5, linewidth=1)
    ax2.text(datetime(2027, 10, 1), 5.5, 'Uber-like (5:1)', fontsize=9,
             color=CYAN, alpha=0.7, ha='center')
    ax2.axhline(y=1.3, color=GREEN, linestyle=':', alpha=0.5, linewidth=1)
    ax2.text(datetime(2027, 10, 1), 1.8, 'Amazon-like (1.3:1)', fontsize=9,
             color=GREEN, alpha=0.7, ha='center')

    # Label the spike
    ax2.annotate('53:1', xy=(datetime(2025, 10, 26), 52.67),
                 xytext=(datetime(2025, 10, 26), 55),
                 fontsize=14, fontweight='bold', color=RED, ha='center')

    # Label key ratios
    for i, (d, r) in enumerate(zip(dates_hist, ratios_hist)):
        if r < 50:
            ax2.text(d, r + 1.5, f'{r:.1f}:1', fontsize=8, ha='center',
                     color=TEXT_COLOR, fontweight='bold')

    for d, r in zip(dates_proj, ratios_proj):
        ax2.text(d, r + 1.5, f'{r:.1f}:1', fontsize=8, ha='center',
                 color=PURPLE, alpha=0.7, fontweight='bold')

    ax2.set_ylabel('Buyer-to-Seller Ratio', fontsize=12, fontweight='bold')
    ax2.set_xlabel('', fontsize=12)
    ax2.set_title('Buyer-to-Seller Ratio: Compression from 53:1 → 5:1 → ~2.5:1 (projected)',
                  fontsize=13, fontweight='bold', pad=10)
    ax2.grid(True, alpha=0.2)
    ax2.set_xlim(datetime(2025, 4, 1), datetime(2028, 1, 1))
    ax2.set_ylim(0, 60)

    # Insight box
    insight_text = (
        "SELLER PRICING POWER\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "• At 5:1, sellers set prices unilaterally (no price discovery)\n"
        "• Avg payment $0.60-$1.00 vs. gas floor of $0.001 → massive margin\n"
        "• No chargebacks = zero seller revenue risk\n"
        "• Compression trend: pricing power erodes as sellers enter\n"
        "• Commodity APIs → race to zero; proprietary data → durable power"
    )
    fig.text(0.5, 0.01, insight_text, fontsize=10, color=TEXT_COLOR, ha='center',
             va='bottom', fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.8', facecolor=BG_COLOR,
                       edgecolor=AMBER, alpha=0.9, linewidth=1.5))

    fig.savefig('/Users/cat/memo-fintech-agents/charts/x402_09_buyer_seller_ratio_deep.png',
                dpi=150, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close()
    print("✓ Chart 1: Buyer-Seller Ratio Over Time saved")


# =============================================================================
# CHART 2: FULL MARKET STACK — VALUE ACCRUAL DIAGRAM
# =============================================================================
def chart_value_stack():
    fig, ax = plt.subplots(figsize=(20, 16))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(50, 98, 'x402 Market Stack: Where Value Accrues',
            fontsize=22, fontweight='bold', ha='center', va='top', color=TEXT_COLOR)
    ax.text(50, 95.5, 'Full back-to-back view of every layer in an x402 transaction  |  Per $1B annual volume scenario',
            fontsize=12, ha='center', va='top', color=LIGHT_BLUE, alpha=0.7)

    # --- Stack layers (bottom to top) ---
    layers = [
        {
            'name': 'INFRASTRUCTURE',
            'subtitle': 'RPC Providers  •  Wallets  •  Key Management',
            'players': 'QuickNode  •  Alchemy  •  Coinbase Wallet  •  thirdweb  •  Dynamic',
            'rev_pct': '0.1%',
            'rev_1b': '$1M',
            'margin': '60-70%',
            'moat': 2,
            'moat_label': 'Low',
            'color': '#4a4a6a',
            'accrual': 'Commoditizing. Multiple substitutes.\nRace to bottom on pricing.',
            'verdict': 'AVOID',
            'verdict_color': RED,
        },
        {
            'name': 'CURRENCY LAYER',
            'subtitle': 'USDC (98.7% of x402 volume)',
            'players': 'Circle (issuer)  •  Coinbase (56% of reserve revenue)',
            'rev_pct': '0% per tx',
            'rev_1b': '$45M',
            'margin': '~95%',
            'moat': 5,
            'moat_label': 'Very High',
            'color': '#1a5276',
            'accrual': 'Earns 4.5% on ENTIRE float, not per-tx.\n$1B in agent wallets = $45M/yr. Scale = destiny.',
            'verdict': 'BUY',
            'verdict_color': GREEN,
        },
        {
            'name': 'SETTLEMENT LAYER',
            'subtitle': 'On-chain finality  •  Gas/Sequencer fees',
            'players': 'Base (75.5%)  •  Solana (24.5%)  •  Ethereum  •  Polygon  •  Arbitrum',
            'rev_pct': '~1%',
            'rev_1b': '$10M',
            'margin': '>90%',
            'moat': 4,
            'moat_label': 'High',
            'color': '#1a4a3a',
            'accrual': 'Earns on EVERY transaction. Cannot be\ndisintermediated without chain migration.',
            'verdict': 'BUY',
            'verdict_color': GREEN,
        },
        {
            'name': 'PROTOCOL LAYER',
            'subtitle': 'x402 open standard  (Apache 2.0)',
            'players': 'x402 Foundation (Coinbase + Cloudflare)',
            'rev_pct': '0%',
            'rev_1b': '$0',
            'margin': 'N/A',
            'moat': 4,
            'moat_label': 'High (standard)',
            'color': '#3a1a5e',
            'accrual': 'Zero direct revenue. Value captured at\nadjacent layers. The "Android strategy."',
            'verdict': 'N/A',
            'verdict_color': LIGHT_BLUE,
        },
        {
            'name': 'FACILITATOR LAYER',
            'subtitle': 'Payment verification  •  On-chain settlement',
            'players': 'Dexter (50%)  •  Coinbase CDP (25%)  •  PayAI (13%)  •  DayDreams (7%)',
            'rev_pct': '~10%',
            'rev_1b': '$100M',
            'margin': '50-75%',
            'moat': 1,
            'moat_label': 'Very Low',
            'color': '#5a3a1a',
            'accrual': 'VALUE TRAP. Dexter went 5%→50% in 3 months.\nZero switching costs. Fees race to zero.',
            'verdict': 'AVOID',
            'verdict_color': RED,
        },
        {
            'name': 'DISCOVERY LAYER',
            'subtitle': 'Agent service discovery  •  Price comparison  •  Routing',
            'players': 'Fluora (MonetizedMCP)  •  x402 V2 API Discovery  •  ??? (whitespace)',
            'rev_pct': 'TBD',
            'rev_1b': 'TBD',
            'margin': 'TBD',
            'moat': 4,
            'moat_label': 'High (if won)',
            'color': '#1a3a5e',
            'accrual': 'BIGGEST WHITESPACE. Whoever builds the\n"Google for agent APIs" owns the chokepoint.',
            'verdict': 'WATCH',
            'verdict_color': AMBER,
        },
        {
            'name': 'APPLICATION LAYER',
            'subtitle': 'Sellers: APIs, data, compute, content',
            'players': 'Firecrawl  •  DappLooker  •  Daydreams  •  Pinata  •  Apify  •  thousands more',
            'rev_pct': '88%',
            'rev_1b': '$880M',
            'margin': '70-90%',
            'moat': 3,
            'moat_label': 'Medium (varies)',
            'color': '#1a4a5e',
            'accrual': 'Highest absolute $. But fragmented across\nthousands. Commodity APIs → margin compression.',
            'verdict': 'SELECTIVE',
            'verdict_color': AMBER,
        },
        {
            'name': 'AGENT ORCHESTRATION',
            'subtitle': 'Who decides which API to call?',
            'players': 'OpenAI  •  Anthropic  •  Google  •  open-source agents',
            'rev_pct': '$0 from x402',
            'rev_1b': '$0 (direct)',
            'margin': 'N/A',
            'moat': 5,
            'moat_label': 'Very High',
            'color': '#3a2a5e',
            'accrual': 'Controls INTENT. Monetized via model subs,\nnot x402 fees. Highest strategic leverage.',
            'verdict': 'OWN',
            'verdict_color': CYAN,
        },
    ]

    n = len(layers)
    layer_height = 8.5
    gap = 1.2
    start_y = 4
    stack_left = 2
    stack_width = 57

    # Revenue bar area
    rev_left = 62
    rev_width = 14

    # Moat bar area
    moat_left = 79
    moat_width = 8

    # Verdict area
    verdict_left = 90

    # Headers
    header_y = start_y + n * (layer_height + gap) + 1
    ax.text(stack_left + stack_width / 2, header_y, 'LAYER', fontsize=11,
            fontweight='bold', ha='center', color=LIGHT_BLUE)
    ax.text(rev_left + rev_width / 2, header_y, 'REVENUE\n(per $1B vol)',
            fontsize=10, fontweight='bold', ha='center', color=LIGHT_BLUE)
    ax.text(moat_left + moat_width / 2, header_y, 'MOAT', fontsize=10,
            fontweight='bold', ha='center', color=LIGHT_BLUE)
    ax.text(verdict_left + 5, header_y, 'VERDICT', fontsize=10,
            fontweight='bold', ha='center', color=LIGHT_BLUE)

    # Draw each layer
    for i, layer in enumerate(layers):
        y = start_y + i * (layer_height + gap)

        # Main layer box
        rect = FancyBboxPatch((stack_left, y), stack_width, layer_height,
                              boxstyle='round,pad=0.3',
                              facecolor=layer['color'], edgecolor='white',
                              linewidth=0.8, alpha=0.85)
        ax.add_patch(rect)

        # Layer name
        ax.text(stack_left + 1.5, y + layer_height - 1.5, layer['name'],
                fontsize=13, fontweight='bold', color='white', va='top')
        # Subtitle
        ax.text(stack_left + 1.5, y + layer_height - 3.5, layer['subtitle'],
                fontsize=9, color=LIGHT_BLUE, alpha=0.8, va='top')
        # Players
        ax.text(stack_left + 1.5, y + layer_height - 5, layer['players'],
                fontsize=8.5, color=TEXT_COLOR, alpha=0.65, va='top')
        # Accrual insight
        ax.text(stack_left + 1.5, y + 0.8, layer['accrual'],
                fontsize=8.5, color=AMBER, va='bottom', fontstyle='italic')

        # Revenue box
        rev_rect = FancyBboxPatch((rev_left, y + 0.5), rev_width, layer_height - 1,
                                  boxstyle='round,pad=0.3',
                                  facecolor=BG_COLOR, edgecolor=GRID_COLOR,
                                  linewidth=0.5, alpha=0.9)
        ax.add_patch(rev_rect)
        ax.text(rev_left + rev_width / 2, y + layer_height / 2 + 1.5,
                layer['rev_pct'], fontsize=11, fontweight='bold',
                ha='center', va='center', color=TEXT_COLOR)
        ax.text(rev_left + rev_width / 2, y + layer_height / 2 - 1,
                layer['rev_1b'], fontsize=14, fontweight='bold',
                ha='center', va='center', color=CYAN)

        # Moat bar
        moat_bar_y = y + 2
        moat_bar_h = layer_height - 4
        max_moat = 5
        filled_w = (layer['moat'] / max_moat) * moat_width

        # Background
        bg_rect = FancyBboxPatch((moat_left, moat_bar_y), moat_width, moat_bar_h,
                                 boxstyle='round,pad=0.1',
                                 facecolor=GRID_COLOR, edgecolor='none', alpha=0.4)
        ax.add_patch(bg_rect)

        # Filled portion
        moat_color = GREEN if layer['moat'] >= 4 else AMBER if layer['moat'] >= 3 else RED
        if filled_w > 0:
            fill_rect = FancyBboxPatch((moat_left, moat_bar_y), filled_w, moat_bar_h,
                                       boxstyle='round,pad=0.1',
                                       facecolor=moat_color, edgecolor='none', alpha=0.7)
            ax.add_patch(fill_rect)

        ax.text(moat_left + moat_width / 2, moat_bar_y + moat_bar_h + 1.2,
                layer['moat_label'], fontsize=8, ha='center', color=moat_color,
                fontweight='bold')

        # Verdict
        ax.text(verdict_left + 5, y + layer_height / 2,
                layer['verdict'], fontsize=13, fontweight='bold',
                ha='center', va='center', color=layer['verdict_color'],
                bbox=dict(boxstyle='round,pad=0.4', facecolor=BG_COLOR,
                          edgecolor=layer['verdict_color'], linewidth=1.5, alpha=0.9))

    # Money flow arrow on the left
    arrow_x = 0.8
    arrow_bottom = start_y + 2
    arrow_top = start_y + n * (layer_height + gap) - 2
    ax.annotate('', xy=(arrow_x, arrow_top), xytext=(arrow_x, arrow_bottom),
                arrowprops=dict(arrowstyle='->', color=AMBER, lw=2.5))
    ax.text(arrow_x, (arrow_bottom + arrow_top) / 2, '$\nF\nL\nO\nW',
            fontsize=9, ha='center', va='center', color=AMBER,
            fontweight='bold', rotation=0)

    # Key insight box at bottom
    insight = (
        "KEY INSIGHT: x402 is not a revenue engine — it's a demand engine.  "
        "Coinbase captures value at the Currency layer (56% of USDC float income), "
        "Settlement layer (Base sequencer fees), and Distribution (wallet/commerce).  "
        "The protocol takes $0.  This is the Android strategy: give away the OS, monetize through services."
    )
    ax.text(50, 1.5, insight, fontsize=10.5, ha='center', va='center',
            color=TEXT_COLOR, fontstyle='italic',
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#0a0a1e',
                      edgecolor=CYAN, linewidth=2, alpha=0.95),
            wrap=True)

    fig.savefig('/Users/cat/memo-fintech-agents/charts/x402_10_value_accrual_stack.png',
                dpi=150, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close()
    print("✓ Chart 2: Value Accrual Stack saved")


# =============================================================================
# CHART 3: COINBASE FLYWHEEL DIAGRAM
# =============================================================================
def chart_coinbase_flywheel():
    fig, ax = plt.subplots(figsize=(16, 16))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.axis('off')
    ax.set_aspect('equal')

    ax.text(0, 1.4, 'The Coinbase x402 Flywheel',
            fontsize=22, fontweight='bold', ha='center', va='top', color=TEXT_COLOR)
    ax.text(0, 1.28, 'How an open protocol with $0 fees generates billions in adjacent revenue',
            fontsize=12, ha='center', va='top', color=LIGHT_BLUE, alpha=0.7)

    # Flywheel nodes
    nodes = [
        {'label': 'x402\nAdoption ↑', 'angle': 90, 'color': CYAN,
         'detail': 'Open protocol\n$0 fees'},
        {'label': 'More USDC\nTransactions', 'angle': 30, 'color': GREEN,
         'detail': '98.7% USDC\n$600M+ volume'},
        {'label': 'Base Gas\nRevenue ↑', 'angle': -30, 'color': AMBER,
         'detail': '$75.4M YTD\n62% L2 share'},
        {'label': 'USDC Float\nIncome ↑', 'angle': -90, 'color': PURPLE,
         'detail': '4.5% yield\nCB gets 56%'},
        {'label': 'Coinbase\nEcosystem ↑', 'angle': -150, 'color': PINK,
         'detail': 'Wallet + Commerce\n+ Exchange'},
        {'label': 'Developer\nAdoption ↑', 'angle': 150, 'color': LIGHT_BLUE,
         'detail': '5.4K stars\n117 projects'},
    ]

    radius = 0.85
    node_radius = 0.22

    # Draw connecting arrows (curved)
    for i in range(len(nodes)):
        j = (i + 1) % len(nodes)
        angle_i = np.radians(nodes[i]['angle'])
        angle_j = np.radians(nodes[j]['angle'])

        x_i = radius * np.cos(angle_i)
        y_i = radius * np.sin(angle_i)
        x_j = radius * np.cos(angle_j)
        y_j = radius * np.sin(angle_j)

        # Arrow from edge of node i to edge of node j
        dx = x_j - x_i
        dy = y_j - y_i
        dist = np.sqrt(dx**2 + dy**2)
        ux, uy = dx / dist, dy / dist

        start_x = x_i + ux * node_radius
        start_y = y_i + uy * node_radius
        end_x = x_j - ux * node_radius
        end_y = y_j - uy * node_radius

        ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                    arrowprops=dict(arrowstyle='->', color=GRID_COLOR,
                                    lw=2, connectionstyle='arc3,rad=0.15'))

    # Draw nodes
    for node in nodes:
        angle = np.radians(node['angle'])
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)

        circle = plt.Circle((x, y), node_radius, facecolor=BG_COLOR,
                            edgecolor=node['color'], linewidth=2.5, zorder=10)
        ax.add_patch(circle)

        ax.text(x, y + 0.04, node['label'], fontsize=11, fontweight='bold',
                ha='center', va='center', color=node['color'], zorder=11)

        # Detail text outside the circle
        detail_r = radius + 0.38
        dx = detail_r * np.cos(angle)
        dy = detail_r * np.sin(angle)
        ax.text(dx, dy, node['detail'], fontsize=9, ha='center', va='center',
                color=TEXT_COLOR, alpha=0.6, fontstyle='italic')

    # Center: Coinbase logo area
    center_circle = plt.Circle((0, 0), 0.28, facecolor=CARD_COLOR,
                               edgecolor=CYAN, linewidth=3, zorder=15)
    ax.add_patch(center_circle)
    ax.text(0, 0.06, 'COINBASE', fontsize=13, fontweight='bold',
            ha='center', va='center', color=CYAN, zorder=16)
    ax.text(0, -0.1, 'captures at\nevery layer', fontsize=9,
            ha='center', va='center', color=TEXT_COLOR, alpha=0.7, zorder=16)

    # Revenue breakdown box at bottom
    rev_text = (
        "COINBASE REVENUE FROM x402 ECOSYSTEM (per $1B annual volume)\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "  USDC reserve income share (56% of Circle yield)     $25M\n"
        "  Base sequencer fees (75% of x402 on Base)            $7.5M\n"
        "  Facilitator fees ($0.001/tx)                          $1M\n"
        "  Commerce / merchant services                         $2-5M\n"
        "  ─────────────────────────────────────────────────────────\n"
        "  TOTAL DIRECT                                        ~$35-38M\n\n"
        "  At $10B volume (2029-2030):                       $350-380M"
    )
    ax.text(0, -1.35, rev_text, fontsize=10, ha='center', va='center',
            color=TEXT_COLOR, fontfamily='monospace',
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#0a0a1e',
                      edgecolor=PURPLE, linewidth=2, alpha=0.95))

    fig.savefig('/Users/cat/memo-fintech-agents/charts/x402_11_coinbase_flywheel.png',
                dpi=150, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close()
    print("✓ Chart 3: Coinbase Flywheel saved")


if __name__ == '__main__':
    chart_buyer_seller_ratio()
    chart_value_stack()
    chart_coinbase_flywheel()
    print("\nAll 3 charts generated successfully.")
