"""
Training curve visualiser.

Reads all *_history.json files in exp_models/ and produces:
  plots/<pipeline>_<target>_acc.png   — test & train accuracy per backbone
  plots/<pipeline>_<target>_loss.png  — test & train loss per backbone
  plots/summary_best_acc.png          — bar chart of best test accuracy
  plots/pipeline_comparison.png       — Pipeline A vs B for every target

Usage:
    python plot_training_curves.py
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# ── Config ─────────────────────────────────────────────────────────────────
BACKBONES = ["rn18", "rn50", "enb0", "cnxt"]
BB_LABEL  = {"rn18": "ResNet18", "rn50": "ResNet50",
             "enb0": "EfficientNet-B0", "cnxt": "ConvNeXt-Tiny"}
LRS       = ["lr1e3", "lr1e4"]
LR_LABEL  = {"lr1e3": "lr=1e-3", "lr1e4": "lr=1e-4"}
TARGETS   = ["speed", "doc", "roughness", "feed"]
TGT_LABEL = {"speed":     "Speed (5-class, 30 ep)",
             "doc":       "DOC (3-class, 33 ep)",
             "roughness": "Roughness (3-class, 33 ep)",
             "feed":      "Feed Coarse (3-class, 33 ep)"}
PIPELINES = ["std", "ses"]
PL_LABEL  = {"std": "Pipeline A — Std CWT", "ses": "Pipeline B — SES 4-ch"}

# Colours: one per backbone, shade per LR
BB_COLOR  = {"rn18": "#4C72B0", "rn50": "#DD8452",
             "enb0": "#55A868", "cnxt": "#C44E52"}
LR_ALPHA  = {"lr1e3": 1.0,  "lr1e4": 0.55}
LR_DASH   = {"lr1e3": "-",  "lr1e4": "--"}

BASE_DIR  = Path("exp_models")
OUT_DIR   = Path("plots")


# ── Helpers ────────────────────────────────────────────────────────────────

def load(pipeline, target, backbone, lr):
    p = BASE_DIR / f"{pipeline}_{target}_{backbone}_{lr}_history.json"
    if not p.exists():
        return None
    with open(p) as f:
        return json.load(f)


def _fmt_pct(x, _):
    return f"{x:.0%}"


# ── 1. Per-target accuracy + loss curves (2 figures per target) ────────────

def make_acc_figure(pipeline, target):
    fig, axes = plt.subplots(2, 2, figsize=(13, 9), sharey=True)
    fig.suptitle(f"{PL_LABEL[pipeline]}  ·  {TGT_LABEL[target]}",
                 fontsize=13, fontweight="bold")

    for ax, bb in zip(axes.flatten(), BACKBONES):
        ax.set_title(BB_LABEL[bb], fontsize=11)
        ax.set_xlabel("Epoch", fontsize=9)
        ax.set_ylabel("Accuracy", fontsize=9)
        ax.set_ylim(-0.02, 1.07)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_pct))
        ax.grid(True, alpha=0.25)
        ax.axhline(1.0, color="grey", lw=0.7, ls=":")

        for lr in LRS:
            d = load(pipeline, target, bb, lr)
            if d is None:
                continue
            h = d["history"]
            ep = range(1, len(h["train_acc"]) + 1)
            best = max(h["test_acc"])
            col  = BB_COLOR[bb]
            al   = LR_ALPHA[lr]
            # train (thin solid, muted)
            ax.plot(ep, h["train_acc"], color=col, lw=1.0, alpha=al * 0.4, ls="-")
            # test (thick, labelled)
            ax.plot(ep, h["test_acc"],  color=col, lw=1.8, alpha=al,
                    ls=LR_DASH[lr],
                    label=f"{LR_LABEL[lr]}  best={best:.1%}")

        ax.legend(fontsize=8, loc="lower right")

    # Legend for train vs test line style
    from matplotlib.lines import Line2D
    handles = [Line2D([0], [0], color="grey", lw=1.2, alpha=0.4, ls="-",  label="train acc (thin)"),
               Line2D([0], [0], color="grey", lw=1.8, ls="-",             label="test acc (solid=lr1e-3)"),
               Line2D([0], [0], color="grey", lw=1.8, ls="--",            label="test acc (dash=lr1e-4)")]
    fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=8,
               bbox_to_anchor=(0.5, -0.01))

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    out = OUT_DIR / f"{pipeline}_{target}_acc.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  saved {out}")


def make_loss_figure(pipeline, target):
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle(f"{PL_LABEL[pipeline]}  ·  {TGT_LABEL[target]}  — Loss",
                 fontsize=13, fontweight="bold")

    for ax, bb in zip(axes.flatten(), BACKBONES):
        ax.set_title(BB_LABEL[bb], fontsize=11)
        ax.set_xlabel("Epoch", fontsize=9)
        ax.set_ylabel("Cross-entropy loss", fontsize=9)
        ax.grid(True, alpha=0.25)

        all_losses = []
        for lr in LRS:
            d = load(pipeline, target, bb, lr)
            if d is None:
                continue
            h = d["history"]
            ep  = range(1, len(h["train_loss"]) + 1)
            col = BB_COLOR[bb]
            al  = LR_ALPHA[lr]
            ax.plot(ep, h["train_loss"], color=col, lw=1.0, alpha=al * 0.4, ls="-")
            ax.plot(ep, h["test_loss"],  color=col, lw=1.8, alpha=al,
                    ls=LR_DASH[lr], label=LR_LABEL[lr])
            all_losses += h["train_loss"] + h["test_loss"]

        if all_losses:
            # Cap y-axis so a single blown-up run (ConvNeXt lr1e3) doesn't crush others
            p95 = np.percentile(all_losses, 95)
            ax.set_ylim(0, min(max(all_losses) * 1.05, p95 * 2.5))

        ax.legend(fontsize=8)

    from matplotlib.lines import Line2D
    handles = [Line2D([0], [0], color="grey", lw=1.0, alpha=0.4, ls="-",  label="train loss"),
               Line2D([0], [0], color="grey", lw=1.8, ls="-",             label="test loss (solid=lr1e-3)"),
               Line2D([0], [0], color="grey", lw=1.8, ls="--",            label="test loss (dash=lr1e-4)")]
    fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=8,
               bbox_to_anchor=(0.5, -0.01))

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    out = OUT_DIR / f"{pipeline}_{target}_loss.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  saved {out}")


# ── 2. Summary bar chart — best test accuracy for all 64 configs ───────────

def make_summary():
    fig, axes = plt.subplots(len(TARGETS), len(PIPELINES),
                             figsize=(14, 4 * len(TARGETS)), sharey=True)
    fig.suptitle("Best Test Accuracy — All 64 Configurations",
                 fontsize=14, fontweight="bold")

    hatch_map = {"lr1e3": "", "lr1e4": "///"}
    x = np.arange(len(BACKBONES))
    width = 0.35

    for row, target in enumerate(TARGETS):
        for col, pipeline in enumerate(PIPELINES):
            ax = axes[row][col]
            ax.set_title(f"{PL_LABEL[pipeline]}\n{TGT_LABEL[target]}", fontsize=9)
            ax.set_ylim(0, 1.10)
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_pct))
            ax.axhline(1.0, color="grey", lw=0.6, ls="--", alpha=0.4)
            ax.grid(True, axis="y", alpha=0.25)
            ax.set_xticks(x)
            ax.set_xticklabels([BB_LABEL[b] for b in BACKBONES],
                               rotation=25, ha="right", fontsize=8)

            for i, lr in enumerate(LRS):
                vals = []
                for bb in BACKBONES:
                    d = load(pipeline, target, bb, lr)
                    vals.append(max(d["history"]["test_acc"]) if d else 0.0)
                offset = (i - 0.5) * width
                bars = ax.bar(x + offset, vals, width,
                              color=[BB_COLOR[b] for b in BACKBONES],
                              hatch=hatch_map[lr], alpha=0.85,
                              edgecolor="white", linewidth=0.5,
                              label=LR_LABEL[lr])
                for bar, v in zip(bars, vals):
                    if v > 0:
                        ax.text(bar.get_x() + bar.get_width() / 2,
                                bar.get_height() + 0.012,
                                f"{v:.0%}", ha="center", va="bottom", fontsize=6.5)

            if row == 0 and col == 0:
                ax.legend(fontsize=8, loc="lower left")

    # Backbone colour legend
    from matplotlib.patches import Patch
    bb_handles = [Patch(color=BB_COLOR[b], label=BB_LABEL[b]) for b in BACKBONES]
    fig.legend(handles=bb_handles, loc="lower center", ncol=4, fontsize=9,
               bbox_to_anchor=(0.5, -0.01), title="Backbone colour")

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    out = OUT_DIR / "summary_best_acc.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  saved {out}")


# ── 3. Pipeline A vs B comparison — test accuracy side by side ─────────────

def make_pipeline_comparison():
    """One figure per target: 4 subplots (one per backbone), each showing
    both pipelines and both LRs as four test-accuracy curves."""
    for target in TARGETS:
        fig, axes = plt.subplots(2, 2, figsize=(13, 9), sharey=True)
        fig.suptitle(f"Pipeline A vs B  ·  {TGT_LABEL[target]}  — Test Accuracy",
                     fontsize=13, fontweight="bold")

        pl_color  = {"std": "#1f77b4", "ses": "#d62728"}
        pl_ls     = {"std": "-", "ses": "--"}

        for ax, bb in zip(axes.flatten(), BACKBONES):
            ax.set_title(BB_LABEL[bb], fontsize=11)
            ax.set_xlabel("Epoch", fontsize=9)
            ax.set_ylabel("Test Accuracy", fontsize=9)
            ax.set_ylim(-0.02, 1.07)
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_pct))
            ax.grid(True, alpha=0.25)
            ax.axhline(1.0, color="grey", lw=0.7, ls=":")

            for pipeline in PIPELINES:
                for lr in LRS:
                    d = load(pipeline, target, bb, lr)
                    if d is None:
                        continue
                    h    = d["history"]
                    ep   = range(1, len(h["test_acc"]) + 1)
                    best = max(h["test_acc"])
                    col  = pl_color[pipeline]
                    al   = LR_ALPHA[lr]
                    ax.plot(ep, h["test_acc"], color=col, lw=1.6, alpha=al,
                            ls=pl_ls[pipeline] if lr == "lr1e3" else ":",
                            label=f"{PL_LABEL[pipeline].split('—')[0].strip()}  {LR_LABEL[lr]}  {best:.1%}")

            ax.legend(fontsize=7, loc="lower right")

        plt.tight_layout()
        out = OUT_DIR / f"pipelinecomp_{target}.png"
        fig.savefig(out, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  saved {out}")


# ── 4. Overfit gap chart — final train vs test acc ─────────────────────────

def make_overfit_chart():
    """Scatter: final train acc (x) vs best test acc (y) for every config."""
    fig, axes = plt.subplots(1, len(TARGETS), figsize=(16, 5), sharey=True)
    fig.suptitle("Overfitting Gap — Final Train Acc vs Best Test Acc",
                 fontsize=13, fontweight="bold")

    for ax, target in zip(axes, TARGETS):
        ax.set_title(TGT_LABEL[target], fontsize=10)
        ax.set_xlabel("Final Train Acc", fontsize=9)
        ax.set_ylabel("Best Test Acc", fontsize=9)
        ax.set_xlim(0.5, 1.05)
        ax.set_ylim(0.4, 1.05)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(_fmt_pct))
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_pct))
        ax.plot([0, 1], [0, 1], "k--", lw=0.7, alpha=0.4, label="no gap")
        ax.grid(True, alpha=0.2)

        for pipeline in PIPELINES:
            for bb in BACKBONES:
                for lr in LRS:
                    d = load(pipeline, target, bb, lr)
                    if d is None:
                        continue
                    h = d["history"]
                    tr_final = h["train_acc"][-1]
                    te_best  = max(h["test_acc"])
                    marker   = "o" if pipeline == "std" else "^"
                    ax.scatter(tr_final, te_best,
                               color=BB_COLOR[bb],
                               marker=marker, s=45, alpha=0.8,
                               linewidths=0.5, edgecolors="white")

        # Backbone legend (first subplot only)
        if target == TARGETS[0]:
            from matplotlib.patches import Patch
            from matplotlib.lines import Line2D
            bb_handles = [Patch(color=BB_COLOR[b], label=BB_LABEL[b]) for b in BACKBONES]
            pl_handles = [Line2D([0], [0], marker="o", color="grey", lw=0, ms=7, label="Pipeline A"),
                          Line2D([0], [0], marker="^", color="grey", lw=0, ms=7, label="Pipeline B")]
            ax.legend(handles=bb_handles + pl_handles, fontsize=7, loc="lower right")

    plt.tight_layout()
    out = OUT_DIR / "overfit_gap.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  saved {out}")


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_dir", default="exp_models",
                        help="Directory containing *_history.json files")
    parser.add_argument("--out_dir",  default=None,
                        help="Output directory for PNGs (default: plots/ or plots_v2/ etc)")
    args = parser.parse_args()

    global BASE_DIR, OUT_DIR
    BASE_DIR = Path(args.base_dir)
    if args.out_dir:
        OUT_DIR = Path(args.out_dir)
    else:
        # auto-name: exp_models -> plots, exp_models_v2 -> plots_v2
        suffix = BASE_DIR.name.replace("exp_models", "")
        OUT_DIR = Path(f"plots{suffix}")

    OUT_DIR.mkdir(exist_ok=True)
    print(f"Reading from : {BASE_DIR}/")
    print(f"Writing to   : {OUT_DIR}/\n")

    print("Accuracy + loss curves per target/pipeline:")
    for pipeline in PIPELINES:
        for target in TARGETS:
            make_acc_figure(pipeline, target)
            make_loss_figure(pipeline, target)

    print("\nSummary bar chart:")
    make_summary()

    print("\nPipeline A vs B comparison:")
    make_pipeline_comparison()

    print("\nOverfit gap scatter:")
    make_overfit_chart()

    total = sum(1 for _ in OUT_DIR.glob("*.png"))
    print(f"\nDone — {total} PNG files written to {OUT_DIR}/")


if __name__ == "__main__":
    main()
