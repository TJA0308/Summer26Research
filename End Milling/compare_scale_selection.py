"""
Test: are the CWT scale rows already selected for roughness
(scalograms_32x3/) and feed_coarse (scalograms_32x3_feedopt/) also good
choices for speed and doc, or would dedicated speed-tuned/doc-tuned scale
selections meaningfully differ?

Method
------
For each of the 4 targets (roughness, feed_coarse, speed, doc), compute the
same averaged |Spearman rho| score for all 64 CWT scale rows
(em_feature_common.cwt_row_scores -- identical method build_32x3_features.py
/build_32x12_features.py use to pick their top-32). This gives 4 independent
"ground truth" rankings of which rows matter for which target.

Then, for the two EXISTING selections (roughness's top-32, feed_coarse's
top-32), check how they'd score if repurposed for speed/doc instead of
built fresh for speed/doc:

  - Overlap: how many of the existing 32 rows are also in speed's/doc's own
    true top-32 (out of 32; 32/32 would mean the selections are identical).
  - Efficiency: mean(target's score over the EXISTING 32 rows) /
    mean(target's score over target's OWN true top-32 rows). 100% means the
    existing selection is exactly as good as a dedicated one would be for
    that target; well below 100% means real signal is being left out.

This does not itself decide whether to build dedicated scalograms -- it
just quantifies the gap so that decision is evidence-based.

Usage:
    python compare_scale_selection.py
"""
from em_feature_common import load_cnn_train_module, load_all_run_images, cwt_row_scores, N_SELECT

TARGETS = ["roughness", "feed_coarse", "speed", "doc"]
EXISTING = ["roughness", "feed_coarse"]   # selections that already exist as scalogram dirs


def top_indices(scores, n=N_SELECT):
    return set(scores.argsort()[::-1][:n].tolist())


def main():
    mod = load_cnn_train_module()
    print("Loading precomputed feature sheets (data/STLMILAE_DOC*.xlsx) ...")
    images = load_all_run_images(mod)
    print(f"  {len(images)} runs loaded\n")

    scores = {t: cwt_row_scores(images, mod, t) for t in TARGETS}
    top32 = {t: top_indices(scores[t]) for t in TARGETS}

    print("Mean |Spearman rho| over each target's OWN top-32 rows (upper bound):")
    for t in TARGETS:
        own_mean = scores[t][sorted(top32[t])].mean()
        print(f"  {t:12s}: {own_mean:.4f}")

    print("\n" + "=" * 78)
    print("Repurposing existing selections for speed / doc")
    print("=" * 78)

    for existing in EXISTING:
        existing_rows = sorted(top32[existing])
        print(f"\n--- {existing}'s selected 32 rows, evaluated for other targets ---")
        for test_target in ["speed", "doc"]:
            overlap = len(top32[existing] & top32[test_target])
            existing_mean = scores[test_target][existing_rows].mean()
            own_mean = scores[test_target][sorted(top32[test_target])].mean()
            efficiency = 100.0 * existing_mean / own_mean if own_mean > 0 else float("nan")
            print(f"  vs {test_target:12s}: overlap {overlap:2d}/32 rows  |  "
                  f"mean score {existing_mean:.4f} vs own-best {own_mean:.4f}  "
                  f"({efficiency:.1f}% efficiency)")

    print("\n" + "=" * 78)
    print("Cross-check: speed vs doc's own selections against each other, and")
    print("against roughness/feed_coarse (both directions), for completeness")
    print("=" * 78)
    for a in TARGETS:
        for b in TARGETS:
            if a >= b:
                continue
            overlap = len(top32[a] & top32[b])
            print(f"  {a:12s} vs {b:12s}: overlap {overlap:2d}/32 rows")


if __name__ == "__main__":
    main()
