"""
Automated experiment runner for CWT+CNN accuracy maximization.
Tries many configurations for speed (35 train) and feed (39 train),
builds an ensemble from top models, and reports best accuracy.
"""

import subprocess
import sys
import re
import csv
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms

ROOT         = Path(__file__).parent.parent
TRAIN_SCRIPT = Path(__file__).parent / "cnn_train.py"
RESULTS_CSV  = ROOT / "experiment_results.csv"
MODELS_DIR   = ROOT / "exp_models"
MODELS_DIR.mkdir(exist_ok=True)

IMG_10W    = str(ROOT / "scalograms_10w")
IMG_10W_FI = str(ROOT / "scalograms_10w_fi")


# 6 focused experiments per target — most impactful configs, batch=16 for speed (~38 min/exp → ~4 hrs)
SPEED_EXPERIMENTS = [
    # ResNet18 baseline
    ("rn18_10w_adamw",
     ["--img_dir", IMG_10W, "--target", "speed", "--backbone", "resnet18",
      "--augment", "light", "--scheduler", "cosine", "--optimizer", "adamw",
      "--epochs", "20", "--lr", "1e-3", "--weight_decay", "1e-4", "--batch", "16"]),

    # EfficientNet-B0 — usually better than ResNet18 on small datasets
    ("effb0_10w_adamw",
     ["--img_dir", IMG_10W, "--target", "speed", "--backbone", "efficientnet_b0",
      "--augment", "light", "--scheduler", "cosine", "--optimizer", "adamw",
      "--epochs", "20", "--lr", "5e-4", "--weight_decay", "1e-4", "--batch", "16"]),

    # ConvNeXt-Tiny — modern architecture with good accuracy
    ("cnxt_10w_adamw",
     ["--img_dir", IMG_10W, "--target", "speed", "--backbone", "convnext_tiny",
      "--augment", "light", "--scheduler", "cosine", "--optimizer", "adamw",
      "--epochs", "20", "--lr", "5e-4", "--weight_decay", "1e-4", "--batch", "16"]),

    # EfficientNet-B0 + MixUp augmentation — regularizes small dataset
    ("effb0_10w_mixup_adamw",
     ["--img_dir", IMG_10W, "--target", "speed", "--backbone", "efficientnet_b0",
      "--augment", "light", "--scheduler", "cosine", "--optimizer", "adamw",
      "--epochs", "20", "--lr", "5e-4", "--weight_decay", "1e-4", "--batch", "16",
      "--mixup", "0.2"]),

    # EfficientNet-B0 + freq-interleave scalograms (different CWT view)
    ("effb0_10w_fi_adamw",
     ["--img_dir", IMG_10W_FI, "--target", "speed", "--backbone", "efficientnet_b0",
      "--augment", "light", "--scheduler", "cosine", "--optimizer", "adamw",
      "--epochs", "20", "--lr", "5e-4", "--weight_decay", "1e-4", "--batch", "16"]),

    # EfficientNet-B0 + both scalogram dirs merged (2× training data)
    ("effb0_both_adamw",
     ["--img_dir", IMG_10W, "--extra_img_dir", IMG_10W_FI, "--target", "speed",
      "--backbone", "efficientnet_b0", "--augment", "light", "--scheduler", "cosine",
      "--optimizer", "adamw", "--epochs", "20", "--lr", "5e-4", "--weight_decay", "1e-4",
      "--batch", "16"]),
]

