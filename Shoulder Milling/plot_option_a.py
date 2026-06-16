"""Generate Option A explanation plots."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from PIL import Image

DATA_DIR = Path(__file__).parent / "data"
OUT_DIR  = Path(__file__).parent / "pca_plots"

FEATURE_COLS = ["32FFT","5statistics","64mexican","64coif",
                "KA","SA","KD","SD","rmsA","rmsD","crestfactA","crestfactD"]
N_ROWS = 64
COL_IDX = {c: i for i, c in enumerate(FEATURE_COLS)}

SIDE_TO_RUNS = {
    1: (1,2,3), 2:(13,14,15), 3:(4,5,6), 4:(16,17,18),
    5:(7,8,9),  6:(19,20,21), 7:(10,11,12), 8:(22,23,24),
}

def load_ra():
    raw = pd.read_excel(DATA_DIR / "Surface Roughness_Data.xlsx", header=None)
    run_ra = {}
    for _, row in raw.iterrows():
        try:
            run_ra[int(float(row[1]))] = float(row[11])
        except Exception:
            pass
    return run_ra

def sheet_to_image(df_raw):
    df = df_raw.copy()
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True).apply(pd.to_numeric, errors="coerce")
    img = np.zeros((N_ROWS, len(FEATURE_COLS)), dtype=np.float32)
    for col_idx, col in enumerate(FEATURE_COLS):
        if col not in df.columns: continue
        vals = df[col].dropna().values.astype(np.float32)
        n = min(len(vals), N_ROWS)
        img[:n, col_idx] = vals[:n]
    return img

# ── load all 72 and fit scaler ──────────────────────────────────────────────
all_imgs = []
side_sheet_map = {}
idx = 0
for i in range(1, 9):
    xl = pd.ExcelFile(DATA_DIR / f"Side{i}.xlsx")
    for sheet in xl.sheet_names:
        all_imgs.append(sheet_to_image(xl.parse(sheet, header=None)))
        side_sheet_map[(i, sheet)] = idx
        idx += 1

X_all = np.stack(all_imgs).reshape(72, -1)
scaler = StandardScaler()
X_sc   = scaler.fit_transform(X_all)

def get_option_a_channels(side_num, feed, normalised=True):
    """Return list of 3 arrays (64, 3) — one per channel R/G/B."""
    xl = pd.ExcelFile(DATA_DIR / f"Side{side_num}.xlsx")
    channels = []
    for ch_col in ["64mexican", "64coif", "32FFT"]:
        col_i = COL_IDX[ch_col]
        windows = []
        for win in ["a", "b", "c"]:
            sheet = [s for s in xl.sheet_names if f"f{feed}" in s and s.endswith(f"_{win}")][0]
            flat_i = side_sheet_map[(side_num, sheet)]
            if normalised:
                vec = X_sc[flat_i].reshape(N_ROWS, len(FEATURE_COLS))[:, col_i]
            else:
                vec = all_imgs[flat_i][:, col_i]
            windows.append(vec)
        channels.append(np.stack(windows, axis=1))   # (64, 3)
    return channels  # [R(64,3), G(64,3), B(64,3)]

def make_rgb(channels_norm):
    """Clip z-scores to [-3,3] and map to [0,1] for RGB display."""
    r, g, b = channels_norm
    return np.stack([
        np.clip((r + 3) / 6, 0, 1),
        np.clip((g + 3) / 6, 0, 1),
        np.clip((b + 3) / 6, 0, 1),
    ], axis=2)  # (64, 3, 3)

def upsample(rgb_64x3, size=224):
    pil = Image.fromarray((rgb_64x3 * 255).astype(np.uint8))
    return np.array(pil.resize((size, size), Image.BILINEAR))

# ───────────────────────────────────────────────────────────────────────────
# PLOT 17 — Structure: channels, RGB, upsampled, analogy table
# ───────────────────────────────────────────────────────────────────────────
run1_raw  = get_option_a_channels(1, 3, normalised=False)  # Run1, Ra=0.22 Low
run1_norm = get_option_a_channels(1, 3, normalised=True)

fig = plt.figure(figsize=(18, 9))
gs  = gridspec.GridSpec(2, 6, figure=fig, hspace=0.5, wspace=0.45)

ch_names  = ["Channel R\n64mexican\n(CWT Mexican hat)", "Channel G\n64coif\n(CWT Coiflet)", "Channel B\n32FFT padded to 64"]
ch_cmaps  = ["Reds", "Greens", "Blues"]

# ── top row: raw channels ──
for i in range(3):
    ax = fig.add_subplot(gs[0, i])
    vmax = np.abs(run1_raw[i]).max()
    im = ax.imshow(run1_raw[i], aspect="auto", cmap=ch_cmaps[i], vmin=0, vmax=vmax, origin="upper")
    ax.set_title(ch_names[i], fontsize=8, pad=3)
    ax.set_xticks([0,1,2]); ax.set_xticklabels(["Win A","Win B","Win C"], fontsize=7)
    if i == 0: ax.set_ylabel("Scale index (row 0 = finest scale)", fontsize=7)
    else: ax.set_yticks([])
    plt.colorbar(im, ax=ax, fraction=0.08)
    ax.axhline(31.5, color="white", linestyle="--", lw=1, alpha=0.7)
    if i == 2:
        ax.text(1, 48, "Zero-padded\n(rows 32-63)", color="white",
                ha="center", fontsize=7, alpha=0.9)

# ── top row: RGB composite + upsampled ──
rgb_raw  = np.stack([(run1_raw[i] - run1_raw[i].min()) /
                     (run1_raw[i].max() - run1_raw[i].min() + 1e-9) for i in range(3)], axis=2)
ax_rgb = fig.add_subplot(gs[0, 3])
ax_rgb.imshow(rgb_raw, aspect="auto", origin="upper")
ax_rgb.set_title("RGB composite\n(raw, per-channel normalised)", fontsize=8)
ax_rgb.set_xticks([0,1,2]); ax_rgb.set_xticklabels(["A","B","C"], fontsize=7)
ax_rgb.set_yticks([])
ax_rgb.axhline(31.5, color="white", linestyle="--", lw=1)

ax_up = fig.add_subplot(gs[0, 4])
ax_up.imshow(upsample(rgb_raw), origin="upper")
ax_up.set_title("Upsampled to\n224x224 (CNN input)", fontsize=8)
ax_up.set_xticks([]); ax_up.set_yticks([])

# ── analogy table ──
ax_tbl = fig.add_subplot(gs[0, 5])
ax_tbl.axis("off")
ax_tbl.text(0.5, 1.0, "End Milling vs Option A", ha="center", va="top",
            fontsize=8, fontweight="bold", transform=ax_tbl.transAxes)
rows = [
    ("",            "END MILLING",          "OPTION A"),
    ("Y-axis",      "300 freq scales",      "64 scale indices"),
    ("X-axis",      "~1000 time samples",   "3 windows (a,b,c)"),
    ("Channel R",   "CWT(ai4)",             "64mexican"),
    ("Channel G",   "CWT(ai6)",             "64coif"),
    ("Channel B",   "0 / CWT(SES)",         "32FFT padded"),
    ("Native size", "300 x time",           "64 x 3"),
    ("CNN input",   "224 x 224",            "224 x 224 (upsampled)"),
    ("Samples",     "~100s runs",           "24 runs (1 image/run)"),
]
for ri, (label, em, sm) in enumerate(rows):
    y = 0.92 - ri * 0.096
    ax_tbl.text(0.0, y, label, fontsize=6.5, fontweight="bold",
                color="gray", va="top", transform=ax_tbl.transAxes)
    ax_tbl.text(0.28, y, em, fontsize=6.5, color="steelblue",
                va="top", transform=ax_tbl.transAxes)
    ax_tbl.text(0.65, y, sm, fontsize=6.5, color="crimson",
                va="top", transform=ax_tbl.transAxes)

# ── bottom row: normalised channels ──
for i in range(3):
    ax = fig.add_subplot(gs[1, i])
    vmax = max(abs(run1_norm[i]).max(), 2)
    im = ax.imshow(run1_norm[i], aspect="auto", cmap="RdBu_r",
                   vmin=-vmax, vmax=vmax, origin="upper")
    ax.set_title(ch_names[i].split("\n")[0] + " (z-score)", fontsize=8)
    ax.set_xticks([0,1,2]); ax.set_xticklabels(["Win A","Win B","Win C"], fontsize=7)
    if i == 0: ax.set_ylabel("Scale index", fontsize=7)
    else: ax.set_yticks([])
    plt.colorbar(im, ax=ax, fraction=0.08, label="z-score")
    ax.axhline(31.5, color="black", linestyle="--", lw=1, alpha=0.5)

# ── normalised RGB + upsampled ──
rgb_norm = make_rgb(run1_norm)
ax_rn = fig.add_subplot(gs[1, 3])
ax_rn.imshow(rgb_norm, aspect="auto", origin="upper")
ax_rn.set_title("RGB composite\n(z-score normalised)", fontsize=8)
ax_rn.set_xticks([0,1,2]); ax_rn.set_xticklabels(["A","B","C"], fontsize=7)
ax_rn.set_yticks([])

ax_un = fig.add_subplot(gs[1, 4])
ax_un.imshow(upsample(rgb_norm), origin="upper")
ax_un.set_title("Normalised + upsampled\n224x224", fontsize=8)
ax_un.set_xticks([]); ax_un.set_yticks([])

# ── row meaning legend ──
ax_leg = fig.add_subplot(gs[1, 5])
ax_leg.axis("off")
ax_leg.text(0.5, 1.0, "What each row represents", ha="center", va="top",
            fontsize=8, fontweight="bold", transform=ax_leg.transAxes)
row_info = [
    ("Row 0",    "DC / coarsest DWT approx"),
    ("Rows 1-5", "Fine scales, DWT levels 1-5"),
    ("Rows 6-9", "Mid-fine / tooth-passing range"),
    ("Rows 10-20","Mid scales, tool interaction"),
    ("Rows 20-31","Coarser scales, FFT high bins"),
    ("Rows 32-63","Wavelet coarse scales only"),
    ("",""),
    ("3 columns", "= 3 time slices of same cut"),
    ("Consistency","windows A/B/C nearly identical"),
]
for ri, (lbl, desc) in enumerate(row_info):
    y = 0.92 - ri * 0.10
    ax_leg.text(0.0, y, lbl,  fontsize=7, fontweight="bold", color="steelblue",
                va="top", transform=ax_leg.transAxes)
    ax_leg.text(0.38, y, desc, fontsize=7, color="black",
                va="top", transform=ax_leg.transAxes)

fig.suptitle("Option A: 3-channel 64x3 scalogram (one image per run)\n"
             "R=64mexican  G=64coif  B=32FFT_padded  |  Run 1, Ra=0.22 µm (Low)",
             fontsize=11, fontweight="bold")
fig.savefig(OUT_DIR / "17_option_a_structure.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("Plot 17 done")

# ───────────────────────────────────────────────────────────────────────────
# PLOT 18 — Low vs High Ra, with difference, all 3 channels
# ───────────────────────────────────────────────────────────────────────────
# Run 1 (Side1, f3, Ra=0.22 Low) vs Run 3 (Side1, f7, Ra=0.92 High)
run3_norm = get_option_a_channels(1, 7, normalised=True)

fig, axes = plt.subplots(3, 3, figsize=(13, 11))
ch_short = ["64mexican (R)", "64coif (G)", "32FFT padded (B)"]

for ch_i in range(3):
    low  = run1_norm[ch_i]
    high = run3_norm[ch_i]
    diff = low - high

    vmax_lh = max(abs(low).max(), abs(high).max(), 3)
    vmax_d  = abs(diff).max()

    # Low
    ax = axes[ch_i, 0]
    im = ax.imshow(low, aspect="auto", cmap="RdBu_r", vmin=-vmax_lh, vmax=vmax_lh, origin="upper")
    ax.set_title(f"Run 1  Ra=0.22 Low\n{ch_short[ch_i]}", fontsize=8)
    ax.set_xticks([0,1,2]); ax.set_xticklabels(["A","B","C"], fontsize=7)
    ax.set_ylabel("Scale index", fontsize=7) if ch_i == 0 else None
    plt.colorbar(im, ax=ax, fraction=0.06)
    ax.axhline(31.5, color="white", linestyle="--", lw=1, alpha=0.6)

    # High
    ax = axes[ch_i, 1]
    im = ax.imshow(high, aspect="auto", cmap="RdBu_r", vmin=-vmax_lh, vmax=vmax_lh, origin="upper")
    ax.set_title(f"Run 3  Ra=0.92 High\n{ch_short[ch_i]}", fontsize=8)
    ax.set_xticks([0,1,2]); ax.set_xticklabels(["A","B","C"], fontsize=7)
    ax.set_yticks([])
    plt.colorbar(im, ax=ax, fraction=0.06)
    ax.axhline(31.5, color="white", linestyle="--", lw=1, alpha=0.6)

    # Difference
    ax = axes[ch_i, 2]
    im = ax.imshow(diff, aspect="auto", cmap="PiYG", vmin=-vmax_d, vmax=vmax_d, origin="upper")
    ax.set_title(f"Difference (Low - High)\n{ch_short[ch_i]}", fontsize=8)
    ax.set_xticks([0,1,2]); ax.set_xticklabels(["A","B","C"], fontsize=7)
    ax.set_yticks([])
    plt.colorbar(im, ax=ax, fraction=0.06, label="Low minus High")
    ax.axhline(31.5, color="black", linestyle="--", lw=1, alpha=0.5)

fig.suptitle("Option A: Low Ra vs High Ra — what the CNN must distinguish\n"
             "Green = Low Ra is higher | Pink = High Ra is higher",
             fontsize=11, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT_DIR / "18_option_a_lowhigh.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("Plot 18 done")

# ───────────────────────────────────────────────────────────────────────────
# PLOT 19 — All 24 runs as upsampled RGB images, labelled by Ra class
# ───────────────────────────────────────────────────────────────────────────
run_ra = load_ra()
class_color = {"Low": "steelblue", "Med": "darkorange", "High": "crimson"}

def ra_class(ra):
    if ra <= 0.30: return "Low"
    if ra <= 0.50: return "Med"
    return "High"

# build all 24 run images
FEED_MAP = {1: 3, 2: 5, 3: 7}   # run offset within side -> feed rate

fig, axes = plt.subplots(4, 6, figsize=(16, 11))
run_idx = 0
for side_num in range(1, 9):
    for feed_pos, feed in enumerate([3, 5, 7]):
        run_num = SIDE_TO_RUNS[side_num][feed_pos]
        ra      = run_ra[run_num]
        cls     = ra_class(ra)

        chs = get_option_a_channels(side_num, feed, normalised=True)
        rgb = upsample(make_rgb(chs), size=64)   # smaller for grid

        ax = axes[run_idx // 6, run_idx % 6]
        ax.imshow(rgb, origin="upper")
        ax.set_title(f"Run {run_num}\nRa={ra:.2f} ({cls})",
                     fontsize=7, color=class_color[cls], pad=2)
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_edgecolor(class_color[cls])
            spine.set_linewidth(2)
        run_idx += 1

fig.suptitle("Option A: All 24 run images (upsampled RGB, normalised)\n"
             "Blue border = Low Ra  |  Orange = Med  |  Red = High",
             fontsize=11, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT_DIR / "19_option_a_all_runs.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("Plot 19 done")
