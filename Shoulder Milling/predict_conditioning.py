"""
Finds the best already-trained model for a given target+pipeline (by
run_level_acc in its history JSON) and runs it over ALL 72 images in that
scalogram directory, writing <target>_pred_<scalo>[_<run_tag>].csv so that
downstream targets (doc conditions on speed; feed conditions on speed+doc)
can load real model predictions as an extra input -- see cnn_train_param.py's
COND_PARENTS / load_conditioning().

Picks the single best model across all 4 backbones x 2 LRs for the pipeline,
rather than predicting once per backbone/LR -- see cnn_train_param.py's
module docstring for why (avoids propagating a known-unstable backbone
config's bad predictions into every downstream model).

Note: predictions for images that were in this model's OWN training split
are inflated (the model has seen/memorized them) relative to its predictions
for images that were genuinely held out as its test set. With this dataset's
size that's accepted as a simplification rather than doing full
cross-validated out-of-fold prediction -- worth revisiting if cascade gains
look too good to be true.

Usage (from this directory, after training all 8 arch x lr combos for a target):
    python predict_conditioning.py --target speed --img_dir scalograms_32x12
    python predict_conditioning.py --target doc   --img_dir scalograms_32x3 --run_tag cascade
"""
import argparse
import json
from pathlib import Path

import pandas as pd
import torch
from PIL import Image

from cnn_train_param import TARGETS, COND_DIMS, COND_PARENTS, build_model, build_transforms, label_for, load_conditioning, ConditionedModel

ARCHS = ["resnet18", "resnet50", "efficientnet_b0", "convnext_tiny"]
LRS   = [1e-3, 1e-4]
ROOT  = Path(__file__).parent


def find_best_model(target, scalo_tag, run_tag):
    """Returns (model_path, history_dict, arch) for the highest run_level_acc
    model among the already-trained arch x lr combos for this target+pipeline.
    Searches both the consolidated models/<subdir>/ location and the top-level
    <subdir>/ location so experimental-split models (not consolidated) are found."""
    subdir = f"models_{target}_{scalo_tag}"
    suffix = f"_{run_tag}" if run_tag else ""
    search_dirs = [ROOT / "models" / subdir, ROOT / subdir]
    best = None
    for model_dir in search_dirs:
        if not model_dir.exists():
            continue
        for arch in ARCHS:
            for lr in LRS:
                tag = f"{arch}_lr{lr:g}{suffix}"
                hist_path = model_dir / f"{tag}_history.json"
                if not hist_path.exists():
                    continue
                with open(hist_path) as f:
                    hist = json.load(f)
                acc = hist.get("run_level_acc", 0.0)
                if best is None or acc > best[2]:
                    best = (model_dir / f"{tag}_best.pt", hist, acc, arch)
    if best is None:
        raise FileNotFoundError(
            f"No trained {target} models found in {search_dirs} (suffix='{suffix}') -- train them first."
        )
    model_path, hist, acc, arch = best
    print(f"  Best {target} model: {model_path.name}  (run_level_acc={acc:.3f})")
    return model_path, hist, arch


@torch.no_grad()
def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--target",  required=True, choices=["speed", "doc"],
                        help="Which already-trained target to generate predictions for")
    parser.add_argument("--img_dir", required=True, help="scalograms_32x12 or scalograms_32x3")
    parser.add_argument("--run_tag", default="",
                        help="Matches the --run_tag used to train the candidate models")
    args = parser.parse_args()

    img_dir   = ROOT / args.img_dir
    scalo_tag = img_dir.name.replace("scalograms_", "")
    device    = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    model_path, hist, arch = find_best_model(args.target, scalo_tag, args.run_tag)
    spec = TARGETS[args.target]

    state   = torch.load(model_path, map_location=device, weights_only=True)
    dropout = hist.get("dropout", 0.0)
    cond_parents = hist.get("cond_parents", [])

    # Detect conditioned checkpoint from state dict keys
    state_is_conditioned = any(k.startswith("base.") or k.startswith("backbone.") for k in state)
    if state_is_conditioned:
        cond_dims = [COND_DIMS[p] for p in cond_parents] if cond_parents else [COND_DIMS.get(args.target, 2)]
        model = ConditionedModel(arch, spec["num_classes"], cond_dims, dropout=dropout).to(device)
    else:
        model = build_model(arch, spec["num_classes"], dropout=dropout).to(device)
    model.load_state_dict(state)
    model.eval()

    _, val_tf = build_transforms()
    df = pd.read_csv(img_dir / "labels.csv")

    # Load parent conditioning values if model is conditioned
    all_paths = [img_dir / row.filename for _, row in df.iterrows()]
    cond_map = None
    if state_is_conditioned and cond_parents:
        per_parent = []
        for parent in cond_parents:
            vals = load_conditioning(img_dir, parent, all_paths, args.run_tag)
            if vals is None:
                raise RuntimeError(
                    f"Model is conditioned on '{parent}' but the conditioning CSV is missing -- "
                    f"run predict_conditioning.py for '{parent}' first."
                )
            per_parent.append(vals)
        cond_map = {p: [pv[i] for pv in per_parent] for i, p in enumerate(all_paths)}

    rows, n_correct = [], 0
    for i, (_, row) in enumerate(df.iterrows()):
        path = img_dir / row.filename
        img  = Image.open(path).convert("RGB")
        t    = val_tf(img).unsqueeze(0).to(device)
        if cond_map is not None:
            conds = [torch.tensor([v], device=device) for v in cond_map[path]]
            pred  = model(t, *conds).argmax(1).item()
        else:
            pred = model(t).argmax(1).item()
        true = label_for(args.target, row.side, row.feed)
        n_correct += int(pred == true)
        rows.append({"filename": row.filename, "pred_label": pred})

    print(f"  Predictions match true label for {n_correct}/{len(rows)} of all images "
          f"(includes this model's own train images, so expect this to read higher than "
          f"its real held-out test accuracy of {hist.get('run_level_acc', float('nan')):.3f})")

    suffix  = f"_{args.run_tag}" if args.run_tag else ""
    out_csv = img_dir / f"{args.target}_pred_{scalo_tag}{suffix}.csv"
    pd.DataFrame(rows).to_csv(out_csv, index=False)
    print(f"  Wrote {len(rows)} predictions -> {out_csv}")


if __name__ == "__main__":
    main()
