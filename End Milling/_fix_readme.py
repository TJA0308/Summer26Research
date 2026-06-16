"""
Rebuild all per-run tables and summary accuracy tables in Trainingreadme.md
using the ground-truth data from exp_results_v2/.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

RESULTS_DIR = Path("exp_results_v2")
README      = Path("cnn_model/Traingingreadme.md")

BACKBONE_LABELS = {
    "rn18": "ResNet18", "rn50": "ResNet50",
    "enb0": "EfficientNet-B0", "cnxt": "ConvNeXt-Tiny",
}
BACKBONES = ["rn18", "rn50", "enb0", "cnxt"]
LRS       = ["lr1e3", "lr1e4"]
LR_LABELS = {"lr1e3": "lr=1e-3", "lr1e4": "lr=1e-4"}
PIPELINES = ["std", "ses", "sesrgb"]
TARGETS   = ["speed", "doc", "roughness", "feed_coarse"]  # README naming


# ── Parse a single exp_results_v2 file ─────────────────────────────────────

def parse_result_file(path):
    text = path.read_text(encoding="utf-8")

    # per-run rows: | run<N> | True | w1..w10 | MV | ✓/✗ |
    run_rows = []
    for row in re.finditer(
        r"\|\s*(run\d+)\s*\|\s*(\S+)\s*\|(?:[^|]+\|){10}\s*(\S+)\s*\|\s*([✓✗])\s*\|",
        text
    ):
        run_id, true_cls, mv, result = row.groups()
        run_rows.append((run_id, true_cls, mv, result))

    wm = re.search(r"Window accuracy:\s*\*\*([\d.]+)%\*\*\s*\((\d+)/(\d+)\)", text)
    rm = re.search(r"Run MV accuracy:\s*\*\*([\d.]+)%\*\*\s*\((\d+)/(\d+)\)", text)

    return {
        "runs":       run_rows,
        "win_pct":    float(wm.group(1)) if wm else None,
        "win_n":      int(wm.group(2))   if wm else None,
        "win_N":      int(wm.group(3))   if wm else None,
        "runmv_pct":  float(rm.group(1)) if rm else None,
        "runmv_n":    int(rm.group(2))   if rm else None,
        "runmv_N":    int(rm.group(3))   if rm else None,
    }


# ── Load all result data ────────────────────────────────────────────────────

def load_all():
    """Returns dict keyed by (pipeline, target_readme, backbone, lr)."""
    data = {}
    for path in RESULTS_DIR.glob("*.md"):
        # Filename pattern: <pipeline>_<target>_<bb>_<lr>.md
        # target may be "feed" or "feed_coarse"
        stem = path.stem
        for pl in PIPELINES:
            if not stem.startswith(pl + "_"):
                continue
            rest = stem[len(pl)+1:]
            for bb in BACKBONES:
                for lr in LRS:
                    suffix = f"_{bb}_{lr}"
                    if rest.endswith(suffix):
                        tgt_raw = rest[:-len(suffix)]
                        # normalise: "feed" -> "feed_coarse"
                        tgt = "feed_coarse" if tgt_raw == "feed" else tgt_raw
                        data[(pl, tgt, bb, lr)] = parse_result_file(path)
    return data


# ── Build the compact per-run table block ──────────────────────────────────

def make_block(pl, tgt, bb, lr, d):
    """Return the replacement text for one backbone/lr block."""
    readme_id = f"{pl}_{tgt}_{bb}_{lr}"

    header = (
        f"**{BACKBONE_LABELS[bb]} {LR_LABELS[lr]}** (`{readme_id}`) "
        f"— Window: {d['win_pct']:.1f}% | Run MV: **{d['runmv_pct']:.1f}%** "
        f"({d['runmv_n']}/{d['runmv_N']})"
    )

    table_rows = ["| Run | True | MV | Result |", "|-----|------|-----|--------|"]
    for run_id, true_cls, mv, result in d["runs"]:
        table_rows.append(f"| {run_id} | {true_cls} | {mv} | {result} |")

    footer = (
        f"\nWindow accuracy: **{d['win_pct']:.1f}%** ({d['win_n']}/{d['win_N']})\n"
        f"Run MV accuracy: **{d['runmv_pct']:.1f}%** ({d['runmv_n']}/{d['runmv_N']})"
    )

    return header + "\n\n" + "\n".join(table_rows) + "\n" + footer


# ── Build summary table row values ─────────────────────────────────────────

def runmv_str(pct, n, N):
    s = f"{pct:.1f}%"
    if pct == 100.0:
        s = f"**{s}**"
    elif pct < 50.0:
        s = f"{s} ❌"
    return s


# ── Replace one per-run block in the text ──────────────────────────────────

# Pattern: matches from the bold header line through the
# "Run MV accuracy: ..." line (inclusive).
BLOCK_RE = re.compile(
    r'(\*\*[^*]+\*\*\s*\(`[^`]+`\)\s*—\s*Window:[^\n]*\n'   # header line
    r'\n'                                                       # blank line
    r'\| Run \| True \| MV \| Result \|\n'                    # table header
    r'\|[-| ]+\|\n'                                            # separator
    r'(?:\|[^\n]+\|\n)+'                                       # data rows
    r'\nWindow accuracy:[^\n]+\n'
    r'Run MV accuracy:[^\n]+)',
    re.MULTILINE,
)


def replace_blocks(text, all_data):
    """Replace every per-run block whose exp_id we have data for."""

    def replacer(m):
        block = m.group(0)
        # Extract exp_id from the backtick label
        id_m = re.search(r'`([^`]+)`', block)
        if not id_m:
            return block
        readme_id = id_m.group(1)

        # Parse pipeline / target / bb / lr from the readme_id
        for pl in PIPELINES:
            if not readme_id.startswith(pl + "_"):
                continue
            rest = readme_id[len(pl)+1:]
            for bb in BACKBONES:
                for lr in LRS:
                    suffix = f"_{bb}_{lr}"
                    if rest.endswith(suffix):
                        tgt = rest[:-len(suffix)]
                        key = (pl, tgt, bb, lr)
                        if key in all_data:
                            return make_block(pl, tgt, bb, lr, all_data[key])
        return block  # no match — leave unchanged

    return BLOCK_RE.sub(replacer, text)


# ── Update summary accuracy tables ─────────────────────────────────────────
# Each summary table looks like:
#   | Backbone | lr=1e-3 | lr=1e-4 |
#   |---------|:-------:|:-------:|
#   | ResNet18 | X% | X% |
#   ...
# We identify them by the section structure and rebuild from data.

SECTION_RE = re.compile(
    r'(### Results — (Pipeline [ABC]) — ([^\n]+) — eval on[^\n]+\n\n)'
    r'(\| Backbone \| lr=1e-3 \| lr=1e-4 \|\n\|[-| :]+\|\n(?:\|[^\n]+\|\n)+)',
    re.MULTILINE,
)

PL_MAP = {
    "Pipeline A": "std",
    "Pipeline B": "ses",
    "Pipeline C": "sesrgb",
}

TGT_RE_MAP = {
    "speed":       re.compile(r'speed', re.I),
    "doc":         re.compile(r'DOC|depth', re.I),
    "roughness":   re.compile(r'roughness', re.I),
    "feed_coarse": re.compile(r'feed', re.I),
}


def infer_target(desc_str):
    for tgt, pat in TGT_RE_MAP.items():
        if pat.search(desc_str):
            return tgt
    return None


def rebuild_summary_table(pl, tgt, all_data):
    rows = ["| Backbone | lr=1e-3 | lr=1e-4 |", "|---------|:-------:|:-------:|"]
    for bb in BACKBONES:
        vals = []
        for lr in LRS:
            d = all_data.get((pl, tgt, bb, lr))
            if d:
                vals.append(runmv_str(d["runmv_pct"], d["runmv_n"], d["runmv_N"]))
            else:
                vals.append("—")
        rows.append(f"| {BACKBONE_LABELS[bb]} | {vals[0]} | {vals[1]} |")
    return "\n".join(rows) + "\n"


def replace_summary_tables(text, all_data):
    def replacer(m):
        header_block = m.group(1)
        pl_label     = m.group(2)
        desc         = m.group(3)
        pl = PL_MAP.get(pl_label)
        tgt = infer_target(desc)
        if pl and tgt:
            new_table = rebuild_summary_table(pl, tgt, all_data)
            return header_block + new_table
        return m.group(0)

    return SECTION_RE.sub(replacer, text)


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    all_data = load_all()
    print(f"Loaded {len(all_data)} result files")

    text = README.read_text(encoding="utf-8")

    text = replace_blocks(text, all_data)
    text = replace_summary_tables(text, all_data)

    README.write_text(text, encoding="utf-8")
    print("Traingingreadme.md updated.")

    # Quick verification
    import subprocess
    r = subprocess.run(
        ["python", "-X", "utf8", "_check_discrepancies.py"],
        capture_output=True, text=True, encoding="utf-8"
    )
    print(r.stdout[:500] if r.stdout else r.stderr[:500])


if __name__ == "__main__":
    main()
