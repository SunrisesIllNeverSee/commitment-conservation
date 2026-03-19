#!/usr/bin/env python3
"""Generate 4 publication figures for the Commitment Conservation Experimental Record."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import json, os

BASE = '/Users/dericmchenry/Desktop/commitment-conservation-experiments'
FOOTER = 'MO§ES™  ·  Ello Cello LLC  ·  Patent No. 63/877,177 (Provisional)'

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica Neue', 'Arial', 'DejaVu Sans'],
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# ── shared helpers ────────────────────────────────────────────────────────────

def box(ax, cx, cy, w, h, txt, fc, fs=8.5, tc='white'):
    p = mpatches.FancyBboxPatch(
        (cx - w/2, cy - h/2), w, h,
        boxstyle='round,pad=0.04', fc=fc, ec='white', lw=1.2, zorder=2)
    ax.add_patch(p)
    ax.text(cx, cy, txt, ha='center', va='center', fontsize=fs,
            color=tc, fontweight='bold', multialignment='center',
            zorder=3, linespacing=1.4)

def arrow(ax, cx, y_from, y_to, col='#777'):
    ax.annotate('', xy=(cx, y_to + 0.04), xytext=(cx, y_from - 0.04),
        arrowprops=dict(arrowstyle='->', lw=1.5, color=col), zorder=1)


# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 1 — Harness Architecture
# ═════════════════════════════════════════════════════════════════════════════

def fig1_harness():
    fig, ax = plt.subplots(figsize=(13, 9.5))
    bg = '#F7F7F7'
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 10)
    ax.axis('off')

    BLUE = '#2B5797'; OG = '#C25B14'; GR = '#1B5E20'
    GRM  = '#2E7D32'; GRL = '#43A047'; DARK = '#2C2C2C'; MEAS = '#7B0E0E'

    xs   = [2.2, 6.5, 10.8]
    cols = [BLUE, OG, GR]
    hdrs = ['BASELINE', 'COMPRESSION', 'GATE']
    subs = ['control · paraphrase only',
            'summarize · no gate',
            'summarize · extract · reconstruct']

    # column headers
    for cx, h, s, c in zip(xs, hdrs, subs, cols):
        ax.text(cx, 9.72, h,  ha='center', fontsize=11, fontweight='bold', color=c)
        ax.text(cx, 9.40, s,  ha='center', fontsize=7.5, color='#999', style='italic')

    # divider lines between columns
    for xd in [4.35, 8.65]:
        ax.axvline(x=xd, ymin=0.03, ymax=0.97, color='#ddd', lw=0.8, zorder=0)

    # input signal (all three)
    for cx in xs:
        box(ax, cx, 8.7, 3.2, 0.52, 'Input Signal  S', DARK)
        arrow(ax, cx, 8.44, 7.92)

    # ── BASELINE ──────────────────────────────────────
    box(ax, xs[0], 7.6, 3.2, 0.55, 'Paraphrase', BLUE)
    ax.text(xs[0], 7.08, 'repeat  x10 iterations', ha='center',
            fontsize=7.5, color=BLUE, style='italic')
    arrow(ax, xs[0], 6.88, 3.25, BLUE)

    # ── COMPRESSION ───────────────────────────────────
    box(ax, xs[1], 7.6, 3.2, 0.55, 'Step A\nSummarize', OG)
    ax.text(xs[1], 7.08, 'repeat  x10 iterations', ha='center',
            fontsize=7.5, color=OG, style='italic')
    arrow(ax, xs[1], 6.88, 3.25, OG)

    # ── GATE (3 steps) ────────────────────────────────
    box(ax, xs[2], 7.6, 3.2, 0.55, 'Step A\nSummarize', GR)
    arrow(ax, xs[2], 7.35, 6.82, GR)
    box(ax, xs[2], 6.5, 3.2, 0.55, 'Step B\nExtract Kernel', GRM, tc='#ddd')
    arrow(ax, xs[2], 6.24, 5.72, GRM)
    box(ax, xs[2], 5.4, 3.2, 0.55, 'Step C\nReconstruct', GRL, tc='#111')
    ax.text(xs[2], 4.88, 'repeat  x10 iterations', ha='center',
            fontsize=7.5, color=GR, style='italic')
    arrow(ax, xs[2], 4.68, 3.25, GR)

    # ── NLI measurement ───────────────────────────────
    for cx, c in zip(xs, cols):
        box(ax, cx, 2.9, 3.2, 0.55, 'Measure NLI\n+ Jaccard', MEAS, fs=8)
        arrow(ax, cx, 2.62, 1.98, c)

    # ── output labels ─────────────────────────────────
    out_labels = [
        'Drift without\nenforcement',
        'Surface compression\nstability',
        'Commitment\nconservation'
    ]
    for cx, lbl, c in zip(xs, out_labels, cols):
        box(ax, cx, 1.65, 3.2, 0.62, lbl, c, fs=8)

    # footer
    ax.text(6.5, 0.48,
        'GPT-4o-mini · temperature 0.3 · 10 recursive iterations per signal',
        ha='center', fontsize=8, color='#aaa', style='italic')
    ax.text(6.5, 0.18, FOOTER, ha='center', fontsize=7, color='#ccc')

    plt.tight_layout(pad=0.3)
    plt.savefig(f'{BASE}/figure1_harness_architecture.png', dpi=180,
                bbox_inches='tight', facecolor=bg)
    plt.close()
    print("Figure 1 done")


# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 2 — Results Heatmap
# ═════════════════════════════════════════════════════════════════════════════

def fig2_heatmap():
    # EXP-006: Baseline / Compression / Gate NLI@i10 (paper recursion test)
    exp006_labels = [
        'Abstract core',
        'Formal law statement',
        'First law restatement',
        'Enforcement conditionality',
    ]
    exp006 = np.array([
        [1.00, 0.50, 0.50],
        [1.00, 0.50, 0.00],
        [1.00, 0.00, 0.50],
        [1.00, 0.00, 0.00],
    ])

    # EXP-005: Gate / ANCH / ESCL NLI@i10 (mechanism isolation)
    exp005_labels = [
        'Procedural keystone',
        'Legal qualifier',
        'Quantified temporal',
        'Passive temporal',
        'Soft modal escalation',
    ]
    exp005 = np.array([
        [0.50, 0.50, 0.00],
        [0.50, 0.00, 1.00],
        [1.00, 1.00, 1.00],
        [1.00, 1.00, 1.00],
        [0.00, 0.00, 0.50],
    ])

    # EXP-007: Gate NLI@i10 (NP-negation probe)
    exp007_labels = [
        'No smoking.',
        'No entry without badge.',
        'No firearms on premises.',
        'No refunds after purchase.',
        'You must not smoke. (ctrl)',
        'You must not enter. (ctrl)',
    ]
    exp007 = np.array([[1.00], [1.00], [1.00], [1.00], [1.00], [1.00]])

    cmap = LinearSegmentedColormap.from_list(
        'conserve', ['#C62828', '#EF9A9A', '#FFFFFF', '#A5D6A7', '#1B5E20'])

    fig, axes = plt.subplots(1, 3, figsize=(14, 7),
                             gridspec_kw={'width_ratios': [3, 3, 1.2]})
    fig.patch.set_facecolor('#FAFAFA')
    fig.suptitle('NLI Stability @ i10 — Selected Signals Across Experiments',
                 fontsize=12, fontweight='bold', color='#222', y=1.01)

    panels = [
        (axes[0], exp006, exp006_labels,
         ['Baseline', 'Compression', 'Gate'],
         'EXP-006  ·  Paper Recursion Test'),
        (axes[1], exp005, exp005_labels,
         ['Gate', 'Gate+ANCH', 'Gate+ESCL'],
         'EXP-005  ·  Mechanism Isolation'),
        (axes[2], exp007, exp007_labels,
         ['Gate'],
         'EXP-007  ·  NP-Negation Probe'),
    ]

    for ax, data, row_labels, col_labels, title in panels:
        im = ax.imshow(data, cmap=cmap, vmin=0.0, vmax=1.0, aspect='auto')
        ax.set_xticks(range(len(col_labels)))
        ax.set_xticklabels(col_labels, fontsize=8.5, fontweight='bold', rotation=30, ha='right')
        ax.set_yticks(range(len(row_labels)))
        ax.set_yticklabels(row_labels, fontsize=8)
        ax.set_title(title, fontsize=9, fontweight='bold', color='#333', pad=8)
        ax.tick_params(length=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
        # annotate cells
        for r in range(data.shape[0]):
            for c in range(data.shape[1]):
                v = data[r, c]
                tc = 'white' if v < 0.35 or v > 0.85 else '#333'
                ax.text(c, r, f'{v:.2f}', ha='center', va='center',
                        fontsize=9, color=tc, fontweight='bold')

    # colorbar on last axis
    cbar = fig.colorbar(im, ax=axes[2], fraction=0.08, pad=0.15, shrink=0.8)
    cbar.set_label('NLI bidirectional\nentailment @ i10',
                   fontsize=7.5, color='#555')
    cbar.ax.tick_params(labelsize=7)

    fig.text(0.5, -0.04, FOOTER, ha='center', fontsize=7.5, color='#bbb')
    plt.tight_layout(pad=1.2)
    plt.savefig(f'{BASE}/figure2_results_heatmap.png', dpi=180,
                bbox_inches='tight', facecolor='#FAFAFA')
    plt.close()
    print("Figure 2 done")


# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 3 — Conservation Curve (actual run.json data)
# ═════════════════════════════════════════════════════════════════════════════

def fig3_conservation_curve():
    # Load EXP-005 quantified_temporal — Gate=1.00 fixpoint (best conservation example)
    d5 = json.load(open(f'{BASE}/EXP-005/run.json'))
    qt = next(e for e in d5 if 'quantified' in e['category'])
    qt_b = [x['nli_stability'] for x in qt['baseline_nli']]
    qt_c = [x['nli_stability'] for x in qt['compression_nli']]
    qt_g = [x['nli_stability'] for x in qt['gate_nli']]

    # Load EXP-006 enforcement_conditionality — starkest collapse
    d6 = json.load(open(f'{BASE}/EXP-006/run.json'))
    ec = next(e for e in d6 if 'enforcement' in e['category'])
    ec_b = [x['nli_stability'] for x in ec['baseline_nli']]
    ec_c = [x['nli_stability'] for x in ec['compression_nli']]
    ec_g = [x['nli_stability'] for x in ec['gate_nli']]

    iters = list(range(1, 11))
    BLUE = '#2B5797'; OG = '#C25B14'; GR = '#1B5E20'

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), sharey=True)
    fig.patch.set_facecolor('#FAFAFA')
    fig.suptitle(
        'NLI Commitment Stability Over 10 Recursive Iterations',
        fontsize=12, fontweight='bold', color='#222')

    def plot_panel(ax, b, c, g, title, signal_label, show_ylabel=True):
        ax.set_facecolor('#FAFAFA')
        ax.plot(iters, b, 'o-', color=BLUE, lw=2, ms=5, label='Baseline')
        ax.plot(iters, c, 's--', color=OG,  lw=2, ms=5, label='Compression')
        ax.plot(iters, g, 'D-',  color=GR,  lw=2.5, ms=6, label='Gate')
        ax.set_xlim(0.5, 10.5)
        ax.set_ylim(-0.08, 1.15)
        ax.set_xticks(iters)
        ax.set_yticks([0.0, 0.5, 1.0])
        ax.set_yticklabels(['0.00', '0.50', '1.00'], fontsize=9)
        ax.set_xlabel('Iteration', fontsize=9, color='#555')
        if show_ylabel:
            ax.set_ylabel('NLI bidirectional entailment', fontsize=9, color='#555')
        ax.axhline(y=1.0, color='#ccc', lw=0.8, ls=':')
        ax.axhline(y=0.5, color='#eee', lw=0.8, ls=':')
        ax.set_title(title, fontsize=10, fontweight='bold', color='#333', pad=8)
        ax.text(0.97, 0.05, f'Signal: {signal_label}', transform=ax.transAxes,
                ha='right', fontsize=7.5, color='#888', style='italic')
        ax.legend(fontsize=8, framealpha=0.8, loc='lower right')
        ax.tick_params(labelsize=8.5)
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)

    plot_panel(ax1, qt_b, qt_c, qt_g,
               'Conservation Under Gate\n(Regime A — modal-anchored)',
               '"Users must change passwords every 90 days."')
    plot_panel(ax2, ec_b, ec_c, ec_g,
               'Conservation Failure\n(EXP-006 — enforcement conditionality)',
               '"Commitment is conserved when enforcement is applied."',
               show_ylabel=False)

    # annotation: fixpoint label on left panel
    ax1.annotate('Gate fixpoint\nNLI=1.00', xy=(2, 1.00),
                 xytext=(4.5, 1.08),
                 fontsize=7.5, color=GR, fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color=GR, lw=1.2))
    # annotation: collapse label on right panel
    ax2.annotate('Gate collapses\nNLI=0.00', xy=(4, 0.00),
                 xytext=(5.5, 0.18),
                 fontsize=7.5, color='#C62828', fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color='#C62828', lw=1.2))

    fig.text(0.5, -0.04, FOOTER, ha='center', fontsize=7.5, color='#bbb')
    plt.tight_layout(pad=1.5)
    plt.savefig(f'{BASE}/figure3_conservation_curve.png', dpi=180,
                bbox_inches='tight', facecolor='#FAFAFA')
    plt.close()
    print("Figure 3 done")


# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 4 — Failure Mode Taxonomy
# ═════════════════════════════════════════════════════════════════════════════

def fig4_failure_modes():
    failure_modes = [
        # (category, name, short_desc, experiment, color)
        ('Step A Failures', 'Step A Boundary',
         'Summarizer strips qualifying content\nbefore extraction can see it.',
         'EXP-002/003', '#1565C0'),
        ('Step A Failures', 'Co-degraded Invariance',
         'Step A impoverishes signal before canonical\nextraction — NLI=1.00 masks real qualifier loss.',
         'EXP-003', '#1976D2'),
        ('Step A Failures', 'Modal Frame Inversion',
         'Anchor-preserving Step A strips prohibition\nframe — positive obligation replaces negative.',
         'EXP-005 (ANCH)', '#1E88E5'),

        ('Step B Failures', 'Structural Blindness',
         'Modal-pattern extractor cannot surface\nordering constraints or scope conditions.',
         'EXP-003/005', '#6A1B9A'),
        ('Step B Failures', 'NP-Negation Blindness',
         'Noun-phrase negation yields empty extraction\n— Jaccard=0.00 despite semantic conservation.',
         'EXP-007', '#7B1FA2'),

        ('Gate Failures', 'Obligation Escalation',
         'Step B upgrades soft modals ("should")\nto hard modals ("must") in gate output.',
         'EXP-004/005', '#B71C1C'),
        ('Gate Failures', 'Lexical Scope Widening',
         '"Firearms" compressed to "weapons";\ntaxonomic broadening at the noun level.',
         'EXP-007', '#C62828'),

        ('Structural / Formal', 'Formal Collapse',
         'Multi-condition formal statement merged\ninto structurally incorrect chain equality.',
         'EXP-006', '#E65100'),
        ('Structural / Formal', 'Self-referential Collapse',
         'Conditionality statement collapsed under\nthe exact failure mode it describes.',
         'EXP-006', '#EF6C00'),
    ]

    # Group by category
    categories = ['Step A Failures', 'Step B Failures',
                  'Gate Failures', 'Structural / Formal']
    cat_colors = {
        'Step A Failures':    '#E3F2FD',
        'Step B Failures':    '#F3E5F5',
        'Gate Failures':      '#FFEBEE',
        'Structural / Formal':'#FFF3E0',
    }
    cat_header_colors = {
        'Step A Failures':    '#1565C0',
        'Step B Failures':    '#6A1B9A',
        'Gate Failures':      '#B71C1C',
        'Structural / Formal':'#E65100',
    }

    fig = plt.figure(figsize=(14, 8))
    fig.patch.set_facecolor('#FAFAFA')
    fig.suptitle('Failure Mode Taxonomy — Commitment Conservation Experimental Series',
                 fontsize=12, fontweight='bold', color='#222', y=1.01)

    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Layout: 4 columns, rows per category
    col_x = [0.3, 3.8, 7.3, 10.8]
    card_w = 3.1
    card_h = 1.5
    padding = 0.25

    col_items = {cat: [] for cat in categories}
    for item in failure_modes:
        col_items[item[0]].append(item)

    for ci, cat in enumerate(categories):
        cx_center = col_x[ci] + card_w / 2
        # Category header
        header_box = mpatches.FancyBboxPatch(
            (col_x[ci], 7.2), card_w, 0.58,
            boxstyle='round,pad=0.03',
            fc=cat_header_colors[cat], ec='white', lw=1, zorder=2)
        ax.add_patch(header_box)
        ax.text(cx_center, 7.49, cat, ha='center', va='center',
                fontsize=9.5, color='white', fontweight='bold', zorder=3)

        items = col_items[cat]
        start_y = 6.6
        for item in items:
            _, name, desc, exp, fc = item
            cy = start_y - card_h / 2
            card = mpatches.FancyBboxPatch(
                (col_x[ci] + 0.05, cy - card_h/2), card_w - 0.1, card_h,
                boxstyle='round,pad=0.05',
                fc=cat_colors[cat], ec=fc, lw=1.5, zorder=2)
            ax.add_patch(card)
            ax.text(cx_center, cy + 0.28, name, ha='center', va='center',
                    fontsize=9, color=fc, fontweight='bold', zorder=3)
            ax.text(cx_center, cy - 0.15, desc, ha='center', va='center',
                    fontsize=7.5, color='#444', zorder=3, multialignment='center',
                    linespacing=1.35)
            ax.text(cx_center, cy - 0.56, exp, ha='center', va='center',
                    fontsize=7, color='#888', zorder=3, style='italic')
            start_y -= card_h + padding

    ax.text(7.0, 0.18, FOOTER, ha='center', fontsize=7.5, color='#bbb')

    plt.savefig(f'{BASE}/figure4_failure_modes.png', dpi=180,
                bbox_inches='tight', facecolor='#FAFAFA')
    plt.close()
    print("Figure 4 done")


# ── run all ──────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    fig1_harness()
    fig2_heatmap()
    fig3_conservation_curve()
    fig4_failure_modes()
    print("All figures saved to", BASE)
