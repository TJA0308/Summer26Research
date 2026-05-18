"""
Predict milling parameters from a raw CSV signal file.

Usage (run from project root):
    python cnn_model/predict.py --csv data/run1.csv --target speed
    python cnn_model/predict.py --csv data/run1.csv --target doc
    python cnn_model/predict.py --csv data/run1.csv --target feed_coarse
    python cnn_model/predict.py --csv data/run1.csv --target feed
"""
import argparse
from pathlib import Path

import pandas as pd
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

from scalogram import compute_powers, build_rgb_image
from scalogram import FS, DOWNSAMPLE, F_MIN, F_MAX, N_FREQS, SIGMA, IMG_SIZE, CHANNELS

# Models live in the project root (one level above this script's cnn_model/ folder)
_ROOT = Path(__file__).parent.parent

TARGETS = {
    "speed": {
        "classes": {0: "1500 rpm", 1: "2000 rpm", 2: "3000 rpm", 3: "4000 rpm", 4: "5000 rpm"},
        "model":   str(_ROOT / "model_speed.pt"),
        "windows": 1,
        "label":   "spindle speed",
    },
    "doc": {
        "classes": {0: "0.015 mm", 1: "0.030 mm", 2: "0.060 mm"},
        "model":   str(_ROOT / "model_doc.pt"),
        "windows": 1,
        "label":   "depth of cut",
    },
    "feed_coarse": {
        "classes": {0: "3-4 mm/rev (low)", 1: "5-6 mm/rev (medium)", 2: "7-8 mm/rev (high)"},
        "model":   str(_ROOT / "model_feed_coarse.pt"),
        "windows": 1,
        "label":   "feed rate (coarse)",
    },
    "feed": {
        "classes": {0: "3 mm/rev", 1: "4 mm/rev", 2: "5 mm/rev",
                    3: "6 mm/rev", 4: "7 mm/rev", 5: "8 mm/rev"},
        "model":   str(_ROOT / "model_feed.pt"),
        "windows": 4,
        "label":   "feed rate",
    },
    "roughness": {
        "classes": {0: "Smooth (Ra<0.7)", 1: "Medium (0.7-1.0)", 2: "Rough (Ra>1.0)"},
        "model":   str(_ROOT / "model_roughness.pt"),
        "windows": 1,
        "label":   "surface roughness",
    },
}


def load_model(model_path, num_classes, device):
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    model.load_state_dict(torch.load(model_path, map_location=device))
    return model.to(device).eval()


def csv_to_tensors(csv_path, n_windows):
    df     = pd.read_csv(csv_path)
    N      = len(df)
    fs_eff = FS // DOWNSAMPLE
    tf = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    window_size = N // 2
    hop         = max(1, (N - window_size) // (n_windows - 1)) if n_windows > 1 else N
    tensors = []
    for w in range(n_windows):
        start  = w * hop
        end    = start + window_size
        if end > N:
            end   = N
            start = max(0, end - window_size)
        df_win = df.iloc[start:end].reset_index(drop=True)
        powers = compute_powers(df_win, CHANNELS, fs_eff, F_MIN, F_MAX, N_FREQS, SIGMA, DOWNSAMPLE)
        img_np = build_rgb_image(powers, IMG_SIZE)
        tensors.append(tf(Image.fromarray(img_np)).unsqueeze(0))
    return tensors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv",    required=True,
                        help="Path to raw signal CSV (e.g. data/run1.csv)")
    parser.add_argument("--target", default="speed",
                        choices=list(TARGETS.keys()),
                        help="What to predict: speed, doc, feed_coarse, feed, or roughness")
    parser.add_argument("--model",  default=None,
                        help="Override model path (auto-selected by target if omitted)")
    args = parser.parse_args()

    cfg         = TARGETS[args.target]
    class_names = cfg["classes"]
    model_path  = args.model or cfg["model"]
    n_windows   = cfg["windows"]

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model  = load_model(model_path, len(class_names), device)

    print(f"Loading {args.csv} ...")
    tensors = csv_to_tensors(args.csv, n_windows)

    with torch.no_grad():
        all_probs = [torch.softmax(model(t.to(device)), dim=1).squeeze() for t in tensors]
        probs = torch.stack(all_probs).mean(dim=0)
        pred  = probs.argmax().item()

    print(f"\nPredicted {cfg['label']}: {class_names[pred]}")
    print("\nClass probabilities:")
    for cls, name in class_names.items():
        bar = "#" * int(probs[cls].item() * 40)
        print(f"  {name:>22}  {probs[cls].item():.3f}  {bar}")


if __name__ == "__main__":
    main()
