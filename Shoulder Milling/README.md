# Shoulder Milling — Train/Test Splits

## Dataset Overview

- **Material:** Steel
- **Tool:** Carbide inserts, 3-tooth end mill
- **Total samples:** 24 cutting conditions × 3 time windows (split 1, 2, 3) = **72 samples**
- **Parameters:**
  - Speed: 2500 RPM, 3500 RPM
  - Feed: 3 in/min (f3), 5 in/min (f5), 7 in/min (f7)
  - Y-depth (doc): 0.25 in, 0.50 in
  - Z-depth (doc): 0.125 in, 0.25 in
- **Sides:** 8 sides, each a unique (speed × Y-doc × Z-doc) combination with 3 feed conditions

### Naming Convention

Each sample is identified by a **condition string + time-window letter**,
matching the Excel sheet names in `data/Side*.xlsx` verbatim, e.g.
`s25f3y5z25_a`:
- **Condition string** `s{speed}f{feed}y{Y-doc}z{Z-doc}` (e.g. `s25f3y5z25` =
  speed 2500rpm, feed f3, Y-doc 0.50in, Z-doc 0.250in) — this is the `run_id`
  used for train/test split membership and majority-vote grouping
- **Time window:** appended as `_a`, `_b`, or `_c` (the 3 time windows per run)
- **Split sub-window:** when a window is further split into 3 row-bands (see
  `split_scalogram_windows.py`), an additional `_1`, `_2`, or `_3` is appended,
  e.g. `s25f3y5z25_a_1`, `s25f3y5z25_a_2`, `s25f3y5z25_a_3`

### Side — Parameter Mapping

| Side | Speed (RPM) | Y-doc (in) | Z-doc (in) | Runs (run_id) |
|------|-------------|-----------|-----------|------|
| 1 | 2500 | 0.50 | 0.250 | s25f3y5z25, s25f5y5z25, s25f7y5z25 |
| 2 | 3500 | 0.50 | 0.250 | s35f3y5z25, s35f5y5z25, s35f7y5z25 |
| 3 | 2500 | 0.25 | 0.250 | s25f3y25z25, s25f5y25z25, s25f7y25z25 |
| 4 | 3500 | 0.25 | 0.250 | s35f3y25z25, s35f5y25z25, s35f7y25z25 |
| 5 | 2500 | 0.50 | 0.125 | s25f3y5z125, s25f5y5z125, s25f7y5z125 |
| 6 | 3500 | 0.50 | 0.125 | s35f3y5z125, s35f5y5z125, s35f7y5z125 |
| 7 | 2500 | 0.25 | 0.125 | s25f3y25z125, s25f5y25z125, s25f7y25z125 |
| 8 | 3500 | 0.25 | 0.125 | s35f3y25z125, s35f5y25z125, s35f7y25z125 |

Within each side, the three runs vary by feed: f3, f5, f7 (the `f{n}` segment of the condition string).

---

## Three Model Splits (48 train / 24 test)

Each split is designed so the test set directly isolates the target feature as the only varying factor, giving each model the clearest possible evaluation signal.

---

### Split 1 — Speed Model

**Test structure: 4 matched speed-pairs**
Within each pair, speed is the only thing that varies (doc and feed are identical). The model is directly challenged to distinguish 2500 from 3500 RPM signals under identical cutting conditions.

| Pair | Run A (2500 RPM) | Run B (3500 RPM) | Y-doc | Z-doc | Feed |
|------|-----------------|-----------------|-------|-------|------|
| A | s25f3y5z25 | s35f3y5z25 | 0.50 | 0.250 | f3 |
| B | s25f5y25z25 | s35f5y25z25 | 0.25 | 0.250 | f5 |
| C | s25f7y5z125 | s35f7y5z125 | 0.50 | 0.125 | f7 |
| D | s25f3y25z125 | s35f3y25z125 | 0.25 | 0.125 | f3 |

**Test runs: s25f3y5z25, s35f3y5z25, s25f5y25z25, s35f5y25z25, s25f7y5z125, s35f7y5z125, s25f3y25z125, s35f3y25z125** → 24 samples (×3 time windows)

**Train runs: s25f5y5z25, s25f7y5z25, s35f5y5z25, s35f7y5z25, s25f3y25z25, s25f7y25z25, s35f3y25z25, s35f7y25z25, s25f3y5z125, s25f5y5z125, s35f3y5z125, s35f5y5z125, s25f5y25z125, s25f7y25z125, s35f5y25z125, s35f7y25z125** → 48 samples (×3 time windows)

| Dimension | Train | Test |
|-----------|-------|------|
| Speed 2500 / 3500 | 8 / 8 | 4 / 4 |
| Y-doc 0.25 / 0.50 | 8 / 8 | 4 / 4 |
| Z-doc 0.125 / 0.25 | 8 / 8 | 4 / 4 |
| Feed f3 / f5 / f7 | 4 / 6 / 6 | 4 / 2 / 2 |

---

### Split 2 — Feed Model

**Test structure: 2 complete feed triplets + 2 extras**
Each triplet holds out all 3 feed rates at the same (speed × doc) condition, so the model must distinguish f3/f5/f7 from signals that differ only in feed. The training set contains 4 complete triplets (sides 2, 4, 5, 7), maximising the feed discrimination signal during training.

