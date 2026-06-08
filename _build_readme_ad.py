"""
Build Traingingreadme.md from Pipeline A + Pipeline D result files.
  exp_results_v2/std_*            -> Pipeline A (32 runs)
  exp_results_d/ses4ch_*          -> Pipeline D no-SMOTE (32 runs)
  exp_results_d/ses4ch_smote_*    -> Pipeline D SMOTE (32 runs)
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

V2_DIR = Path("exp_results_v2")
D_DIR  = Path("exp_results_d")
README = Path("cnn_model/Traingingreadme.md")

BACKBONES = ["rn18", "rn50", "enb0", "cnxt"]
BB_LABEL  = {"rn18": "ResNet18", "rn50": "ResNet50",
             "enb0": "EfficientNet-B0", "cnxt": "ConvNeXt-Tiny"}
LRS      = ["lr1e3", "lr1e4"]
LR_LABEL = {"lr1e3": "lr=1e-3", "lr1e4": "lr=1e-4"}
TARGETS  = ["speed", "doc", "roughness", "feed_coarse"]
TGT_LABEL = {
    "speed":       "Speed (5-class, 30 epochs)",
    "doc":         "DOC (3-class, 33 epochs)",
    "roughness":   "Roughness Ra (3-class, 33 epochs)",
    "feed_coarse": "Feed Rate Coarse (3-class, 33 epochs)",
}


def parse_result_file(path):
    text = path.read_text(encoding="utf-8")
    run_rows = []
    for row in re.finditer(
        r"\|\s*(run\d+)\s*\|\s*(\S+)\s*\|(?:[^|]+\|){10}\s*(\S+)\s*\|\s*([✓✗])\s*\|",
        text,
    ):
        run_rows.append(row.groups())  # (run_id, true_cls, mv, result)

    wm = re.search(r"Window accuracy:\s*\*\*([\d.]+)%\*\*\s*\((\d+)/(\d+)\)", text)
    rm = re.search(r"Run MV accuracy:\s*\*\*([\d.]+)%\*\*\s*\((\d+)/(\d+)\)", text)
    return {
        "runs":      run_rows,
        "win_pct":   float(wm.group(1)) if wm else 0.0,
        "win_n":     int(wm.group(2))   if wm else 0,
        "win_N":     int(wm.group(3))   if wm else 0,
        "runmv_pct": float(rm.group(1)) if rm else 0.0,
        "runmv_n":   int(rm.group(2))   if rm else 0,
        "runmv_N":   int(rm.group(3))   if rm else 0,
    }


def load_a():
    data = {}
    for tgt in TARGETS:
        for bb in BACKBONES:
            for lr in LRS:
                p = V2_DIR / f"std_{tgt}_{bb}_{lr}.md"
                if p.exists():
                    data[(tgt, bb, lr)] = parse_result_file(p)
    return data


def load_d(smote=False):
    data = {}
    prefix = "ses4ch_smote_" if smote else "ses4ch_"
    for tgt in TARGETS:
        for bb in BACKBONES:
            for lr in LRS:
                p = D_DIR / f"{prefix}{tgt}_{bb}_{lr}.md"
                if p.exists():
                    data[(tgt, bb, lr)] = parse_result_file(p)
    return data


def runmv_cell(d):
    if d is None:
        return "—"
    pct = d["runmv_pct"]
    s = f"{pct:.1f}%"
    if pct == 100.0:
        return f"**{s}**"
    if pct < 50.0:
        return f"{s} ❌"
    return s


def summary_table(data, tgt):
    rows = ["| Backbone | lr=1e-3 | lr=1e-4 |", "|---------|:-------:|:-------:|"]
    for bb in BACKBONES:
        v = [runmv_cell(data.get((tgt, bb, lr))) for lr in LRS]
        rows.append(f"| {BB_LABEL[bb]} | {v[0]} | {v[1]} |")
    return "\n".join(rows)


def detail_block(exp_id, d):
    bb_key = next(b for b in BACKBONES if f"_{b}_" in exp_id)
    lr_key = next(l for l in LRS if exp_id.endswith(l))
    header = (
        f"**{BB_LABEL[bb_key]} {LR_LABEL[lr_key]}** (`{exp_id}`) "
        f"— Window: {d['win_pct']:.1f}% | Run MV: **{d['runmv_pct']:.1f}%** "
        f"({d['runmv_n']}/{d['runmv_N']})"
    )
    rows = ["| Run | True | MV | Result |", "|-----|------|-----|--------|"]
    for run_id, true_cls, mv, result in d["runs"]:
        rows.append(f"| {run_id} | {true_cls} | {mv} | {result} |")
    footer = (
        f"\nWindow accuracy: **{d['win_pct']:.1f}%** ({d['win_n']}/{d['win_N']})\n"
        f"Run MV accuracy: **{d['runmv_pct']:.1f}%** ({d['runmv_n']}/{d['runmv_N']})"
    )
    return header + "\n\n" + "\n".join(rows) + "\n" + footer


def detail_section(pl_prefix, data, tgt, heading):
    lines = [f"### {heading}\n"]
    for bb in BACKBONES:
        for lr in LRS:
            d = data.get((tgt, bb, lr))
            if d:
                exp_id = f"{pl_prefix}_{tgt}_{bb}_{lr}"
                lines.append(detail_block(exp_id, d))
                lines.append("")
    return "\n".join(lines)


def build():
    a      = load_a()
    d      = load_d(smote=False)
    d_smot = load_d(smote=True)
    print(f"Loaded: Pipeline A={len(a)}  Pipeline D={len(d)}  Pipeline D+SMOTE={len(d_smot)}")

    W = []

    W.append("# CNN Training Results — Pipeline A & Pipeline D\n")
    W.append(
        "Comparison of two CWT-based classification pipelines across four milling process\n"
        "parameter targets. Pipeline A uses a standard 3-channel RGB scalogram; Pipeline D\n"
        "adds raw ai6 and SES channels as a full 4-channel input.\n"
    )
    W.append(f"**Total experiments:** 96  (32 Pipeline A · 32 Pipeline D · 32 Pipeline D+SMOTE)\n")

    W.append("---\n")
    W.append("## Pipelines\n")

    W.append("### Pipeline A — Standard RGB CWT (`std`)\n")
    W.append(
        "| Item | Detail |\n"
        "|------|--------|\n"
        "| Input | 3-channel PNG 224×224 |\n"
        "| Channels | R=CWT(ai4 raw), G=CWT(ai6 raw), B=0 |\n"
        "| Backbone | Unmodified ImageNet pretrained |\n"
        "| Script | `cnn_model/cnn_train.py` |\n"
        "| Scalograms | `scalograms_10w/` |\n"
    )

    W.append("### Pipeline D — 4-Channel SES CWT (`ses4ch`)\n")
    W.append(
        "| Item | Detail |\n"
        "|------|--------|\n"
        "| Input | 4-channel .npy 4×224×224 float32 [0,1] |\n"
        "| ch0 | CWT(ai4 raw) |\n"
        "| ch1 | CWT(ai6 raw) |\n"
        "| ch2 | CWT(SES ai4) — squared envelope \\|H{x}\\|² |\n"
        "| ch3 | CWT(SES ai6) — squared envelope \\|H{x}\\|² |\n"
        "| Backbone | First conv patched to 4-ch (4th kernel = avg of 3-ch weights) |\n"
        "| Script | `cnn_model/cnn_train_hilbert.py` |\n"
        "| Scalograms | `scalograms_ses_4ch_10w/` |\n"
        "| SMOTE | `cnn_model/smote_ses_4ch.py` — signal-space interpolation |\n"
    )

    W.append("---\n")
    W.append("## Training Configuration\n")
    W.append(
        "| Parameter | Value |\n"
        "|-----------|-------|\n"
        "| Optimizer | AdamW |\n"
        "| Weight decay | 1e-4 |\n"
        "| LR scheduler | Cosine annealing |\n"
        "| Label smoothing | 0.05 |\n"
        "| MixUp alpha | 0.2 |\n"
        "| Batch size | 16 |\n"
        "| Speed epochs | 30 |\n"
        "| DOC / Roughness / Feed epochs | 33 |\n"
    )

    W.append("---\n")
    W.append("## Data Splits\n")
    W.append(
        "| Target | Train runs | Test runs | Test selection |\n"
        "|--------|----------:|----------:|----------------|\n"
        "| Speed (5-class) | 30 | 15 | 3/class × 5 RPM levels |\n"
        "| DOC (3-class) | 33 | 12 | 4/class × 3 DOC levels |\n"
        "| Roughness (3-class) | 33 | 12 | 4/class × 3 Ra classes |\n"
        "| Feed Coarse (3-class) | 33 | 12 | 4/class × 3 feed rates |\n"
    )
    W.append(
        "Pipeline D uses `SPEED_TEST_RUNS_H` / `DOC_TEST_RUNS_H` from `cnn_train_hilbert.py` "
        "(balanced sets distinct from Pipeline A's splits).\n"
    )

    # Per-target
    for tgt in TARGETS:
        W.append("---\n")
        W.append(f"## {TGT_LABEL[tgt]}\n")

        W.append(f"### Results — Pipeline A — {TGT_LABEL[tgt]} — eval on test set\n")
        W.append(summary_table(a, tgt))
        W.append("\n")

        W.append(f"### Results — Pipeline D — {TGT_LABEL[tgt]} — eval on test set\n")
        W.append(summary_table(d, tgt))
        W.append("\n")

        W.append(f"### Results — Pipeline D (SMOTE) — {TGT_LABEL[tgt]} — eval on test set\n")
        W.append(summary_table(d_smot, tgt))
        W.append("\n")

        W.append(detail_section("std", a, tgt,
            f"Per-Run Detail — Pipeline A — {TGT_LABEL[tgt]}"))

        W.append(detail_section("ses4ch", d, tgt,
            f"Per-Run Detail — Pipeline D — {TGT_LABEL[tgt]}"))

        W.append(detail_section("ses4ch_smote", d_smot, tgt,
            f"Per-Run Detail — Pipeline D (SMOTE) — {TGT_LABEL[tgt]}"))

    text = "\n".join(W)
    README.write_text(text, encoding="utf-8")
    print(f"Written: {README}  ({len(text):,} chars)")


if __name__ == "__main__":
    build()
