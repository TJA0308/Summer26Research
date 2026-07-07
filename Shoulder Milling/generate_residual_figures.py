"""
Generate diagnostic figures for residual_preprocessing_readme.md.

Figure 1 – Condition dominance:
    Show f3 scalograms from all 8 sides (same feed, 8 different speed×doc
    conditions). Visually demonstrates that condition changes scalogram far
    more than feed does.

Figure 2 – Feed variation within one condition:
    Same side (side 1), three feeds (f3 / f5 / f7), window 1.
    Shown alongside Figure 1 to contrast: differences across conditions
    dwarf differences across feeds.

Figure 3 – Residual subtraction walkthrough:
    For side 1: show raw f3 | raw f5 | raw f7 | condition mean |
    residual f3 | residual f5 | residual f7.

Figure 4 – Cross-condition feed-delta correlation heat-map:
    For every pair of sides, compute the pixel-space correlation of
    (f7 - f3). Shows how feed direction reverses across conditions.

Output: readme_figures/fig1_condition_dominance.png
        readme_figures/fig2_feed_within_condition.png
        readme_figures/fig3_subtraction_walkthrough.png
        readme_figures/fig4_delta_correlation.png
"""
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

ROOT = Path(__file__).parent
OUT  = ROOT / "readme_figures"
OUT.mkdir(exist_ok=True)

SRC_DIR  = ROOT / "scalograms_32x3_feedopt"
RES_DIR  = ROOT / "scalograms_32x3_feedopt_residual"

SIDE_TO_SPEED = {1:0, 2:1, 3:0, 4:1, 5:0, 6:1, 7:0, 8:1}  # 0=2500rpm, 1=3500rpm
SIDE_TO_DOC   = {1:0, 2:0, 3:1, 4:1, 5:2, 6:2, 7:3, 8:3}
SPEED_LABEL   = {0: "2500 rpm", 1: "3500 rpm"}
DOC_LABEL     = {0: "doc1", 1: "doc2", 2: "doc3", 3: "doc4"}


def load(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("L"), dtype=np.float32)


df     = pd.read_csv(SRC_DIR / "labels.csv")
df_res = pd.read_csv(RES_DIR / "labels.csv")

imgs     = {fn: load(SRC_DIR / fn) for fn in df["filename"]}
imgs_res = {fn: load(RES_DIR / fn) for fn in df_res["filename"]}


# ── Figure 1: condition dominance ────────────────────────────────────────────
fig, axes = plt.subplots(2, 4, figsize=(12, 7))
fig.suptitle("Fig 1 — Same feed (f3), all 8 conditions\n"
             "The scalogram pattern is dominated by speed × depth-of-cut, "
             "not by feed rate.", fontsize=11, y=1.01)

