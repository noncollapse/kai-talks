#!/usr/bin/env python3
"""Reproduce the opening radar figure from the paper's frozen numeric results.

Requires matplotlib==3.10.6 and numpy. Run from any directory.
No experiment execution, digitized data, or placeholder baseline curves.
"""
from pathlib import Path
import csv
import hashlib
import json
import math
import statistics

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'figures/data/stress_per_regime_results.csv'
MANIFEST = ROOT / 'figures/data/stress_radar_provenance.json'
OUT = ROOT / 'public/figs'
STEM = 'stress-opening-radar'
SETTINGS = [
    ('near_constant', 'Near-constant'),
    ('bounded', 'Bounded'),
    ('quantized', 'Quantized'),
    ('discontinuous', 'Discontinuous'),
    ('near_zero', 'Near-zero'),
    ('high_noise', 'High noise'),
    ('heavy_tail_noise', 'Heavy-tail\nnoise'),
    ('asymmetric_extreme_outlier', 'Asymmetric\noutliers'),
    ('heteroscedastic', 'Heteroscedastic'),
    ('categorical_missing', 'Categorical\n+ missing'),
]
METHODS = ['Linear', 'RFF', 'PI', 'Bootstrap', 'AMP', 'TabCon']
NAMES = {'PI': 'TabPFN (PI)'}
STYLES = {
    'Linear': ('#a18470', 'o', (0, (1.5, 2.3))),
    'RFF': ('#9b88bd', '^', (0, (2, 2.2))),
    'PI': ('#8594ad', 's', '-'),
    'Bootstrap': ('#526075', 'X', (0, (4, 2, 1, 2))),
    'AMP': ('#b46e9e', 'D', (0, (4, 2))),
    'TabCon': ('#4263eb', 'o', '-'),
}
BG, INK, MUTED, GRID, TARGET = '#fbfcff', '#17233e', '#64748b', '#dfe5f0', '#0b9687'


def load():
    provenance = json.loads(MANIFEST.read_text())
    assert hashlib.sha256(DATA.read_bytes()).hexdigest() == provenance['source_sha256']
    rows = list(csv.DictReader(DATA.open()))
    table = {(r['regime'], r['method']): r for r in rows}
    for regime, _ in SETTINGS:
        for method in METHODS:
            row = table[regime, method]
            assert int(row['tasks']) == 128
            assert 0.55 <= float(row['coverage_95']) <= 1
            assert .003 <= float(row['length_95']) <= 20
    return table


def closed(values):
    return np.r_[values, values[0]]


