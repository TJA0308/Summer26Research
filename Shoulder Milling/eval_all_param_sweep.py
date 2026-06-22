"""
Runs eval_detailed_param.py's per-window evaluation for all 48
cnn_train_param.py model combinations (3 targets x 2 scalogram dirs x
4 backbones x 2 learning rates), writing one detailed Markdown breakdown
per model into exp_results_<scalo_tag>/ plus a combined summary CSV.

Mirrors run_all_param_sweep.py's combo list, but reads already-trained
checkpoints instead of training -- run run_all_param_sweep.py (or the
individual cnn_train_param.py commands) first.

Usage (from this directory, after training):
    python eval_all_param_sweep.py
"""
import csv
from pathlib import Path

import torch

from eval_detailed_param import TARGETS, eval_one

TARGETS_LIST = list(TARGETS.keys())          # speed, feed, doc
IMG_DIRS     = ["scalograms_32x12", "scalograms_32x3"]
ARCHS        = ["resnet18", "resnet50", "efficientnet_b0", "convnext_tiny"]
LRS          = [1e-3, 1e-4]

HERE = Path(__file__).parent


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}\n")

    rows = []
    for target in TARGETS_LIST:
        for img_dir_name in IMG_DIRS:
            scalo_tag = img_dir_name.replace("scalograms_", "")
            img_dir   = HERE / img_dir_name
            for arch in ARCHS:
                for lr in LRS:
                    subdir = f"models_{target}_{scalo_tag}"
                    model_path = HERE / "models" / subdir / f"{arch}_lr{lr:g}_best.pt"
                    if not model_path.exists():
                        model_path = HERE / subdir / f"{arch}_lr{lr:g}_best.pt"
                    if not model_path.exists():
                        print(f"[skip] missing model: {model_path}")
                        rows.append({"target": target, "scalogram": scalo_tag, "arch": arch,
                                     "lr": lr, "window_acc": None, "run_acc": None, "status": "missing"})
                        continue

                    save_md = HERE / f"exp_results_{scalo_tag}" / f"{target}_{arch}_lr{lr:g}.md"
                    print(f"[eval] {model_path.relative_to(HERE)}")
                    try:
                        results, _ = eval_one(model_path, target, img_dir, arch,
                                               device=device, save_md=save_md, verbose=False)
                    except Exception as e:
                        print(f"  FAILED: {e}")
                        rows.append({"target": target, "scalogram": scalo_tag, "arch": arch,
                                     "lr": lr, "window_acc": None, "run_acc": None, "status": "failed"})
                        continue

                    n_runs, n_correct = len(results), sum(r["correct"] for r in results)
                    all_preds  = [p for r in results for p in r["window_preds"]]
                    all_labels = [r["true_label"] for r in results for _ in r["window_preds"]]
                    win_acc = sum(p == l for p, l in zip(all_preds, all_labels)) / len(all_preds)
                    run_acc = n_correct / n_runs
                    rows.append({"target": target, "scalogram": scalo_tag, "arch": arch, "lr": lr,
                                 "window_acc": round(win_acc, 4), "run_acc": round(run_acc, 4), "status": "ok"})
                    print(f"  window_acc={win_acc:.3f}  run_acc={run_acc:.3f} ({n_correct}/{n_runs})  -> {save_md.name}")

    out_csv = HERE / "eval_param_sweep_summary.csv"
    with open(out_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["target", "scalogram", "arch", "lr", "window_acc", "run_acc", "status"])
        writer.writeheader()
        writer.writerows(rows)

    n_ok = sum(1 for r in rows if r["status"] == "ok")
    print(f"\n{n_ok}/{len(rows)} models evaluated. Summary written to {out_csv}")


if __name__ == "__main__":
    main()
