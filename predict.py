"""
Predict spindle speed from a raw CSV signal file.

Usage:
    python predict.py --csv data/run1.csv
    python predict.py --csv data/run1.csv --model best_model.pt
"""
import argparse

import pandas as pd
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

from scalogram import compute_powers, build_rgb_image
from scalogram import FS, DOWNSAMPLE, F_MIN, F_MAX, N_FREQS, SIGMA, IMG_SIZE, CHANNELS

SPEED_NAMES = {0: "1500 rpm", 1: "2000 rpm", 2: "3000 rpm", 3: "4000 rpm", 4: "5000 rpm"}
FEED_NAMES  = {0: "low feed", 1: "medium feed", 2: "high feed"}
DOC_NAMES   = {0: "0.015 mm", 1: "0.03 mm", 2: "0.06 mm"}


def load_model(model_path, device, num_classes):
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    return model


def csv_to_tensors(csv_path):
    """Generate one tensor per window, matching scalogram.py --n_windows 2."""
    df     = pd.read_csv(csv_path)
    N      = len(df)
    fs_eff = FS // DOWNSAMPLE
    tf = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    window_size = N // 2
    hop         = N // 4
    tensors = []
    for w in range(2):
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
    parser.add_argument("--csv",    required=True, help="Path to raw signal CSV")
    parser.add_argument("--target", default="speed", choices=["speed", "feed", "doc"],
                        help="Prediction target: speed, feed rate, or depth of cut")
    parser.add_argument("--model",  default=None, help="Path to saved model weights (auto-selected by target if omitted)")
    args = parser.parse_args()

    if args.target == "feed":
        class_names = FEED_NAMES
        num_classes = 3
        model_path  = args.model or "best_model_feed.pt"
        label       = "feed rate"
    elif args.target == "doc":
        class_names = DOC_NAMES
        num_classes = 3
        model_path  = args.model or "best_model_doc.pt"
        label       = "depth of cut"
    else:
        class_names = SPEED_NAMES
        num_classes = 5
        model_path  = args.model or "best_model.pt"
        label       = "speed"

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model  = load_model(model_path, device, num_classes)

    print(f"Loading {args.csv} ...")
    tensors = csv_to_tensors(args.csv)

    with torch.no_grad():
        all_probs = [torch.softmax(model(t.to(device)), dim=1).squeeze() for t in tensors]
        probs = torch.stack(all_probs).mean(dim=0)
        pred  = probs.argmax().item()

    print(f"\nPredicted {label} : {class_names[pred]}")
    print("\nClass probabilities:")
    for cls, name in class_names.items():
        bar = "#" * int(probs[cls].item() * 40)
        print(f"  {name:>12}  {probs[cls].item():.3f}  {bar}")


if __name__ == "__main__":
    main()