| Group | Runs | Speed | Y-doc | Z-doc | Feeds in test |
|-------|------|-------|-------|-------|---------------|
| Side 1 triplet | s25f3y5z25, s25f5y5z25, s25f7y5z25 | 2500 | 0.50 | 0.250 | f3, f5, f7 |
| Side 8 triplet | s35f3y25z125, s35f5y25z125, s35f7y25z125 | 3500 | 0.25 | 0.125 | f3, f5, f7 |
| Extra | s25f7y25z25 | 2500 | 0.25 | 0.250 | f7 |
| Extra | s35f3y5z125 | 3500 | 0.50 | 0.125 | f3 |

**Test runs: s25f3y5z25, s25f5y5z25, s25f7y5z25, s25f7y25z25, s35f3y5z125, s35f3y25z125, s35f5y25z125, s35f7y25z125** → 24 samples (×3 time windows)

**Train runs: s35f3y5z25, s35f5y5z25, s35f7y5z25, s25f3y25z25, s25f5y25z25, s35f3y25z25, s35f5y25z25, s35f7y25z25, s25f3y5z125, s25f5y5z125, s25f7y5z125, s35f5y5z125, s35f7y5z125, s25f3y25z125, s25f5y25z125, s25f7y25z125** → 48 samples (×3 time windows)

| Dimension | Train | Test |
|-----------|-------|------|
| Speed 2500 / 3500 | 8 / 8 | 4 / 4 |
| Y-doc 0.25 / 0.50 | 8 / 8 | 4 / 4 |
| Z-doc 0.125 / 0.25 | 8 / 8 | 4 / 4 |
| Feed f3 / f5 / f7 | 5 / 6 / 5 | 3 / 2 / 3 |

---

### Split 3 — Doc Model

**Test structure: 2 doc-quadruplets**
Each quadruplet holds out all 4 (Y-doc × Z-doc) combinations at the same (speed × feed), so the only thing varying within each group is depth of cut. This directly probes whether the model can discriminate doc from signals where speed and feed are fixed.

| Group | Runs | Speed | Feed | Docs covered |
|-------|------|-------|------|--------------|
| 2500 / f3 quad | s25f3y5z25, s25f3y25z25, s25f3y5z125, s25f3y25z125 | 2500 | f3 | all 4 Y/Z-doc combos |
| 3500 / f5 quad | s35f5y5z25, s35f5y25z25, s35f5y5z125, s35f5y25z125 | 3500 | f5 | all 4 Y/Z-doc combos |

**Test runs: s25f3y5z25, s35f5y5z25, s25f3y25z25, s35f5y25z25, s25f3y5z125, s35f5y5z125, s25f3y25z125, s35f5y25z125** → 24 samples (×3 time windows)

**Train runs: s25f5y5z25, s25f7y5z25, s35f3y5z25, s35f7y5z25, s25f5y25z25, s25f7y25z25, s35f3y25z25, s35f7y25z25, s25f5y5z125, s25f7y5z125, s35f3y5z125, s35f7y5z125, s25f5y25z125, s25f7y25z125, s35f3y25z125, s35f7y25z125** → 48 samples (×3 time windows)

| Dimension | Train | Test |
|-----------|-------|------|
| Speed 2500 / 3500 | 8 / 8 | 4 / 4 |
| Y-doc 0.25 / 0.50 | 8 / 8 | 4 / 4 |
| Z-doc 0.125 / 0.25 | 8 / 8 | 4 / 4 |
| Feed f3 / f5 / f7 | 4 / 4 / 8 | 4 / 4 / 0 |

---

## Split Comparison Summary

| | Speed split | Feed split | Doc split |
|--|-------------|------------|-----------|
| Test structure | 4 speed-pairs | 2 feed-triplets + 2 extras | 2 doc-quadruplets |
| Test isolates | Speed only | Feed only | Doc only |
| Test runs | s25f3y5z25, s35f3y5z25, s25f5y25z25, s35f5y25z25, s25f7y5z125, s35f7y5z125, s25f3y25z125, s35f3y25z125 | s25f3y5z25, s25f5y5z25, s25f7y5z25, s25f7y25z25, s35f3y5z125, s35f3y25z125, s35f5y25z125, s35f7y25z125 | s25f3y5z25, s35f5y5z25, s25f3y25z25, s35f5y25z25, s25f3y5z125, s35f5y5z125, s25f3y25z125, s35f5y25z125 |
| Train runs | s25f5y5z25,s25f7y5z25,s35f5y5z25,s35f7y5z25,s25f3y25z25,s25f7y25z25,s35f3y25z25,s35f7y25z25,s25f3y5z125,s25f5y5z125,s35f3y5z125,s35f5y5z125,s25f5y25z125,s25f7y25z125,s35f5y25z125,s35f7y25z125 | s35f3y5z25,s35f5y5z25,s35f7y5z25,s25f3y25z25,s25f5y25z25,s35f3y25z25,s35f5y25z25,s35f7y25z25,s25f3y5z125,s25f5y5z125,s25f7y5z125,s35f5y5z125,s35f7y5z125,s25f3y25z125,s25f5y25z125,s25f7y25z125 | s25f5y5z25,s25f7y5z25,s35f3y5z25,s35f7y5z25,s25f5y25z25,s25f7y25z25,s35f3y25z25,s35f7y25z25,s25f5y5z125,s25f7y5z125,s35f3y5z125,s35f7y5z125,s25f5y25z125,s25f7y25z125,s35f3y25z125,s35f7y25z125 |
| f7 in test | 2 runs | 3 runs | 0 runs |

All splits have **48 training samples and 24 test samples**. Speed and Y/Z-doc are perfectly balanced (4/4) in every test set. Feed is intentionally uneven across splits because each split's structure prioritises a different axis of variation.