def main():
    data = load()
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({
        'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'DejaVu Sans'],
        'font.size': 14, 'text.color': INK, 'axes.labelcolor': INK,
        'svg.fonttype': 'none', 'pdf.fonttype': 42,
        'figure.facecolor': BG, 'axes.facecolor': BG,
        'savefig.facecolor': BG, 'axes.unicode_minus': False,
    })
    fig = plt.figure(figsize=(14.4, 6.1))
    axes = [fig.add_axes([.085, .105, .37, .67], projection='polar'),
            fig.add_axes([.545, .105, .37, .67], projection='polar')]
    angles = np.linspace(0, 2 * math.pi, len(SETTINGS), endpoint=False)
    theta = closed(angles)
    handles = {}

    for index, ax in enumerate(axes):
        ax.set_theta_offset(math.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_ylim(0, 1)
        ax.set_xticks(angles)
        ax.set_xticklabels([])
        ax.grid(color=GRID, linewidth=.8)
        ax.spines['polar'].set_color('#c5cfe0')
        ax.spines['polar'].set_linewidth(1)
        ax.set_axisbelow(True)
        for angle, (_, label) in zip(angles, SETTINGS):
            horizontal = math.sin(angle)
            ha = 'center' if abs(horizontal) < .2 else ('left' if horizontal > 0 else 'right')
            ax.text(angle, 1.09, label, ha=ha, va='center', fontsize=13.4,
                    color='#455773', linespacing=1.15, clip_on=False)

        if index == 0:
            transform = lambda x: (x - .55) / .45
            ticks = [.6, .7, .8, .9, 1]
            metric = 'coverage_95'
            ax.set_yticks([transform(v) for v in ticks])
            ax.set_yticklabels([f'{v:.0%}' for v in ticks], fontsize=10.7, color=MUTED)
            ax.plot(theta, np.full_like(theta, transform(.95)), color=TARGET,
                    linewidth=2.1, linestyle=(0, (5, 3)), zorder=5)
        else:
            transform = lambda x: (math.log10(x) - math.log10(.003)) / math.log10(20 / .003)
            metric = 'length_95'
            ticks = [.01, .1, 1, 10]
            ax.set_yticks([transform(v) for v in ticks])
            ax.set_yticklabels(['0.01', '0.1', '1', '10'], fontsize=10.7, color=MUTED)
        ax.set_rlabel_position(18)
        for tick in ax.get_yticklabels():
            tick.set_bbox(dict(facecolor=BG, edgecolor='none', pad=.3, alpha=.85))

        for method in METHODS:
            color, marker, dash = STYLES[method]
            values = [transform(float(data[regime, method][metric])) for regime, _ in SETTINGS]
            prominent = method == 'TabCon'
            ax.plot(theta, closed(values), color=color, marker=marker,
                    markersize=5.7 if prominent else 4.3,
                    markerfacecolor=color if prominent else BG,
                    markeredgewidth=1.15, linestyle=dash,
                    linewidth=3.4 if prominent else 1.65,
                    zorder=8 if prominent else 3, alpha=1 if prominent else .9)
            if prominent:
                ax.fill(theta, closed(values), color=color, alpha=.065, zorder=1)
            handles[method] = Line2D([0], [0], color=color, marker=marker, linestyle=dash,
                                    markerfacecolor=color if prominent else BG,
                                    linewidth=3 if prominent else 1.65, markersize=6)

    order = ['TabCon', 'PI', 'AMP', 'Bootstrap', 'Linear', 'RFF']
    target_handle = Line2D([0], [0], color=TARGET, linewidth=2.1, linestyle=(0, (5, 3)))
    legend = fig.legend([handles[m] for m in order] + [target_handle],
                       [NAMES.get(m, m) for m in order] + ['95% target'],
                       loc='upper center', bbox_to_anchor=(.5, 1), ncol=7,
                       frameon=False, fontsize=13.4, handlelength=2.2,
                       handletextpad=.55, columnspacing=1.5)
    legend.get_texts()[0].set_color(STYLES['TabCon'][0])
    legend.get_texts()[0].set_fontweight('bold')
    for x, title, subtitle in [(.27, 'Coverage probability', 'Closer to the 95% target is better'),
                               (.73, 'Interval length', 'Smaller radius = shorter · log scale')]:
        fig.text(x, .884, title, ha='center', fontsize=19, weight='bold', color=INK)
        fig.text(x, .844, subtitle, ha='center', fontsize=12, color=MUTED)

    for suffix in ['svg', 'pdf', 'png']:
        fig.savefig(OUT / f'{STEM}.{suffix}', dpi=180, metadata={'Creator': 'TabCon slide figure script'})
    plt.close(fig)
    metrics = {}
    for method in METHODS:
        metrics[method] = {
            'mean_coverage': statistics.fmean(float(data[r, method]['coverage_95']) for r, _ in SETTINGS),
            'mean_length': statistics.fmean(float(data[r, method]['length_95']) for r, _ in SETTINGS),
        }
    summary = {
        'nominal_coverage': .95, 'settings': len(SETTINGS), 'tasks_per_setting': 128,
        'aggregation': 'Unweighted arithmetic means across the ten stress settings; each has 128 tasks.',
        'methods': metrics,
        'tabcon_length_reduction_vs_tabpfn_pi': 1 - metrics['TabCon']['mean_length'] / metrics['PI']['mean_length'],
        'coverage_axis': {'minimum': .55, 'maximum': 1.0, 'scale': 'linear'},
        'length_axis': {'minimum': .003, 'maximum': 20, 'scale': 'log10'},
    }
    (ROOT / 'figures/data/stress_preview_summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
