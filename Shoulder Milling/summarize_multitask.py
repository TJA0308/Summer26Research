"""
Aggregates cnn_train_multitask.py's history.json files across seeds and
prints mean +/- std per (scalogram, split) -- the statistic this experiment
is actually judged on (see cnn_train_multitask.py's docstring), not a
best-of-sweep pick.

Also prints the falsification verdict proposed alongside this experiment:
FAIL if mean feed window accuracy stays <= 46% everywhere, or mean feed run
accuracy stays <= 62.5% (5/8) on 2 or more of the 3 splits per scalogram dir
-- i.e. multi-task learning didn't move the needle beyond what the (buggy,
non-reproducing) cascade and every prior sweep already established as feed's
real ceiling.

Usage (from this directory, after running run_multitask_feed.ps1):
    python summarize_multitask.py
"""
import glob
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
WINDOW_FAIL_THRESHOLD = 0.46
RUN_FAIL_THRESHOLD    = 0.625


def load_all():
    rows = []
    for path in glob.glob(str(HERE / "models_multitask_feed_*" / "*_history.json")):
        with open(path) as f:
            d = json.load(f)
        rows.append(d)
    return rows


def main():
    rows = load_all()
    if not rows:
        print("No models_multitask_feed_*/*_history.json files found -- "
              "run run_multitask_feed.ps1 first.")
        return

    groups = defaultdict(list)
    for r in rows:
        key = (r["scalogram"], r["split_id"] or "base", r["arch"], r["lr"])
        groups[key].append(r)

    print(f"{'scalogram':<22} {'split':<6} {'arch':<16} {'lr':<7} {'n':>2}  "
          f"{'window_acc':>18}  {'run_hard':>18}  {'run_soft':>18}")
    print("-" * 112)

    fail_counts = defaultdict(int)   # scalo -> count of splits failing run threshold
    scalo_splits = defaultdict(set)
    window_pass_any = defaultdict(bool)

    for key in sorted(groups):
        scalo, split, arch, lr = key
        runs = groups[key]
        seeds = sorted(r["seed"] for r in runs)
        window = np.array([r["best_feed_window_acc"] for r in runs])
        run_hard = np.array([r["feed_run_acc_hard"] for r in runs])
        run_soft = np.array([r["feed_run_acc_soft"] for r in runs])

        print(f"{scalo:<22} {split:<6} {arch:<16} {lr:<7} {len(runs):>2}  "
              f"{window.mean():>6.3f} +/- {window.std():<7.3f}  "
              f"{run_hard.mean():>6.3f} +/- {run_hard.std():<7.3f}  "
              f"{run_soft.mean():>6.3f} +/- {run_soft.std():<7.3f}  "
              f"(seeds {seeds})")

        scalo_splits[scalo].add(split)
        if window.mean() > WINDOW_FAIL_THRESHOLD:
            window_pass_any[scalo] = True
        if max(run_hard.mean(), run_soft.mean()) <= RUN_FAIL_THRESHOLD:
            fail_counts[scalo] += 1

    print("\n--- Verdict (see cnn_train_multitask.py docstring for rationale) ---")
    for scalo in sorted(scalo_splits):
        n_splits = len(scalo_splits[scalo])
        window_ok = window_pass_any.get(scalo, False)
        run_fails = fail_counts.get(scalo, 0)
        failed = (not window_ok) or (run_fails >= 2)
        verdict = "FAIL (no improvement over cascade ceiling)" if failed else "PASS (worth pursuing further)"
        print(f"{scalo}: window_acc>{WINDOW_FAIL_THRESHOLD:.0%} on any split = {window_ok}, "
              f"run_acc<={RUN_FAIL_THRESHOLD:.1%} on {run_fails}/{n_splits} splits -> {verdict}")


if __name__ == "__main__":
    main()