FEED_COARSE_EXPERIMENTS = [
    ("rn18_10w_adamw",
     ["--img_dir", IMG_10W, "--target", "feed_coarse", "--backbone", "resnet18",
      "--augment", "light", "--scheduler", "cosine", "--optimizer", "adamw",
      "--epochs", "20", "--lr", "1e-3", "--weight_decay", "1e-4", "--batch", "16"]),

    ("effb0_10w_adamw",
     ["--img_dir", IMG_10W, "--target", "feed_coarse", "--backbone", "efficientnet_b0",
      "--augment", "light", "--scheduler", "cosine", "--optimizer", "adamw",
      "--epochs", "20", "--lr", "5e-4", "--weight_decay", "1e-4", "--batch", "16"]),

    ("cnxt_10w_adamw",
     ["--img_dir", IMG_10W, "--target", "feed_coarse", "--backbone", "convnext_tiny",
      "--augment", "light", "--scheduler", "cosine", "--optimizer", "adamw",
      "--epochs", "20", "--lr", "5e-4", "--weight_decay", "1e-4", "--batch", "16"]),

    ("effb0_10w_mixup_adamw",
     ["--img_dir", IMG_10W, "--target", "feed_coarse", "--backbone", "efficientnet_b0",
      "--augment", "light", "--scheduler", "cosine", "--optimizer", "adamw",
      "--epochs", "20", "--lr", "5e-4", "--weight_decay", "1e-4", "--batch", "16",
      "--mixup", "0.2"]),

    ("effb0_10w_fi_adamw",
     ["--img_dir", IMG_10W_FI, "--target", "feed_coarse", "--backbone", "efficientnet_b0",
      "--augment", "light", "--scheduler", "cosine", "--optimizer", "adamw",
      "--epochs", "20", "--lr", "5e-4", "--weight_decay", "1e-4", "--batch", "16"]),

    ("effb0_both_adamw",
     ["--img_dir", IMG_10W, "--extra_img_dir", IMG_10W_FI, "--target", "feed_coarse",
      "--backbone", "efficientnet_b0", "--augment", "light", "--scheduler", "cosine",
      "--optimizer", "adamw", "--epochs", "20", "--lr", "5e-4", "--weight_decay", "1e-4",
      "--batch", "16"]),
]

ROUGHNESS_EXPERIMENTS = [
    # Baseline ResNet18 + AdamW
    ("rn18_10w_adamw",
     ["--img_dir", IMG_10W, "--target", "roughness", "--backbone", "resnet18",
      "--augment", "light", "--scheduler", "cosine", "--optimizer", "adamw",
      "--epochs", "20", "--lr", "1e-3", "--weight_decay", "1e-4", "--batch", "16"]),

    # EfficientNet-B0 + AdamW (best performing architecture from speed experiments)
    ("effb0_10w_adamw",
     ["--img_dir", IMG_10W, "--target", "roughness", "--backbone", "efficientnet_b0",
      "--augment", "light", "--scheduler", "cosine", "--optimizer", "adamw",
      "--epochs", "20", "--lr", "5e-4", "--weight_decay", "1e-4", "--batch", "16"]),
]

FEED_EXPERIMENTS = [
    # ResNet18 baseline
    ("rn18_10w_adamw",
     ["--img_dir", IMG_10W, "--target", "feed", "--backbone", "resnet18",
      "--augment", "light", "--scheduler", "cosine", "--optimizer", "adamw",
      "--epochs", "20", "--lr", "1e-3", "--weight_decay", "1e-4", "--batch", "16"]),

    # EfficientNet-B0
    ("effb0_10w_adamw",
     ["--img_dir", IMG_10W, "--target", "feed", "--backbone", "efficientnet_b0",
      "--augment", "light", "--scheduler", "cosine", "--optimizer", "adamw",
      "--epochs", "20", "--lr", "5e-4", "--weight_decay", "1e-4", "--batch", "16"]),

    # ConvNeXt-Tiny
    ("cnxt_10w_adamw",
     ["--img_dir", IMG_10W, "--target", "feed", "--backbone", "convnext_tiny",
      "--augment", "light", "--scheduler", "cosine", "--optimizer", "adamw",
      "--epochs", "20", "--lr", "5e-4", "--weight_decay", "1e-4", "--batch", "16"]),

    # EfficientNet-B0 + MixUp
    ("effb0_10w_mixup_adamw",
     ["--img_dir", IMG_10W, "--target", "feed", "--backbone", "efficientnet_b0",
      "--augment", "light", "--scheduler", "cosine", "--optimizer", "adamw",
      "--epochs", "20", "--lr", "5e-4", "--weight_decay", "1e-4", "--batch", "16",
      "--mixup", "0.2"]),

    # EfficientNet-B0 + freq-interleave scalograms
    ("effb0_10w_fi_adamw",
     ["--img_dir", IMG_10W_FI, "--target", "feed", "--backbone", "efficientnet_b0",
      "--augment", "light", "--scheduler", "cosine", "--optimizer", "adamw",
      "--epochs", "20", "--lr", "5e-4", "--weight_decay", "1e-4", "--batch", "16"]),

    # EfficientNet-B0 + both dirs merged (2× training data)
    ("effb0_both_adamw",
     ["--img_dir", IMG_10W, "--extra_img_dir", IMG_10W_FI, "--target", "feed",
      "--backbone", "efficientnet_b0", "--augment", "light", "--scheduler", "cosine",
      "--optimizer", "adamw", "--epochs", "20", "--lr", "5e-4", "--weight_decay", "1e-4",
      "--batch", "16"]),
]