for side in range(1, 9):
    ax = axes[(side-1)//4][(side-1)%4]
    row = df[(df["side"] == side) & (df["feed"] == "f3") & (df["window"] == "w1")].iloc[0]
    ax.imshow(imgs[row["filename"]], cmap="viridis", aspect="auto")
    spd = SPEED_LABEL[SIDE_TO_SPEED[side]]
    doc = DOC_LABEL[SIDE_TO_DOC[side]]
    ax.set_title(f"Side {side}\n{spd}, {doc}", fontsize=9)
    ax.axis("off")

plt.tight_layout()
plt.savefig(OUT / "fig1_condition_dominance.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved fig1_condition_dominance.png")


# ── Figure 2: feed variation within one condition ─────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(9, 4))
fig.suptitle("Fig 2 — Same condition (side 1: 2500 rpm, doc1), three feeds\n"
             "Feed differences are subtle compared with the between-condition "
             "variation in Fig 1.", fontsize=10)

for i, feed in enumerate(["f3", "f5", "f7"]):
    row = df[(df["side"] == 1) & (df["feed"] == feed) & (df["window"] == "w1")].iloc[0]
    axes[i].imshow(imgs[row["filename"]], cmap="viridis", aspect="auto")
    axes[i].set_title(feed, fontsize=12)
    axes[i].axis("off")

plt.tight_layout()
plt.savefig(OUT / "fig2_feed_within_condition.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved fig2_feed_within_condition.png")


# ── Figure 3: subtraction walkthrough ────────────────────────────────────────
side = 1
feeds = ["f3", "f5", "f7"]
window = "w1"

raw_imgs  = []
res_imgs  = []
for feed in feeds:
    row = df[(df["side"] == side) & (df["feed"] == feed) & (df["window"] == window)].iloc[0]
    raw_imgs.append(imgs[row["filename"]])
    res_imgs.append(imgs_res[row["filename"]])

cond_mean = np.mean(raw_imgs, axis=0)

fig = plt.figure(figsize=(14, 7))
gs  = gridspec.GridSpec(2, 4, figure=fig, wspace=0.05, hspace=0.35)
fig.suptitle("Fig 3 — Residual subtraction walkthrough (side 1, window 1)\n"
             "Top: raw scalograms for f3/f5/f7 + their per-condition mean  "
             "Bottom: after subtracting the condition mean", fontsize=10)

vmin_raw  = min(r.min() for r in raw_imgs)
vmax_raw  = max(r.max() for r in raw_imgs)
vmin_res  = min(r.min() for r in res_imgs)
vmax_res  = max(r.max() for r in res_imgs)

for i, (feed, raw, res) in enumerate(zip(feeds, raw_imgs, res_imgs)):
    ax_top = fig.add_subplot(gs[0, i])
    ax_top.imshow(raw, cmap="viridis", aspect="auto", vmin=vmin_raw, vmax=vmax_raw)
    ax_top.set_title(f"Raw {feed}", fontsize=10)
    ax_top.axis("off")

    ax_bot = fig.add_subplot(gs[1, i])
    ax_bot.imshow(res, cmap="RdBu_r", aspect="auto", vmin=vmin_res, vmax=vmax_res)
    ax_bot.set_title(f"Residual {feed}", fontsize=10)
    ax_bot.axis("off")

ax_mean = fig.add_subplot(gs[0, 3])
ax_mean.imshow(cond_mean, cmap="viridis", aspect="auto", vmin=vmin_raw, vmax=vmax_raw)
ax_mean.set_title("Condition mean\n(subtracted)", fontsize=10)
ax_mean.axis("off")

ax_blank = fig.add_subplot(gs[1, 3])
ax_blank.text(0.5, 0.5, "Feed signal\nisolated", ha="center", va="center",
              fontsize=12, color="gray", transform=ax_blank.transAxes)
ax_blank.axis("off")

plt.savefig(OUT / "fig3_subtraction_walkthrough.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved fig3_subtraction_walkthrough.png")


# ── Figure 4: cross-condition feed-delta correlation ─────────────────────────
sides = list(range(1, 9))
n = len(sides)

# Compute f7-f3 delta vector per side (mean over 3 windows)
deltas = {}
for side in sides:
    f3_rows = df[(df["side"] == side) & (df["feed"] == "f3")]
    f7_rows = df[(df["side"] == side) & (df["feed"] == "f7")]
    d = (np.mean([imgs[r["filename"]] for _, r in f7_rows.iterrows()], axis=0) -
         np.mean([imgs[r["filename"]] for _, r in f3_rows.iterrows()], axis=0))
    deltas[side] = d.flatten()

corr = np.zeros((n, n))
for i, s1 in enumerate(sides):
    for j, s2 in enumerate(sides):
        d1, d2 = deltas[s1], deltas[s2]
        corr[i, j] = np.corrcoef(d1, d2)[0, 1]

fig, ax = plt.subplots(figsize=(7, 6))
im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
ax.set_xticks(range(n))
ax.set_xticklabels([f"S{s}" for s in sides])
ax.set_yticks(range(n))
ax.set_yticklabels([f"S{s}" for s in sides])
for i in range(n):
    for j in range(n):
        ax.text(j, i, f"{corr[i,j]:.2f}", ha="center", va="center",
                fontsize=7.5, color="black" if abs(corr[i,j]) < 0.7 else "white")
plt.colorbar(im, ax=ax, label="Pearson r")
ax.set_title("Fig 4 — Cross-condition correlation of (f7 − f3) feed-delta vector\n"
             "Negative values mean the feed signal literally reverses direction.\n"
             f"Mean off-diagonal: {corr[~np.eye(n,dtype=bool)].mean():.3f}", fontsize=10)
plt.tight_layout()
plt.savefig(OUT / "fig4_delta_correlation.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved fig4_delta_correlation.png")

print(f"\nAll figures saved to {OUT}/")
