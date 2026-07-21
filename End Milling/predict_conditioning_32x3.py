"""
Finds the best already-trained speed or doc model (by run_level_acc in its
history JSON) for the 32x3 pipeline and runs it over every real window image
in a given scalogram directory, writing <target>_pred_32x3[...].csv so that
cnn_model/cnn_train_32x3.py's --cascade_predicted mode can condition feed_coarse
training on PREDICTED speed/doc instead of ground truth -- mirrors Shoulder
Milling's predict_conditioning.py.

Simpler than Shoulder Milling's version by construction: End Milling's
ConditionedResNet (cnn_model/cnn_train.py) only supports ONE cascade shape --
feed_coarse conditioned jointly on speed AND doc, both always present, never
a subset. So this script only ever predicts "speed" or "doc", never an
arbitrary COND_PARENTS list.

Note: predictions for images that were in this model's OWN training split are
inflated relative to genuinely held-out predictions. Accepted as a
simplification for this dataset's size, same caveat Shoulder Milling's
version documents -- worth revisiting if cascade gains look too good to be
true.

Usage (from this directory, after training speed/doc models with
cnn_model/cnn_train_32x3.py):
    python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x3
    python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x3_feedopt
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

import pandas as pd
import torch
from PIL import Image

ROOT = Path(__file__).parent
CNN_MODEL_DIR = ROOT / "cnn_model"


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod   # so the module's own internal imports resolve
    spec.loader.exec_module(mod)
    return mod


def find_best_model(target: str, scalo_tag: str, run_tag: str, models_root: Path):
    subdir = f"models_{target}_{scalo_tag}"
    suffix = f"_{run_tag}" if run_tag else ""
    search_dirs = [models_root / subdir]
    best = None
    for model_dir in search_dirs:
        if not model_dir.exists():
            continue
        for hist_path in model_dir.glob(f"*{suffix}_history.json"):
            with open(hist_path) as f:
                hist = json.load(f)
            acc = hist.get("run_level_acc", 0.0)
            tag = hist_path.stem.replace("_history", "")
            model_path = model_dir / f"{tag}_best.pt"
            if not model_path.exists():
                continue
            if best is None or acc > best[2]:
                best = (model_path, hist, acc)
    if best is None:
        raise FileNotFoundError(
            f"No trained {target} models found in {search_dirs} (suffix='{suffix}') -- "
            f"train them first with cnn_model/cnn_train_32x3.py --target {target}."
        )
    model_path, hist, acc = best
    print(f"  Best {target} model: {model_path.name}  (run_level_acc={acc:.3f})")
    return model_path, hist


@torch.no_grad()
def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                      description=__doc__)
    parser.add_argument("--target", required=True, choices=["speed", "doc"],
                        help="Which already-trained parent target to generate predictions for")
    parser.add_argument("--img_dir", required=True,
                        help="scalograms_32x3, scalograms_32x3_feedopt, or a _9win / _residual* variant")
    parser.add_argument("--run_tag", default="",
                        help="Matches the --run_tag used to train the candidate models")
    parser.add_argument("--models_root", default=None,
                        help="Where cnn_train_32x3.py saved models_<target>_<scalo_tag>/ "
                             "(default: this script's directory)")
    args = parser.parse_args()

    cnn_train_32x3 = _load_module("cnn_train_32x3", CNN_MODEL_DIR / "cnn_train_32x3.py")

    img_dir = ROOT / args.img_dir
    scalo_tag = img_dir.name.replace("scalograms_", "")
    models_root = Path(args.models_root) if args.models_root else ROOT
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    model_path, hist = find_best_model(args.target, scalo_tag, args.run_tag, models_root)
    num_classes = {"speed": 5, "doc": 3}[args.target]
    dropout = hist.get("dropout", 0.0)
    arch = hist.get("arch", "resnet18")

    model = cnn_train_32x3.build_model(arch, num_classes, dropout=dropout).to(device)
    state = torch.load(model_path, map_location=device, weights_only=True)
    model.load_state_dict(state)
    model.eval()

    _, val_tf = cnn_train_32x3.build_transforms()
    df = pd.read_csv(img_dir / "labels.csv")

    label_map = cnn_train_32x3.SPEED_LABELS if args.target == "speed" else cnn_train_32x3.DOC_LABELS

    rows, n_correct = [], 0
    for _, row in df.iterrows():
        path = img_dir / row.filename
        img = Image.open(path).convert("RGB")
        t = val_tf(img).unsqueeze(0).to(device)
        pred = model(t).argmax(1).item()
        true = label_map[row.run]
        n_correct += int(pred == true)
        rows.append({"filename": row.filename, "pred_label": pred})

    print(f"  Predictions match true label for {n_correct}/{len(rows)} of all real images "
          f"(includes this model's own train images, so expect this to read higher than "
          f"its real held-out run_level_acc of {hist.get('run_level_acc', float('nan')):.3f})")

    suffix = f"_{args.run_tag}" if args.run_tag else ""
    out_csv = img_dir / f"{args.target}_pred_{scalo_tag}{suffix}.csv"
    pd.DataFrame(rows).to_csv(out_csv, index=False)
    print(f"  Wrote {len(rows)} predictions -> {out_csv}")


if __name__ == "__main__":
    main()