def run_experiment_capture(name, target, extra_args, save_path):
    cmd = [sys.executable, str(TRAIN_SCRIPT)] + extra_args + ["--save", str(save_path)]
    print(f"\n{'='*70}")
    print(f"  [{target.upper()}] {name}")
    print(f"  Save: {save_path.name}")
    print(f"{'='*70}", flush=True)
    t0 = time.time()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    lines = []
    for line in proc.stdout:
        print(line, end="", flush=True)
        lines.append(line)
    proc.wait()
    elapsed = time.time() - t0

    acc = None
    for line in reversed(lines):
        m = re.search(r"Best test accuracy:\s*([0-9.]+)", line)
        if m:
            acc = float(m.group(1))
            break
    return acc, elapsed


def load_model_for_inference(backbone, num_classes, model_path, device):
    sys.path.insert(0, str(Path(__file__).parent))
    from cnn_train import build_model
    model = build_model(backbone, num_classes, freeze_backbone=False)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    return model.to(device)


def ensemble_predict_tta(ensemble_models, test_paths, test_labels, device, n_aug=6):
    mean = [0.485, 0.456, 0.406]
    std  = [0.229, 0.224, 0.225]
    val_tf = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean, std)])
    tta_tf = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.15, contrast=0.15),
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])
    correct, n = 0, 0
    for path, label in zip(test_paths, test_labels):
        img = Image.open(path).convert("RGB")
        all_probs = []
        with torch.no_grad():
            for model, _ in ensemble_models:
                p_list = [F.softmax(model(val_tf(img).unsqueeze(0).to(device)), dim=1)]
                for _ in range(n_aug - 1):
                    p_list.append(F.softmax(model(tta_tf(img).unsqueeze(0).to(device)), dim=1))
                all_probs.append(torch.stack(p_list).mean(0))
        avg = torch.stack(all_probs).mean(0)
        correct += int(avg.argmax(1).item() == label)
        n += 1
    return correct / n if n > 0 else 0.0


