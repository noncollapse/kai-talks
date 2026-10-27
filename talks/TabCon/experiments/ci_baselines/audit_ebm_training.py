"""Read-only instrumentation of the pinned official EBM; no oracle is opened.

Separate diagnostic runs, never written into modern_full or plotted as a benchmark.
"""
import os
for _key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_key] = "1"

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import inspect
import json
from pathlib import Path
import time
import numpy as np
from boulevard import ExplainableBooster

ROOT = Path(__file__).resolve().parent
TASKS = ["high_noise__042", "high_noise__000", "high_noise__001",
         "high_noise__007", "high_noise__030", "high_noise__029",
         "categorical_missing__042"]
VARIANTS = ["original", "subsample_08", "no_warmup", "lr_inverse_p", "lr_inverse_p_no_warmup"]


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


class ObservedBooster(ExplainableBooster):
    """Return exactly the author's updates; record copies/scalars only."""

    def _contributions_from_bins(self, bins, scores):
        result = super()._contributions_from_bins(bins, scores)
        frame = inspect.currentframe().f_back
        if frame.f_code is ExplainableBooster.fit.__code__ and scores is self.term_scores_:
            loc = frame.f_locals
            intercept = float(np.mean(self.audit_y - result))
            pred = intercept + result
            self.audit_trace.append(dict(
                phase="final_rescaling" if "finalization_start" in loc else "round",
                round=int(loc["round_idx"]),
                mse=float(np.mean((self.audit_y-pred)**2)),
                max_abs_prediction=float(np.max(np.abs(pred))),
                max_abs_term=float(max(np.max(np.abs(v)) for v in scores))))
        del frame
        return result

    def _fit_binned_tree_update(self, **kwargs):
        update, structure = super()._fit_binned_tree_update(**kwargs)
        frame = inspect.currentframe().f_back
        loc = frame.f_locals
        if frame.f_code is ExplainableBooster.fit.__code__:
            j, b, p = int(loc["feature_idx"]), int(loc["round_idx"]), int(loc["n_features"])
            residual = kwargs["residual"]
            if j == 0:
                self.audit_update = np.zeros_like(residual)
            centered = update - np.dot(kwargs["full_bin_counts"], update)/len(residual)
            self.audit_update += centered[kwargs["feature_bins"]]
            if j == p-1:
                denom = max(float(np.dot(residual,residual)), 1e-300)
                self.audit_steps.append(dict(
                    round=b, input_mse=float(np.mean(residual**2)),
                    summed_update_norm_ratio=float(np.linalg.norm(self.audit_update)/np.sqrt(denom)),
                    summed_update_projection=float(np.dot(self.audit_update,residual)/denom)))
        del frame
        return update, structure


def run_one(job):
    task, variant, out_base = job
    old = ROOT/"runs/modern_full/iebm"/task
    config = json.loads((old/"config.json").read_text())
    input_path = ROOT/"data"/task/"inputs.npz"
    input_sha = hashlib.sha256(input_path.read_bytes()).hexdigest()
    assert input_sha == config["input_sha256"]
    with np.load(input_path) as d:
        X, y, Xq = [np.asarray(d[k], dtype=float) for k in ("X","y","Xq")]
    params = dict(config["parameters"])
    if variant == "subsample_08": params["subsample_rate"] = .8
    if variant in ("no_warmup", "lr_inverse_p_no_warmup"): params["warmup_rounds"] = 0
    if variant in ("lr_inverse_p", "lr_inverse_p_no_warmup"): params["learning_rate"] = 1./X.shape[1]
    ym, ys = float(y.mean()), float(y.std())
    ystd = (y-ym)/ys
    model = ObservedBooster(**params, random_state=config["seed"])
    model.audit_y, model.audit_trace, model.audit_steps = ystd, [], []
    started = time.monotonic()
    model.fit(X, ystd)
    model.prepare_inference()
    lo, hi, mean = model.predict_intervals(Xq, level=.95, mode="confidence")
    train_mse = float(np.mean((ystd-model.predict(X))**2))
    assert len(model.audit_trace)==params["max_rounds"]+1
    assert len(model.audit_steps)==params["max_rounds"]
    np.testing.assert_allclose(model.audit_trace[-1]["mse"],train_mse,rtol=1e-12,atol=1e-12)
    reproduced = None
    if variant == "original":
        with np.load(old/"inference_diagnostics.npz") as saved:
            np.testing.assert_allclose(mean,saved["mean_standardized"],rtol=1e-12,atol=1e-12)
            np.testing.assert_allclose(model.sigma_hat2_,saved["sigma2"],rtol=1e-12,atol=1e-12)
            reproduced = bool(np.array_equal(mean,saved["mean_standardized"]))
        with np.load(old/"predictions.npz") as saved:
            np.testing.assert_allclose(lo*ys+ym,saved["lower"],rtol=1e-12,atol=1e-12)
            np.testing.assert_allclose(hi*ys+ym,saved["upper"],rtol=1e-12,atol=1e-12)
    summary = dict(task=task,variant=variant,n=len(y),p=X.shape[1],parameters=params,
        seed=config["seed"],input_sha256=input_sha,initial_mse=float(np.mean(ystd**2)),
        final_train_mse=train_mse,sigma2=float(model.sigma_hat2_),
        max_round_mse=max(v["mse"] for v in model.audit_trace),
        max_query_abs_mean_standardized=float(np.max(np.abs(mean))),
        mean_interval_length_original_units=float(np.mean(hi-lo)*ys),
        original_prediction_bitwise_reproduced=reproduced,
        seconds=time.monotonic()-started,oracle_opened=False,
        source_sha256=hashlib.sha256(Path(inspect.getfile(ExplainableBooster)).read_bytes()).hexdigest())
    dest = Path(out_base)/task/variant
    dump(dest/"summary.json",summary)
    dump(dest/"trace.json",dict(rounds=model.audit_trace,updates=model.audit_steps))
    return summary


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--workers",type=int,default=4)
    parser.add_argument("--out",type=Path,default=ROOT/"runs/ebm_audit_20261027")
    args=parser.parse_args()
    jobs=[(t,v,str(args.out)) for t in TASKS for v in VARIANTS]
    dump(args.out/"launch.json",dict(tasks=TASKS,variants=VARIANTS,
        selection="Worst original task; other n/p regimes; low-p controls; tiny unsplittable context; encoded categorical counterpart",
        protocol="Same original inputs/seeds. Only listed parameter interventions. No oracle, no benchmark replacement.",
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),started_at=time.time()))
    summaries=[]
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures=[executor.submit(run_one,j) for j in jobs]
        for future in as_completed(futures):
            result=future.result();summaries.append(result)
            print(json.dumps(result),flush=True)
    dump(args.out/"summary.json",sorted(summaries,key=lambda v:(v["task"],v["variant"])))


if __name__=="__main__": main()
