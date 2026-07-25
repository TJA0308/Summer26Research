"""
Post-hoc condition-prior probability stacking for ALREADY-TRAINED End Milling
feed_coarse/roughness checkpoints -- ports the condition-prior insight from
cv_evaluate_32x3.py (its "cond_only"/"cond_stack" models, tested there only
against cheap HGB/tiny_cnn proxies under leave-one-condition-out CV) onto the
REAL backbones (resnet18/50, efficientnet_b0, convnext_tiny) from the actual
training sweep -- without retraining anything. Reuses predict_conditioning_32x3.py's
_load_module/find_best_model pattern to load a checkpoint + its history JSON
and run inference standalone.

Why this exists (see cond_prior.py's docstring for the full background):
feed_coarse/roughness are causally downstream of the (DOC, speed) machining
condition -- a KNOWN, controlled parameter -- not merely confounded by it.
A model fit on the condition one-hot ALONE ("cond_only") already reaches a
strong accuracy with zero vibration signal; combining it with an image
model's probabilities via a WEIGHTED AVERAGE (not feature concatenation,
which dilutes the clean condition signal -- see cv_evaluate_32x3.py's
cond_hgb vs cond_stack results) can push accuracy further.

IMPORTANT caveat on what this script's numbers mean: under the "standard"
split (the only split any existing checkpoint was trained with), a test
run's (DOC, speed) condition is typically ALSO present in training (the
split is by class, not by condition -- a test run's sibling runs at the same
condition are usually in the training set). So the condition-prior number
here behaves close to a near-oracle per-condition lookup -- a different,
legitimate question from cv_evaluate_32x3.py's honest leave-one-condition-out
story, where the held-out condition is NEVER seen during training. Both are
valid answers to different questions; don't conflate this script's numbers
with cv_evaluate_32x3.py's LOCO numbers.

Usage (after training feed_coarse/roughness models with cnn_model/cnn_train_32x3.py):
    python stack_conditioning_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt
    python stack_conditioning_32x3.py --target roughness --img_dir scalograms_32x12 --cond_weight 0.8
    python stack_conditioning_32x3.py --target roughness --img_dir scalograms_32x3 --dry_run   # smoke-test, no checkpoint needed

Retrofitting across ALL existing checkpoints from a prior sweep: one call per
models_<target>_<scalo_tag>/ directory, accumulating a single comparable
stack_summary.csv (the analogue of cv_evaluate_32x3.py's cv_summary.csv). A
loop, not a built-in --all mode -- the models_<target>_<scalo_tag>/ <->
scalograms_<scalo_tag>/ directory-name mapping (base/_residual/_9win/_raw*w
variants) is error-prone to auto-discover; an explicit loop is auditable:

    for d in cnn_model/models_feed_coarse_*/ ; do
        tag=$(basename "$d")
        tag=${tag#models_feed_coarse_}
        python stack_conditioning_32x3.py --target feed_coarse --img_dir "scalograms_$tag"
    done
    for d in cnn_model/models_roughness_*/ ; do
        tag=$(basename "$d")
        tag=${tag#models_roughness_}
        python stack_conditioning_32x3.py --target roughness --img_dir "scalograms_$tag"
    done
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from PIL import Image

import cond_prior

ROOT = Path(__file__).parent
CNN_MODEL_DIR = ROOT / "cnn_model"


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod   # so the module's own internal imports resolve
    spec.loader.exec_module(mod)
    return mod


def find_best_plain_model(target: str, scalo_tag: str, run_tag: str, models_root: Path,
                           include_conditioned: bool):
    """Same globbing/max-run_level_acc pattern as predict_conditioning_32x3.py's
    find_best_model, but (by default) filters OUT conditioned/cascade_predicted
    checkpoints -- see this script's module docstring on why: the whole point
    is adding an EXTERNAL condition prior to a PURE-vibration backbone; a
    conditioned checkpoint already fuses the condition internally, so
    stacking a prior on top would double-count it. --include_conditioned
    overrides this filter for the explicit 'does external stacking add
    anything on top of internal fusion?' comparison."""
    model_dir = models_root / f"models_{target}_{scalo_tag}"
    suffix = f"_{run_tag}" if run_tag else ""
    if not model_dir.exists():
        raise FileNotFoundError(f"{model_dir} not found -- train {target} models first.")

    best = None
    for hist_path in model_dir.glob(f"*{suffix}_history.json"):
        with open(hist_path) as f:
            hist = json.load(f)
        if not include_conditioned and (hist.get("conditioned") or hist.get("cascade_predicted")):
            continue
        acc = hist.get("run_level_acc", 0.0)
        tag = hist_path.stem.replace("_history", "")
        model_path = model_dir / f"{tag}_best.pt"
        if not model_path.exists():
            continue
        if best is None or acc > best[2]:
            best = (model_path, hist, acc)
    if best is None:
        raise FileNotFoundError(
            f"No matching {target} checkpoints in {model_dir} (suffix='{suffix}', "
            f"include_conditioned={include_conditioned})."
        )
    model_path, hist, acc = best
    print(f"  Best model: {model_path.name}  (run_level_acc={acc:.3f}  "
          f"conditioned={hist.get('conditioned')}  cascade_predicted={hist.get('cascade_predicted')})")
    return model_path, hist