def _parse_backbone(args_list):
    try:
        idx = args_list.index("--backbone")
        return args_list[idx + 1]
    except ValueError:
        return "resnet18"


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", choices=["speed", "feed", "feed_coarse", "roughness", "both"], default="both")
    parser.add_argument("--top_n", type=int, default=3)
    parser.add_argument("--skip_done", action="store_true", help="Skip if model file exists")
    parser.add_argument("--exp_start", type=int, default=0, help="Start index into experiment list (inclusive)")
    parser.add_argument("--exp_end",   type=int, default=None, help="End index (exclusive); omit for all remaining")
    parser.add_argument("--ensemble_only", action="store_true", help="Skip training, build ensemble from existing models")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    all_results = []
    targets_to_run = []
    if args.target in ("speed", "both"):
        targets_to_run.append(("speed", SPEED_EXPERIMENTS, 5))
    if args.target in ("feed", "both"):
        targets_to_run.append(("feed", FEED_EXPERIMENTS, 6))
    if args.target == "feed_coarse":
        targets_to_run.append(("feed_coarse", FEED_COARSE_EXPERIMENTS, 3))
    if args.target == "roughness":
        targets_to_run.append(("roughness", ROUGHNESS_EXPERIMENTS, 3))

    for target, experiments, num_classes in targets_to_run:
        exp_slice = experiments[args.exp_start:args.exp_end]
        print(f"\n{'#'*70}")
        print(f"  TARGET: {target.upper()} | running {len(exp_slice)} of {len(experiments)} experiments [idx {args.exp_start}:{args.exp_end}]")
        print(f"{'#'*70}")
        target_results = []

        for exp_name, exp_args in ([] if args.ensemble_only else exp_slice):
            save_path = MODELS_DIR / f"{target}_{exp_name}.pt"

            if args.skip_done and save_path.exists():
                print(f"  [SKIP] {exp_name} (model exists)")
                target_results.append({
                    "name": exp_name, "acc": None,
                    "path": save_path, "backbone": _parse_backbone(exp_args)
                })
                continue

            acc, elapsed = run_experiment_capture(exp_name, target, exp_args, save_path)
            backbone = _parse_backbone(exp_args)
            target_results.append({"name": exp_name, "acc": acc, "path": save_path, "backbone": backbone})
            all_results.append({"target": target, "name": exp_name, "acc": acc,
                                 "elapsed_s": round(elapsed), "path": str(save_path), "backbone": backbone})
            print(f"\n  >> {exp_name}: acc={acc}  ({elapsed:.0f}s)", flush=True)

        valid = [r for r in target_results if r["acc"] is not None]
        valid.sort(key=lambda x: x["acc"], reverse=True)

        print(f"\n{'-'*60}")
        print(f"  {target.upper()} RESULTS (ranked):")
        for i, r in enumerate(valid, 1):
            print(f"  {i:2d}. {r['name']:50s}  {r['acc']:.3f}")

        top = [r for r in valid[:args.top_n] if Path(str(r["path"])).exists()]
        if len(top) >= 2:
            print(f"\n  Building ensemble from top {len(top)} models for {target} …")
            sys.path.insert(0, str(Path(__file__).parent))
            from cnn_train import (
                SPEED_LABELS, SPEED_TEST_RUNS, FEED_LABELS, FEED_TEST_RUNS,
                FEED_COARSE_LABELS,
                RA_LABELS, RA_TEST_RUNS,
                load_split, load_smote_map
            )
            if target == "speed":
                label_map, test_runs = SPEED_LABELS, SPEED_TEST_RUNS
            elif target == "roughness":
                label_map, test_runs = RA_LABELS, RA_TEST_RUNS
            elif target == "feed_coarse":
                label_map, test_runs = FEED_COARSE_LABELS, FEED_TEST_RUNS
            else:
                label_map, test_runs = FEED_LABELS, FEED_TEST_RUNS

            img_dir = Path(IMG_10W)
            smote_csv = ("smote_speed_labels.csv"        if target == "speed"
                         else "smote_roughness_labels.csv"   if target == "roughness"
                         else "smote_feed_coarse_labels.csv" if target == "feed_coarse"
                         else "smote_labels.csv")
            smote_map = load_smote_map(img_dir, smote_csv)
            _, (te_p, te_l) = load_split(img_dir, label_map, test_runs, smote_map)

            ensemble_models = []
            for r in top:
                try:
                    m = load_model_for_inference(r["backbone"], num_classes, r["path"], device)
                    ensemble_models.append((m, r["name"]))
                except Exception as e:
                    print(f"  Warning: could not load {r['name']}: {e}")

            if ensemble_models:
                ens_tta_acc = ensemble_predict_tta(ensemble_models, te_p, te_l, device, n_aug=6)
                print(f"  Ensemble+TTA ({len(ensemble_models)} models): {ens_tta_acc:.3f}")
                all_results.append({"target": target, "name": f"ENSEMBLE_TOP{len(top)}_TTA",
                                     "acc": ens_tta_acc, "elapsed_s": 0,
                                     "path": "", "backbone": "ensemble"})

    if all_results:
        with open(RESULTS_CSV, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["target","name","acc","elapsed_s","path","backbone"])
            writer.writeheader()
            writer.writerows(all_results)
        print(f"\nResults saved to {RESULTS_CSV}")

    print(f"\n{'='*70}")
    print("  FINAL SUMMARY")
    print(f"{'='*70}")
    for tgt in ["speed", "feed"]:
        tr = [r for r in all_results if r.get("target") == tgt and r.get("acc") is not None]
        if tr:
            best = max(tr, key=lambda x: x["acc"])
            print(f"  {tgt.upper():6s}  best={best['acc']:.3f}  ({best['name']})")


if __name__ == "__main__":
    main()
