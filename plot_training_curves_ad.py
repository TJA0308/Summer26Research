"""
Training curve plots for Pipeline A (std) and Pipeline D (ses4ch / ses4ch_smote).

Sources:
    exp_models_v2/std_{target}_{bb}_{lr}_history.json         -> Pipeline A
    exp_models_d/ses4ch_{target}_{bb}_{lr}_history.json       -> Pipeline D
    exp_models_d/ses4ch_smote_{target}_{bb}_{lr}_history.json -> Pipeline D + SMOTE

Note: model filenames use 'feed' not 'feed_coarse'.

Output: plots_ad/  (~30 PNG files)

Usage:
    python plot_training_curves_ad.py
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# ── Directories ────────────────────────────────────────────────────────────
A_DIR   = Path("exp_models_v2")
D_DIR   = Path("exp_models_d")
OUT_DIR = Path("plots_ad")

# ── Dimension constants ────────────────────────────────────────────────────
BACKBONES = ["rn18", "rn50", "enb0", "cnxt"]
BB_LABEL  = {"rn18": "ResNet18", "rn50": "ResNet50",
             "enb0": "EfficientNet-B0", "cnxt": "ConvNeXt-Tiny"}
LRS       = ["lr1e3", "lr1e4"]
LR_LABEL  = {"lr1e3": "lr=1e-3", "lr1e4": "lr=1e-4"}
LR_ALPHA  = {"lr1e3": 1.0, "lr1e4": 0.55}
LR_DASH   = {"lr1e3": "-", "lr1e4": "--"}

# model filenames use "feed" (not "feed_coarse")
TARGETS   = ["speed", "doc", "roughness", "feed"]
TGT_LABEL = {
    "speed":     "Speed (5-class, 30 ep)",
    "doc":       "DOC (3-class, 33 ep)",
    "roughness": "Roughness (3-class, 33 ep)",
    "feed":      "Feed Coarse (3-class, 33 ep)",
}

PIPELINES = ["std", "ses4ch", "ses4ch_smote"]
PL_LABEL  = {
    "std":         "Pipeline A — Std RGB CWT",
    "ses4ch":      "Pipeline D — 4-ch SES CWT",
    "ses4ch_smote":"Pipeline D + SMOTE — 4-ch SES CWT",
}
PL_COLOR  = {"std": "#1f77b4", "ses4ch": "#d62728", "ses4ch_smote": "#2ca02c"}
PL_LS     = {"std": "-",       "ses4ch": "--",       "ses4ch_smote": "-."}

BB_COLOR  = {"rn18": "#4C72B0", "rn50": "#DD8452",
             "enb0": "#55A868", "cnxt": "#C44E52"}


def _fmt_pct(x, _):
    return f"{x:.0%}"


def load(pipeline, target, bb, lr):
    if pipeline == "std":
        p = A_DIR / f"std_{target}_{bb}_{lr}_history.json"
    elif pipeline == "ses4ch":
        p = D_DIR / f"ses4ch_{target}_{bb}_{lr}_history.json"
    else:  # ses4ch_smote
        p = D_DIR / f"ses4ch_smote_{target}_{bb}_{lr}_history.json"
    if not p.exists():
        return None
    with open(p) as f:
        return json.load(f)


# ── 1. Per-pipeline per-target accuracy curves ─────────────────────────────

def make_acc_figure(pipeline, target):
    fig, axes = plt.subplots(2, 2, figsize=(13, 9), sharey=True)
    fig.suptitle(f"{PL_LABEL[pipeline]}  ·  {TGT_LABEL[target]}  — Accuracy",
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
            h    = d["history"]
            ep   = range(1, len(h["train_acc"]) + 1)
            best = max(h["test_acc"])
            col  = BB_COLOR[bb]
            al   = LR_ALPHA[lr]
            ax.plot(ep, h["train_acc"], color=col, lw=1.0, alpha=al * 0.35, ls="-")
            ax.plot(ep, h["test_acc"],  color=col, lw=1.8, alpha=al,
                    ls=LR_DASH[lr],
                    label=f"{LR_LABEL[lr]}  best={best:.1%}")
        ax.legend(fontsize=8, loc="lower right")

    from matplotlib.lines import Line2D
    handles = [
        Line2D([0], [0], color="grey", lw=1.0, alpha=0.35, ls="-", label="train acc (thin)"),
        Line2D([0], [0], color="grey", lw=1.8, ls="-",              label="test acc  lr=1e-3"),
        Line2D([0], [0], color="grey", lw=1.8, ls="--",             label="test acc  lr=1e-4"),
    ]
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
            h   = d["history"]
            ep  = range(1, len(h["train_loss"]) + 1)
            col = BB_COLOR[bb]
            al  = LR_ALPHA[lr]
            ax.plot(ep, h["train_loss"], color=col, lw=1.0, alpha=al * 0.35, ls="-")
            ax.plot(ep, h["test_loss"],  color=col, lw=1.8, alpha=al,
                    ls=LR_DASH[lr], label=LR_LABEL[lr])
            all_losses += h["train_loss"] + h["test_loss"]

        if all_losses:
            p95 = np.percentile(all_losses, 95)
            ax.set_ylim(0, min(max(all_losses) * 1.05, p95 * 2.5))
        ax.legend(fontsize=8)

    from matplotlib.lines import Line2D
    handles = [
        Line2D([0], [0], color="grey", lw=1.0, alpha=0.35, ls="-", label="train loss"),
        Line2D([0], [0], color="grey", lw=1.8, ls="-",              label="test loss  lr=1e-3"),
        Line2D([0], [0], color="grey", lw=1.8, ls="--",             label="test loss  lr=1e-4"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=8,
               bbox_to_anchor=(0.5, -0.01))
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    out = OUT_DIR / f"{pipeline}_{target}_loss.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  saved {out}")


# ── 2. Pipeline A vs D comparison per target ───────────────────────────────

def make_comparison(target):
    """One figure per target, 4 subplots (one per backbone).
    Shows test accuracy curves for all 3 pipeline × 2 LR = 6 lines each."""
    fig, axes = plt.subplots(2, 2, figsize=(13, 9), sharey=True)
    fig.suptitle(f"Pipeline A vs D  ·  {TGT_LABEL[target]}  — Test Accuracy",
                 fontsize=13, fontweight="bold")

    for ax, bb in zip(axes.flatten(), BACKBONES):
        ax.set_title(BB_LABEL[bb], fontsize=11)
        ax.set_xlabel("Epoch", fontsize=9)
        ax.set_ylabel("Test Accuracy", fontsize=9)
        ax.set_ylim(-0.02, 1.07)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_pct))
        ax.grid(True, alpha=0.25)
        ax.axhline(1.0, color="grey", lw=0.7, ls=":")

        for pl in PIPELINES:
            for lr in LRS:
                d = load(pl, target, bb, lr)
                if d is None:
                    continue
                h    = d["history"]
                ep   = range(1, len(h["test_acc"]) + 1)
                best = max(h["test_acc"])
                col  = PL_COLOR[pl]
                al   = LR_ALPHA[lr]
                ls   = PL_LS[pl] if lr == "lr1e3" else ":"
                short = PL_LABEL[pl].split("—")[0].strip()
                ax.plot(ep, h["test_acc"], color=col, lw=1.6, alpha=al, ls=ls,
                        label=f"{short} {LR_LABEL[lr]} {best:.1%}")
        ax.legend(fontsize=7, loc="lower right")

    plt.tight_layout()
    out = OUT_DIR / f"compare_AD_{target}.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  saved {out}")


# ── 3. Summary bar chart ───────────────────────────────────────────────────

def make_summary():
    fig, axes = plt.subplots(len(TARGETS), len(PIPELINES),
                             figsize=(15, 4 * len(TARGETS)), sharey=True)
    fig.suptitle("Best Test Accuracy — Pipeline A vs D (no-SMOTE vs SMOTE)",
                 fontsize=14, fontweight="bold")

    hatch_map = {"lr1e3": "", "lr1e4": "///"}
    x = np.arange(len(BACKBONES))
    width = 0.35

    for row, target in enumerate(TARGETS):
        for col, pl in enumerate(PIPELINES):
            ax = axes[row][col]
            ax.set_title(f"{PL_LABEL[pl]}\n{TGT_LABEL[target]}", fontsize=8)
            ax.set_ylim(0, 1.10)
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_pct))
            ax.axhline(1.0, color="grey", lw=0.6, ls="--", alpha=0.4)
            ax.grid(True, axis="y", alpha=0.25)
            ax.set_xticks(x)
            ax.set_xticklabels([BB_LABEL[b] for b in BACKBONES],
                               rotation=25, ha="right", fontsize=7)

            for i, lr in enumerate(LRS):
                vals = []
                for bb in BACKBONES:
                    d = load(pl, target, bb, lr)
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
                                f"{v:.0%}", ha="center", va="bottom", fontsize=6)
            if row == 0 and col == 0:
                ax.legend(fontsize=8)

    from matplotlib.patches import Patch
    bb_handles = [Patch(color=BB_COLOR[b], label=BB_LABEL[b]) for b in BACKBONES]
    fig.legend(handles=bb_handles, loc="lower center", ncol=4, fontsize=9,
               bbox_to_anchor=(0.5, -0.005), title="Backbone")
    plt.tight_layout(rect=[0, 0.025, 1, 1])
    out = OUT_DIR / "summary_best_acc.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  saved {out}")


# ── 4. Overfit gap scatter ─────────────────────────────────────────────────

def make_overfit():
    fig, axes = plt.subplots(1, len(TARGETS), figsize=(16, 5), sharey=True)
    fig.suptitle("Overfitting Gap — Final Train Acc vs Best Test Acc",
                 fontsize=13, fontweight="bold")

    pl_marker = {"std": "o", "ses4ch": "^", "ses4ch_smote": "s"}

    for ax, target in zip(axes, TARGETS):
        ax.set_title(TGT_LABEL[target], fontsize=10)
        ax.set_xlabel("Final Train Acc", fontsize=9)
        ax.set_ylabel("Best Test Acc", fontsize=9)
        ax.set_xlim(0.4, 1.05)
        ax.set_ylim(0.4, 1.05)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(_fmt_pct))
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_pct))
        ax.plot([0, 1], [0, 1], "k--", lw=0.7, alpha=0.4)
        ax.grid(True, alpha=0.2)

        for pl in PIPELINES:
            for bb in BACKBONES:
                for lr in LRS:
                    d = load(pl, target, bb, lr)
                    if d is None:
                        continue
                    h = d["history"]
                    ax.scatter(h["train_acc"][-1], max(h["test_acc"]),
                               color=BB_COLOR[bb],
                               marker=pl_marker[pl], s=50, alpha=0.8,
                               linewidths=0.5, edgecolors="white")

        if target == TARGETS[0]:
            from matplotlib.patches import Patch
            from matplotlib.lines import Line2D
            bb_h = [Patch(color=BB_COLOR[b], label=BB_LABEL[b]) for b in BACKBONES]
            pl_h = [Line2D([0], [0], marker=pl_marker[pl], color="grey",
                           lw=0, ms=7, label=PL_LABEL[pl].split("—")[0].strip())
                    for pl in PIPELINES]
            ax.legend(handles=bb_h + pl_h, fontsize=7, loc="lower right")

    plt.tight_layout()
    out = OUT_DIR / "overfit_gap.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  saved {out}")


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    OUT_DIR.mkdir(exist_ok=True)
    print(f"Writing to: {OUT_DIR}/\n")

    print("Accuracy + loss curves per pipeline / target:")
    for pl in PIPELINES:
        for tgt in TARGETS:
            make_acc_figure(pl, tgt)
            make_loss_figure(pl, tgt)

    print("\nPipeline A vs D comparison (per target):")
    for tgt in TARGETS:
        make_comparison(tgt)

    print("\nSummary bar chart:")
    make_summary()

    print("\nOverfit gap scatter:")
    make_overfit()

    total = sum(1 for _ in OUT_DIR.glob("*.png"))
    print(f"\nDone — {total} PNG files in {OUT_DIR}/")


if __name__ == "__main__":
    main()
