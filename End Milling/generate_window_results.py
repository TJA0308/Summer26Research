"""
Window-level inference dump for confusion-matrix analysis.

For every trained `_best.pt` checkpoint under cnn_model/models_<target>_<scalo_tag>*/,
re-runs inference on that model's held-out TEST windows and writes a per-window
CSV (filename, run, true_label, pred_label, prob_0..prob_k-1) next to the
checkpoint as `<stem>_window_preds.csv`. This is the raw material for a
window-level confusion matrix -- as opposed to *_history.json, which only has
per-epoch aggregate loss/accuracy, and the run-level accuracy already printed
during training.

Usage:
    python generate_window_results.py                     # all targets/dirs
    python generate_window_results.py --target feed_coarse
    python generate_window_results.py --only_missing       # skip if CSV exists
"""
import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "cnn_model"))

from cnn_train_32x3 import (   # noqa: E402
    TARGETS, COND_PARENTS, SPEED_LABELS, DOC_LABELS,
    build_transforms, build_model, ConditionedModel,
    load_split, load_split_conditioned, load_smote_map, load_predicted_conditioning,
    run_ids_from_paths,
)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
COND_DIMS = {"speed": 5, "doc": 3}


@torch.no_grad()
def infer_probs(model, paths, val_tf, cond_labels_list=None):
    from cnn_train_32x3 import ScalogramDataset, ConditionedScalogramDataset
    from torch.utils.data import DataLoader
    dummy_labels = [0] * len(paths)
    if cond_labels_list is not None:
        ds = ConditionedScalogramDataset(paths, dummy_labels, cond_labels_list[0], cond_labels_list[1], val_tf)
        dl = DataLoader(ds, batch_size=16, shuffle=False, num_workers=0)
        all_probs = []
        for imgs, _lbls, spd, doc in dl:
            probs = torch.softmax(model(imgs.to(DEVICE), spd.to(DEVICE), doc.to(DEVICE)), dim=1).cpu().numpy()
            all_probs.append(probs)
    else:
        ds = ScalogramDataset(paths, dummy_labels, val_tf)
        dl = DataLoader(ds, batch_size=16, shuffle=False, num_workers=0)
        all_probs = []
        for imgs, _ in dl:
            probs = torch.softmax(model(imgs.to(DEVICE)), dim=1).cpu().numpy()
            all_probs.append(probs)
    return np.concatenate(all_probs, axis=0)


def process_model_dir(model_dir: Path, target: str, only_missing: bool):
    spec = TARGETS[target]
    scalo_tag = model_dir.name.replace(f"models_{target}_", "")
    img_dir = HERE / f"scalograms_{scalo_tag}"
    if not img_dir.exists():
        print(f"  skip {model_dir.name}: img_dir {img_dir} missing")
        return

    _, val_tf = build_transforms()
    hist_files = sorted(model_dir.glob("*_history.json"))
    if not hist_files:
        return

    for hist_path in hist_files:
        stem = hist_path.name.replace("_history.json", "")
        pt_path = model_dir / f"{stem}_best.pt"
        out_csv = model_dir / f"{stem}_window_preds.csv"
        if not pt_path.exists():
            continue
        if only_missing and out_csv.exists():
            continue

        hist = json.loads(hist_path.read_text())
        conditioned = hist.get("conditioned", False)
        cascade_predicted = hist.get("cascade_predicted", False)
        run_tag = hist.get("run_tag", "") or ""
        split = hist.get("split", "standard")
        cascading = conditioned or cascade_predicted
        test_runs = spec["test_runs_balanced"] if split == "balanced" else spec["test_runs_standard"]

        try:
            if cascading:
                _, (te_p, te_l, te_spd, te_doc) = load_split_conditioned(
                    img_dir, spec["label_map"], test_runs, SPEED_LABELS, DOC_LABELS)
                if cascade_predicted:
                    for parent, arr in (("speed", te_spd), ("doc", te_doc)):
                        pred_te = load_predicted_conditioning(img_dir, parent, te_p, scalo_tag, run_tag)
                        if pred_te is None:
                            raise FileNotFoundError(f"{parent}_pred_{scalo_tag}_{run_tag}.csv missing")
                        arr[:] = pred_te
                model = ConditionedModel(hist["arch"], spec["num_classes"],
                                          [COND_DIMS["speed"], COND_DIMS["doc"]],
                                          dropout=hist.get("dropout", 0.15)).to(DEVICE)
                state = torch.load(pt_path, map_location=DEVICE, weights_only=False)
                model.load_state_dict(state)
                model.eval()
                probs = infer_probs(model, te_p, val_tf, cond_labels_list=[te_spd, te_doc])
            else:
                _, (te_p, te_l) = load_split(img_dir, spec["label_map"], test_runs, {})
                model = build_model(hist["arch"], spec["num_classes"],
                                     dropout=hist.get("dropout", 0.15)).to(DEVICE)
                state = torch.load(pt_path, map_location=DEVICE, weights_only=False)
                model.load_state_dict(state)
                model.eval()
                probs = infer_probs(model, te_p, val_tf)
        except Exception as e:
            print(f"  FAILED {model_dir.name}/{stem}: {e}")
            continue

        run_ids = run_ids_from_paths(te_p)
        preds = probs.argmax(axis=1)
        rows = []
        for i, p in enumerate(te_p):
            row = {
                "filename": Path(p).name, "run": run_ids[i],
                "true_label": te_l[i], "pred_label": int(preds[i]),
            }
            for c in range(spec["num_classes"]):
                row[f"prob_{c}"] = round(float(probs[i, c]), 6)
            rows.append(row)
        pd.DataFrame(rows).to_csv(out_csv, index=False)
        n_correct = int((preds == np.array(te_l)).sum())
        print(f"  {model_dir.name}/{stem}: wrote {len(rows)} window preds "
              f"({n_correct}/{len(rows)} window-level correct) -> {out_csv.name}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default=None, choices=list(TARGETS.keys()))
    parser.add_argument("--only_missing", action="store_true",
                         help="Skip model dirs that already have a *_window_preds.csv")
    args = parser.parse_args()

    targets = [args.target] if args.target else list(TARGETS.keys())
    for target in targets:
        pattern = f"models_{target}_*"
        dirs = sorted((HERE / "cnn_model").glob(pattern))
        # exclude e.g. models_feed_coarse_* matching models_feed_* prefix collisions
        dirs = [d for d in dirs if re.match(rf"^models_{re.escape(target)}(_|$)", d.name)]
        print(f"\n=== {target}: {len(dirs)} model dirs ===")
        for d in dirs:
            process_model_dir(d, target, args.only_missing)


if __name__ == "__main__":
    main()
