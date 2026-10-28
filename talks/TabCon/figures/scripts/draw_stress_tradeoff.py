#!/usr/bin/env python3
"""Draw signed coverage deviations against interval length from verified CSVs.

Six original methods plus completed, paired interval baselines. No runtime or
candidate-method results are inferred. Coverage is evaluated against the saved latent oracle;
this script does not equate it with the conditional mean given observed X.
"""
import csv
import hashlib
import json
import math
import statistics

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator

from draw_stress_preview import ROOT, OUT, SETTINGS, METHODS as ORIGINAL_METHODS, NAMES as ORIGINAL_NAMES, STYLES as ORIGINAL_STYLES, BG, INK, MUTED, GRID, load

STEM = 'stress-opening-tradeoff'
NOMINAL = .95
FIRST_ADDITIONS = ['GRF', 'Local Linear Forest', 'BDE']
NAMES = {**ORIGINAL_NAMES, 'PI': 'TabPFN (Prediction Interval)'}
STYLES = {**ORIGINAL_STYLES,
    'GRF': ('#368267', 'P', '-'),
    'Local Linear Forest': ('#1b94a7', 'v', '-'),
    'BDE': ('#b58a3d', 'h', '-'),
    'RF-IJ': ('#586cb3', 'D', '-'),
    'DRF': ('#a65d73', '>', '-'),
    'BRAT-P': ('#8c647c', 's', '-'),
    'BRAT-D': ('#c07751', '^', '-'),
    'RF-U': ('#8c8a2d', 'p', '-'),
}


def load_additional(table):
    path = ROOT / 'figures/data/stress_additional_ci_results.csv'
    provenance = json.loads((ROOT / 'figures/data/stress_additional_ci_provenance.json').read_text())
    assert hashlib.sha256(path.read_bytes()).hexdigest() == provenance['source_sha256']
    rows = list(csv.DictReader(path.open()))
    assert len(rows) == 30
    assert len({(r['regime'], r['method']) for r in rows}) == 30
    for row in rows:
        assert row['method'] in FIRST_ADDITIONS
        assert int(row['tasks']) == 128
        assert 0 <= float(row['coverage_95']) <= 1
        assert math.isfinite(float(row['length_95'])) and float(row['length_95']) > 0
        table[row['regime'], row['method']] = row
    for method in FIRST_ADDITIONS:
        assert provenance['methods'][method]['tasks'] == 1280
        assert provenance['methods'][method]['queries'] == 155520
    return provenance


def load_extra(table):
    path = ROOT/'figures/data/stress_extra_ci_results.csv'
    if not path.exists():
        return {'methods': {}}
    provenance = json.loads((ROOT/'figures/data/stress_extra_ci_provenance.json').read_text())
    assert hashlib.sha256(path.read_bytes()).hexdigest()==provenance['source_sha256']
    rows = list(csv.DictReader(path.open()))
    methods = list(provenance['methods'])
    assert set(methods)<= {'RF-IJ', 'DRF'}, 'Bayesian baselines were cancelled by the user'
    assert len(rows)==10*len(methods)
    assert {(r['regime'],r['method']) for r in rows} == {
        (regime,method) for regime,_ in SETTINGS for method in methods}
    for method in methods:
        p = provenance['methods'][method]
        assert p['tasks']==1280 and p['queries']==155520 and p['locally_verified']
    for row in rows:
        assert int(row['tasks'])==128
        assert 0<=float(row['coverage_95'])<=1
        assert math.isfinite(float(row['length_95'])) and float(row['length_95'])>0
        table[row['regime'],row['method']] = row
    return provenance


def load_modern(table):
    path = ROOT/'figures/data/stress_modern_ci_results.csv'
    if not path.exists():
        return {'methods': {}}
    provenance = json.loads((ROOT/'figures/data/stress_modern_ci_provenance.json').read_text())
    assert hashlib.sha256(path.read_bytes()).hexdigest()==provenance['source_sha256']
    rows = list(csv.DictReader(path.open()))
    methods = list(provenance['methods'])
    assert set(methods)=={'BRAT-P','BRAT-D','RF-U','Inferable EBM'}
    assert len(rows)==40
    assert {(r['regime'],r['method']) for r in rows} == {
        (regime,method) for regime,_ in SETTINGS for method in methods}
    for method in methods:
        p = provenance['methods'][method]
        assert p['tasks']==1280 and p['queries']==155520 and p['locally_verified']
    for row in rows:
        assert int(row['tasks'])==128 and row['interval_kind']=='confidence'
        assert 0<=float(row['coverage_95'])<=1
        assert math.isfinite(float(row['length_95'])) and float(row['length_95'])>0
        if row['method'] != 'Inferable EBM':
            table[row['regime'],row['method']] = row
    # Keep the complete, hashed source archive; EBM was excluded by the user.
    return {**provenance,
            'methods': {m: p for m, p in provenance['methods'].items() if m != 'Inferable EBM'},
            'excluded_from_plot': ['Inferable EBM']}


