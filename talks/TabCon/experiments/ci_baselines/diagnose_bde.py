"""Observe an isolated BDE replay without changing its training or random draws.

Usage: python diagnose_bde.py --task high_noise__053 --out runs/audit/bde_replay
The ordinary adapter is run unchanged, with read-only epoch observations added.
"""
import sys
import json
import runpy
from pathlib import Path

import run_task  # Set the original CPU/thread environment before TensorFlow.
import numpy as np
import tensorflow as tf

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'runtime_vendor' / 'bde'))
import neural_networks as nn

seed_offset = 0
global_clipnorm = None
if '--global-clipnorm' in sys.argv:
    pos = sys.argv.index('--global-clipnorm')
    global_clipnorm = float(sys.argv[pos + 1])
    del sys.argv[pos:pos + 2]
if '--seed-offset' in sys.argv:
    pos = sys.argv.index('--seed-offset')
    seed_offset = int(sys.argv[pos + 1])
    del sys.argv[pos:pos + 2]
set_seed = tf.keras.utils.set_random_seed


def diagnostic_seed(seed):
    report['actual_seed'] = seed + seed_offset
    set_seed(seed + seed_offset)


tf.keras.utils.set_random_seed = diagnostic_seed
OUT = Path(sys.argv[sys.argv.index('--out') + 1]).resolve()
if (OUT / 'metrics.json').exists():
    raise RuntimeError('Use a fresh diagnostic directory; completed evidence is never overwritten.')
OUT.mkdir(parents=True, exist_ok=True)
TRACE = OUT / 'trace'
TRACE.mkdir(exist_ok=True)
report = {'fits': [], 'networks': [], 'seed_offset': seed_offset,
          'global_clipnorm': global_clipnorm,
          'purpose': 'diagnostic only; no production replacement'}
active = {'kind': '', 'member': -1}
counts = {'base': 0, 'bootstrap': 0}


def stats(a):
    a = np.asarray(a, dtype=np.float64)
    finite = a[np.isfinite(a)]
    return dict(shape=list(a.shape), finite=bool(np.isfinite(a).all()),
                mean=float(finite.mean()), std=float(finite.std()),
                quantiles=np.quantile(finite, [0, .01, .5, .99, 1]).tolist())


def flush():
    (OUT / 'diagnostics.json').write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')


original_fit = tf.keras.Model.fit


def observed_fit(model, x=None, y=None, *args, **kwargs):
    if global_clipnorm is not None:
        # Optional sensitivity experiment, never the production protocol.
        # Set before the first train-function trace; do not reset Adam state.
        model.optimizer.global_clipnorm = global_clipnorm
    index = len(report['fits'])
    record = dict(index=index, **active, x=stats(x), y=stats(y),
                  global_clipnorm=model.optimizer.global_clipnorm,
                  optimizer_start=int(model.optimizer.iterations), epochs=[])
    report['fits'].append(record)
    np.savez_compressed(TRACE / f'fit_{index:02d}_inputs.npz', X=x, y=y)
    x_tensor = tf.convert_to_tensor(x, dtype=tf.float32)

    class Observe(tf.keras.callbacks.Callback):
        def on_train_batch_end(self, batch, logs=None):
            if active['kind'] == 'base' and active['member'] == 1:
                # This row has the largest absolute standardized input value.
                row = int(np.argmax(np.max(np.abs(x), axis=1)))
                output = model(x_tensor[row:row + 1], training=False).numpy()[0]
                record.setdefault('rare_row_batches', []).append(dict(
                    iteration=int(model.optimizer.iterations), row=row,
                    mean=float(output[0]), log_sigma=float(output[1]),
                    cumulative_epoch_loss=float(logs['loss'])))

        def on_epoch_end(self, epoch, logs=None):
            # No predict()/fit(), random draws or mutable model state in this hook.
            output = model(x_tensor, training=False).numpy()
            record['epochs'].append(dict(epoch=epoch + 1,
                loss=float(logs['loss']), mean=stats(output[:, 0]),
                log_sigma=stats(output[:, 1])))

    kwargs['callbacks'] = list(kwargs.get('callbacks') or []) + [Observe()]
    history = original_fit(model, x, y, *args, **kwargs)
    record['optimizer_end'] = int(model.optimizer.iterations)
    record['weight_max_abs'] = [float(np.max(np.abs(w.numpy()))) for w in model.weights]
    model.save(TRACE / f'fit_{index:02d}_final.keras')
    flush()
    return history


tf.keras.Model.fit = observed_fit


def wrap_init(original, kind):
    def observed(self, X, Y, *args, **kwargs):
        index = counts[kind]
        counts[kind] += 1
        active.update(kind=kind, member=index)
        np.savez_compressed(TRACE / f'{kind}_{index}_raw_inputs.npz', X=X, y=Y)
        original(self, X, Y, *args, **kwargs)
        # Direct eager inference does not consume RNG or modify training state.
        z = (X - self._X_mean) / self._X_std
        output = self.model(tf.convert_to_tensor(z, dtype=tf.float32), training=False).numpy()
        sigma = (np.exp(output[:, 1]) + 1e-3) * self._Y_std
        mean = output[:, 0] * self._Y_std + self._Y_mean
        np.savez_compressed(TRACE / f'{kind}_{index}_context_outputs.npz',
            mean=mean, sigma=sigma, normalized_outputs=output,
            X_mean=self._X_mean, X_std=self._X_std,
            y_mean=self._Y_mean, y_std=self._Y_std)
        report['networks'].append(dict(kind=kind, member=index,
            y_raw=stats(Y), context_mean=stats(mean), context_sigma=stats(sigma)))
        flush()
    return observed


nn.LikelihoodNetwork.__init__ = wrap_init(nn.LikelihoodNetwork.__init__, 'base')
nn.ExtraTrainedNetwork.__init__ = wrap_init(nn.ExtraTrainedNetwork.__init__, 'bootstrap')
sys.argv += ['--method', 'bde']
runpy.run_path(str(ROOT / 'run_task.py'), run_name='__main__')

task = sys.argv[sys.argv.index('--task') + 1]
reference = ROOT / 'runs' / 'full' / 'bde' / task / 'members.npz'
if reference.exists():
    old, new = np.load(reference), np.load(OUT / 'members.npz')
    report['reference_comparison'] = {
        key: dict(bitwise_equal=bool(np.array_equal(old[key], new[key])),
                  max_abs_difference=float(np.max(np.abs(old[key]-new[key]))))
        for key in old.files}
config_path = OUT / 'config.json'
config = json.loads(config_path.read_text())
config.update(seed=report['actual_seed'], diagnostic_only=True,
              global_clipnorm=global_clipnorm)
config_path.write_text(json.dumps(config, indent=2) + '\n')
metrics_path = OUT / 'metrics.json'
metrics = json.loads(metrics_path.read_text())
metrics.update(production=False, diagnostic_only=True)
metrics_path.write_text(json.dumps(metrics, indent=2) + '\n')
flush()
print(json.dumps(report.get('reference_comparison', {})), flush=True)
