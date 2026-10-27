"""Freeze the original stress episodes, checking every one against saved Wald results."""
import argparse
import hashlib
import json
import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd

STRESSES = ['near_constant', 'bounded', 'quantized', 'discontinuous', 'near_zero',
            'high_noise', 'heavy_tail_noise', 'asymmetric_extreme_outlier',
            'heteroscedastic', 'categorical_missing']
GENERATOR_SHA = 'ad310101c33529299885f9beb73152fd7c24a4e0a9e68f8220d0096c6f6b17e7'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, obj):
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj, indent=2, allow_nan=False, default=str) + '\n')
    tmp.replace(path)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--original-repo', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--episodes', type=int, default=128)
    args = p.parse_args()
    repo = args.original_repo.resolve()
    sys.path.insert(0, str(repo))
    sys.path.insert(0, str(repo / 'src'))
    from experiments.data.pfn_episode_generator_v2 import make_stress_generator
    from experiments.wald_baselines.common import (
        ContextFeatureEncoder, _drop_constant_columns, evaluate_batch, stable_seed)

    generator_path = repo / 'experiments/data/pfn_episode_generator_v2.py'
    assert sha(generator_path) == GENERATOR_SHA, 'Generator differs from the plotted experiment'
    ref_path = repo / 'results/wald_baselines/linear_rff_hc3_seed0_20260920_104500/02_stress/raw_metrics.csv'
    reference = pd.read_csv(ref_path)
    reference = reference[reference.system == 'Linear-Wald-HC3'].set_index(['suite', 'episode'])
    args.out.mkdir(parents=True, exist_ok=True)
    manifest, failures = [], []
    for episode in range(args.episodes):
        for stress in STRESSES:
            task = f'{stress}__{episode:03d}'
            folder = args.out / task
            folder.mkdir(exist_ok=True)
            if (folder / 'metadata.json').exists():
                metadata = json.loads((folder / 'metadata.json').read_text())
                assert metadata['validated_against_saved_wald']
                for filename, digest in metadata['files'].items():
                    assert sha(folder / filename) == digest
                manifest.append(metadata)
                continue
            generated = make_stress_generator(base_seed=770001, stress=stress).sample(episode)
            batch = generated.batch
            expected = reference.loc[(stress, episode)]
            dims = dict(n_context=len(batch.y_context_noisy_raw),
                        n_query=len(batch.f_query_oracle_raw),
                        n_features=batch.X_query_raw.shape[1], episode_seed=generated.seed)
            for key, value in dims.items():
                assert value == int(expected[key]), (task, key, value, expected[key])
            result, _ = evaluate_batch(batch, seed=stable_seed('stress', stress, generated.seed),
                                      methods=['Linear-Wald-HC3'], coverages=[.95],
                                      rff_features=64, min_residual_df=8)
            got = result['Linear-Wald-HC3']
            checks = {k: dict(actual=float(got[k]), saved=float(expected[k]))
                      for k in ['coverage_95', 'length_95', 'mean_rmse']}
            # HC3 variances and therefore coverage are sensitive to BLAS/SVD
            # roundoff on ill-conditioned linear designs (condition > 1e6).
            # This preliminary check is the point prediction, not the variance.
            # A separate RFF replay is required before any full experiment.
            passed = np.isclose(checks['mean_rmse']['actual'], checks['mean_rmse']['saved'],
                                rtol=1e-6, atol=1e-8)
            if not passed:
                failures.append(dict(task=task, checks=checks))
                dump(args.out / 'alignment_failures.json', failures)
                raise RuntimeError(f'Task {task} does not reproduce saved Wald results: {checks}')

            encoder = ContextFeatureEncoder.fit(batch.X_context_raw)
            xc, xq, removed = _drop_constant_columns(
                encoder.transform(batch.X_context_raw), encoder.transform(batch.X_query_raw))
            assert xc.shape[1] > 0, 'All features constant; explicit method handling needed'
            # Oracle is deliberately separate: baseline adapters never load this file.
            np.savez_compressed(folder / 'inputs.npz', X=xc, y=batch.y_context_noisy_raw, Xq=xq)
            np.save(folder / 'oracle.npy', batch.f_query_oracle_raw)
            with (folder / 'raw.pkl').open('wb') as f:
                pickle.dump(dict(X=batch.X_context_raw, y=batch.y_context_noisy_raw,
                                 Xq=batch.X_query_raw, metadata=generated.metadata()), f)
            metadata = dict(task=task, stress=stress, episode=episode, **dims,
                            encoded_features=xc.shape[1], constant_columns_removed=removed,
                            generator_sha256=GENERATOR_SHA, checks=checks,
                            validated_against_saved_wald=True,
                            files={f: sha(folder / f) for f in ['inputs.npz', 'oracle.npy', 'raw.pkl']})
            dump(folder / 'metadata.json', metadata)
            manifest.append(metadata)
            print(json.dumps(dict(task=task, verified=len(manifest), **dims)), flush=True)
        dump(args.out / 'manifest.partial.json', manifest)
    dump(args.out / 'manifest.json', manifest)
    dump(args.out / 'alignment.linear.json', dict(status='passed', tasks=len(manifest),
         seed=770001, episodes_per_stress=args.episodes, stresses=STRESSES,
         original_metrics_sha256=sha(ref_path), generator_sha256=GENERATOR_SHA,
         validation='Every episode reproduces saved Linear-Wald-HC3 prediction RMSE; '
                    'HC3 width/coverage recorded separately due to ill-conditioned designs. RFF audit required.',
         limitation='Historical raw arrays were not found in the source evaluation directory; '
                    'matching numerical results is validation, not a historical byte-hash comparison.',
         target='Original saved f_query_oracle_raw; no change to latent-SCM target semantics',
         preprocessing='Context-only original Wald encoder; constant columns dropped; no projection'))


if __name__ == '__main__':
    main()