def point(ax, method, metrics, size=130):
    color, marker, _ = STYLES[method]
    row = metrics[method]
    prominent = method == 'TabCon'
    gap = row['mean_signed_coverage_gap_pp']
    ax.scatter(row['mean_length'], gap,
               s=size * (1.35 if prominent else 1), marker=marker,
               facecolor=color, edgecolor='white', linewidth=1.3,
               alpha=1 if prominent else .93, zorder=6)


def label(ax, method, metrics, offset, *, size=17, ha='left', va='center', boxed=False):
    row = metrics[method]
    color = STYLES[method][0]
    ax.annotate(NAMES.get(method, method),
                (row['mean_length'], row['mean_signed_coverage_gap_pp']),
                xytext=offset, textcoords='offset points',
                fontsize=size, color=color, weight='bold', ha=ha, va=va,
                bbox=dict(boxstyle='round,pad=.28', facecolor='#edf1ff',
                          edgecolor='#cbd5ff', linewidth=1) if boxed else None,
                zorder=8)


def main():
    table = load()
    additional = load_additional(table)
    extra = load_extra(table)
    modern = load_modern(table)
    methods = ORIGINAL_METHODS + FIRST_ADDITIONS + list(extra['methods']) + list(modern['methods'])
    metrics = {}
    for method in methods:
        coverages = [float(table[r, method]['coverage_95']) for r, _ in SETTINGS]
        lengths = [float(table[r, method]['length_95']) for r, _ in SETTINGS]
        signed_gaps = [100 * (coverage - NOMINAL) for coverage in coverages]
        metrics[method] = {
            'mean_coverage': statistics.fmean(coverages),
            'mean_length': statistics.fmean(lengths),
            # Absolute deviation is computed BEFORE averaging across settings.
            'mean_absolute_coverage_gap_pp': 100 * statistics.fmean(abs(c - NOMINAL) for c in coverages),
            'mean_signed_coverage_gap_pp': statistics.fmean(signed_gaps),
            'min_signed_coverage_gap_pp': min(signed_gaps),
            'max_signed_coverage_gap_pp': max(signed_gaps),
            'undercoverage_settings': sum(gap < 0 for gap in signed_gaps),
            'overcoverage_settings': sum(gap > 0 for gap in signed_gaps),
        }
    summary = {
        'nominal_coverage': NOMINAL,
        'settings': len(SETTINGS), 'tasks_per_setting': 128,
        'aggregation': 'Equal-weight means across ten stress settings. Each setting contains 128 tasks.',
        'coverage_gap_definition': 'Plotted y = 100 * mean_s(coverage_95_s - 0.95), in percentage points. Negative: undercoverage; positive: overcoverage.',
        'display': 'One point per method showing its mean interval length and mean signed coverage deviation across ten stress settings. No range bars are plotted; setting-level variation is retained in the summary metrics.',
        'coverage_target': 'Saved latent oracle from the original stress evaluation; not independently verified as E[Y|observed X].',
        'x_axis': 'Arithmetic mean interval length in the original outcome units, displayed on a logarithmic axis. No scale normalization.',
        'methods': metrics,
        'native_interval_kinds': {m: ('prediction' if m == 'PI' else 'credible' if m == 'AMP' else 'confidence') for m in methods},
        'tabcon_length_reduction_vs_tabpfn_pi': 1 - metrics['TabCon']['mean_length'] / metrics['PI']['mean_length'],
        'scope': 'Six original methods plus completed ' + ', '.join(FIRST_ADDITIONS + list(extra['methods']) + list(modern['methods'])) + ' evaluations on the original 1280 paired tasks. DeepLR excluded; unfinished methods not plotted.',
        'additional_results_source_sha256': additional['source_sha256'],
        'extra_results_source_sha256': extra.get('source_sha256'),
        'modern_results_source_sha256': modern.get('source_sha256'),
        'bde_note': additional['bde_note'],
        'excluded_methods': {'Inferable EBM': 'Removed at user request on 2026-10-27; original results retained.'},
    }
    plt.rcParams.update({
        'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'DejaVu Sans'],
        'font.size': 14, 'text.color': INK, 'axes.labelcolor': INK,
        'svg.fonttype': 'none', 'pdf.fonttype': 42,
        'figure.facecolor': BG, 'axes.facecolor': BG,
        'savefig.facecolor': BG, 'axes.unicode_minus': False,
    })
    # Place direction guides inside the plot so margins can serve the data.
    fig = plt.figure(figsize=(13.6, 5.8))
    ax = fig.add_axes([.075, .115, .91, .82])
    summary['broken_x_axis'] = False
    ax.set_xscale('log')
    ax.set_xlim(.15, 30)
    ax.set_ylim(-85, 5.5)
    ax.axhspan(0, ax.get_ylim()[1], color='#e9f5f3', alpha=.65, zorder=0)
    ax.axhspan(ax.get_ylim()[0], 0, color='#fff1ec', alpha=.38, zorder=0)
    ax.xaxis.set_major_locator(FixedLocator([.2,.5,1,2,5,10,20] if modern['methods'] else [.5,1,2,4,8,16]))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f'{value:g}'))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.set_yticks([-80,-60,-40,-20,0,5] if modern['methods'] else [-40,-30,-20,-10,0,5])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f'{value:+g}' if value else '0'))
    ax.tick_params(axis='both', labelsize=13, length=0, pad=8, colors=MUTED)
    ax.set_xlabel('Mean interval length (log scale)', fontsize=16, labelpad=7)
    ax.set_ylabel('Coverage deviation from 95% (pp)', fontsize=16, labelpad=10)
    ax.grid(color=GRID, linewidth=.8)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color('#c9d3e3')
        spine.set_linewidth(.9)

    # Signed deviations are minimized in distance to zero, not toward -infinity.
    # Replace the old lower-left Pareto staircase with the nominal target line.
    ax.axhline(0, color='#345b74', linewidth=1.6, linestyle=(0, (5, 3)), zorder=3)
    ax.text(.17, 2.8, 'OVERCOVERAGE', color='#258476', fontsize=12, weight='bold', va='center')
    ax.text(.17, -6.5, 'UNDERCOVERAGE', color='#b87964', fontsize=12, weight='bold')
    ax.annotate('95% target', xy=(23, 0), xytext=(-2, -10),
                textcoords='offset points', ha='right', va='top',
                fontsize=12.5, color='#345b74',
                bbox=dict(facecolor=BG, edgecolor='none', pad=1.5))

    for method in methods:
        point(ax, method, metrics, size=100 if method in ('RF-IJ', 'PI', 'AMP') else 145)
    label(ax, 'Bootstrap', metrics, (-14, 3), ha='right')
    label(ax, 'RFF', metrics, (-12, 0), ha='right')
    label(ax, 'Linear', metrics, (13, 0))
    label(ax, 'PI', metrics, (0, 20), size=15.5, ha='center')
    label(ax, 'AMP', metrics, (12, 0), size=15.5)
    label(ax, 'TabCon', metrics, (-15, -11), size=17, ha='right', boxed=True)
    label(ax, 'BDE', metrics, (14, 0), size=16)
    # Keep labels close to their points, alternating sides in the dense cluster.
    # Matching label/marker colors identify methods without leader lines.
    cluster_labels = {
        'RF-U': ((12, 10), 'left'),
        'Local Linear Forest': ((-13, 2), 'right'),
        'DRF': ((14, -1), 'left'),
        'GRF': ((-13, 3), 'right'),
        'RF-IJ': ((13, -11), 'left'),
    }
    for method, (offset, alignment) in cluster_labels.items():
        if method in methods:
            label(ax, method, metrics, offset, size=16, ha=alignment)
    for method in modern['methods']:
        if method not in cluster_labels:
            label(ax, method, metrics, (14, 0), size=15.5)

    # Keep the horizontal guide at the bottom centre and the vertical guide
    # at the left centre. The upward guide remains below the nominal line.
    guide_arrow = dict(arrowstyle='->', color=MUTED, lw=1.3)
    ax.annotate('', xy=(.38, .14), xytext=(.62, .14),
                xycoords='axes fraction', arrowprops=guide_arrow)
    ax.text(.50, .085, 'Shorter intervals', transform=ax.transAxes,
            ha='center', va='center', fontsize=13.5, color=MUTED)
    ax.annotate('', xy=(.04, .65), xytext=(.04, .38),
                xycoords='axes fraction', arrowprops=guide_arrow)
    ax.text(.065, .515, 'Better coverage', transform=ax.transAxes,
            rotation=90, ha='center', va='center', fontsize=13.5, color=MUTED)

    for suffix in ['svg', 'pdf', 'png']:
        fig.savefig(OUT / f'{STEM}.{suffix}', dpi=220,
                    metadata={'Creator': 'TabCon stress tradeoff figure script'})
    plt.close(fig)
    summary['figure_sha256'] = hashlib.sha256((OUT / f'{STEM}.svg').read_bytes()).hexdigest()
    (ROOT / 'figures/data/stress_tradeoff_summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