def load_run_images(img_dir: Path, target_runs: set, label_map: dict):
    """Globs img_dir for real run{N}_w{K}.png files belonging to target_runs
    (excludes smote*/synthetic samples -- those don't start with 'run')."""
    paths, labels, run_ids = [], [], []
    for p in sorted(img_dir.glob("run*_w*.png")):
        run = p.stem.split("_w")[0]
        if run in target_runs:
            paths.append(p)
            labels.append(label_map[run])
            run_ids.append(run)
    return paths, labels, run_ids


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                      description=__doc__)
    parser.add_argument("--target", required=True, choices=["feed_coarse", "roughness"],
                        help="Only these two targets have condition-prior signal "
                             "(feed_coarse/roughness are downstream of DOC x speed; "
                             "speed/doc themselves are the parents, nothing to stack).")
    parser.add_argument("--img_dir", required=True,
                        help="scalograms_32x3, scalograms_32x3_feedopt, or a _9win/_raw*w/_residual* variant")
    parser.add_argument("--run_tag", default="", help="Matches the --run_tag used to train candidates")
    parser.add_argument("--models_root", default=None,
                        help="Where cnn_train_32x3.py saved models_<target>_<scalo_tag>/ "
                             "(default: this script's directory)")
    parser.add_argument("--split", default="standard", choices=["standard", "balanced"],
                        help="Which TARGETS[target]['test_runs_*'] set this checkpoint was trained with")
    parser.add_argument("--cond_weight", type=float, default=0.7,
                        help="Primary weight reported for cond_weight*cond_probs + (1-cond_weight)*pixel_probs")
    parser.add_argument("--cond_weight_sweep", type=float, nargs="+",
                        default=[0.0, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                        help="Additional weights evaluated in the same run (cheap -- the CNN "
                             "forward pass only runs once, the sweep is pure numpy after that)")
    parser.add_argument("--include_conditioned", action="store_true",
                        help="Also consider conditioned/cascade_predicted checkpoints (off by "
                             "default -- see find_best_plain_model's docstring)")
    parser.add_argument("--dry_run", action="store_true",
                        help="Skip checkpoint loading entirely; substitute uniform pixel "
                             "probabilities so the rest of the pipeline (condition-prior fit, "
                             "weight sweep, CSV writing) can be smoke-tested without a .pt file")
    args = parser.parse_args()

    img_dir = ROOT / args.img_dir
    scalo_tag = img_dir.name.replace("scalograms_", "")
    models_root = Path(args.models_root) if args.models_root else ROOT
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}   Target: {args.target}   Img dir: {img_dir.name}   split={args.split}")

    cnn_train_32x3 = _load_module("cnn_train_32x3", CNN_MODEL_DIR / "cnn_train_32x3.py")
    spec = cnn_train_32x3.TARGETS[args.target]
    label_map = spec["label_map"]
    num_classes = spec["num_classes"]
    test_runs = set(spec["test_runs_balanced"] if args.split == "balanced" else spec["test_runs_standard"])
    train_runs = set(label_map.keys()) - test_runs

    te_paths, te_labels, te_run_ids = load_run_images(img_dir, test_runs, label_map)
    if not te_paths:
        raise FileNotFoundError(f"No test-run PNGs found in {img_dir} for {args.target}")

    cond_of = cond_prior.conditions_for_runs(label_map, cnn_train_32x3.DOC_LABELS, cnn_train_32x3.SPEED_LABELS)

    if args.dry_run:
        print("  [--dry_run] substituting uniform pixel probabilities, no checkpoint loaded")
        run_true = {r: label_map[r] for r in set(te_run_ids)}
        run_probs = {r: np.full(num_classes, 1.0 / num_classes) for r in run_true}
        model_tag = "DRY_RUN"
    else:
        model_path, hist = find_best_plain_model(args.target, scalo_tag, args.run_tag, models_root,
                                                   args.include_conditioned)
        arch, dropout = hist.get("arch", "resnet18"), hist.get("dropout", 0.0)
        conditioned = bool(hist.get("conditioned") or hist.get("cascade_predicted"))
        _, val_tf = cnn_train_32x3.build_transforms()

        if conditioned:
            model = cnn_train_32x3.ConditionedModel(
                arch, num_classes,
                [cnn_train_32x3.COND_DIMS["speed"], cnn_train_32x3.COND_DIMS["doc"]], dropout=dropout
            ).to(device)
        else:
            model = cnn_train_32x3.build_model(arch, num_classes, dropout=dropout).to(device)
        state = torch.load(model_path, map_location=device, weights_only=True)
        model.load_state_dict(state)

        cond_labels_list = None
        if conditioned:
            te_spd = [cnn_train_32x3.SPEED_LABELS[r] for r in te_run_ids]
            te_doc = [cnn_train_32x3.DOC_LABELS[r] for r in te_run_ids]
            cond_labels_list = [te_spd, te_doc]

        run_probs, run_true = cnn_train_32x3.run_prob_vectors(
            model, te_paths, te_labels, te_run_ids, val_tf, device, cond_labels_list)
        model_tag = model_path.stem.replace("_best", "")

    test_order = list(run_true)
    pixel_mat = np.stack([run_probs[r] for r in test_order])
    true_arr = np.array([run_true[r] for r in test_order])
    pixel_acc = float(np.mean(pixel_mat.argmax(1) == true_arr))

    # Fit at WINDOW level (one row per training window, not one per run) --
    # matching cv_evaluate_32x3.py's proven-working convention. Condition is
    # constant per run, so this repeats each run's condition n_windows times,
    # but that repetition matters in practice: HistGradientBoostingClassifier
    # defaults to min_samples_leaf=20, and with only ~33 RUN-level rows (one
    # per training run) it can't satisfy that anywhere and degenerates to
    # predicting the single overall-majority class for every test run
    # (confirmed while building this script -- run-level fitting gave exactly
    # chance accuracy, always predicting class 1). Window-level repetition
    # (~33 runs x 3-9 windows = 99-297 rows) gives it enough rows to split on.
    _, tr_labels_w, tr_run_ids_w = load_run_images(img_dir, train_runs, label_map)
    tr_conditions_w = [cond_of[r] for r in tr_run_ids_w]
    clf, classes_ = cond_prior.fit_condition_prior(tr_conditions_w, tr_labels_w, num_classes)
    cond_mat = cond_prior.predict_condition_prior(clf, classes_, [cond_of[r] for r in test_order], num_classes)
    cond_only_acc = float(np.mean(cond_mat.argmax(1) == true_arr))

    print(f"\nPixel-model-only run acc  : {pixel_acc:.3f}  ({len(test_order)} runs)")
    print(f"Condition-prior-only acc  : {cond_only_acc:.3f}")

    weights = sorted(set(args.cond_weight_sweep) | {args.cond_weight})
    rows = []
    for w in weights:
        stacked = cond_prior.stack_probs(cond_mat, pixel_mat, w)
        stack_acc = float(np.mean(stacked.argmax(1) == true_arr))
        marker = "  <-- --cond_weight" if w == args.cond_weight else ""
        print(f"  cond_weight={w:.2f}  stack_acc={stack_acc:.3f}{marker}")
        rows.append({
            "target": args.target, "img_dir": img_dir.name, "model_tag": model_tag,
            "split": args.split, "cond_weight": w,
            "pixel_run_acc": round(pixel_acc, 4), "cond_only_acc": round(cond_only_acc, 4),
            "stack_run_acc": round(stack_acc, 4), "n_runs": len(test_order),
        })

    out_path = ROOT / "stack_summary.csv"
    out = pd.DataFrame(rows)
    if out_path.exists():
        out = pd.concat([pd.read_csv(out_path), out], ignore_index=True)
    out.to_csv(out_path, index=False)
    print(f"\nWrote {len(rows)} rows -> {out_path.name}")


if __name__ == "__main__":
    main()
