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

Each cutting condition is identified as **[side][feed]**, where:
- **Side (1–8):** unique (speed × Y-doc × Z-doc) combination
- **Feed letter:** a = f3, b = f5, c = f7
- **Time window:** appended as 1, 2, or 3 (e.g. 1a-1, 1a-2, 1a-3)

### Side — Parameter Mapping

| Side | Speed (RPM) | Y-doc (in) | Z-doc (in) | Runs |
|------|-------------|-----------|-----------|------|
| 1 | 2500 | 0.50 | 0.250 | 1a, 1b, 1c |
| 2 | 3500 | 0.50 | 0.250 | 2a, 2b, 2c |
| 3 | 2500 | 0.25 | 0.250 | 3a, 3b, 3c |
| 4 | 3500 | 0.25 | 0.250 | 4a, 4b, 4c |
| 5 | 2500 | 0.50 | 0.125 | 5a, 5b, 5c |
| 6 | 3500 | 0.50 | 0.125 | 6a, 6b, 6c |
| 7 | 2500 | 0.25 | 0.125 | 7a, 7b, 7c |
| 8 | 3500 | 0.25 | 0.125 | 8a, 8b, 8c |

Within each side: a = f3, b = f5, c = f7.

---

## Three Model Splits (48 train / 24 test)

Each split is designed so the test set directly isolates the target feature as the only varying factor, giving each model the clearest possible evaluation signal.

---

### Split 1 — Speed Model

**Test structure: 4 matched speed-pairs**
Within each pair, speed is the only thing that varies (doc and feed are identical). The model is directly challenged to distinguish 2500 from 3500 RPM signals under identical cutting conditions.

| Pair | Run A (2500 RPM) | Run B (3500 RPM) | Y-doc | Z-doc | Feed |
|------|-----------------|-----------------|-------|-------|------|
| A | 1a | 2a | 0.50 | 0.250 | f3 |
| B | 3b | 4b | 0.25 | 0.250 | f5 |
| C | 5c | 6c | 0.50 | 0.125 | f7 |
| D | 7a | 8a | 0.25 | 0.125 | f3 |

**Test runs: 1a, 2a, 3b, 4b, 5c, 6c, 7a, 8a** → 24 samples (×3 time windows)

**Train runs: 1b, 1c, 2b, 2c, 3a, 3c, 4a, 4c, 5a, 5b, 6a, 6b, 7b, 7c, 8b, 8c** → 48 samples (×3 time windows)

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
| Side 1 triplet | 1a, 1b, 1c | 2500 | 0.50 | 0.250 | f3, f5, f7 |
| Side 8 triplet | 8a, 8b, 8c | 3500 | 0.25 | 0.125 | f3, f5, f7 |
| Extra | 3c | 2500 | 0.25 | 0.250 | f7 |
| Extra | 6a | 3500 | 0.50 | 0.125 | f3 |

**Test runs: 1a, 1b, 1c, 3c, 6a, 8a, 8b, 8c** → 24 samples (×3 time windows)

**Train runs: 2a, 2b, 2c, 3a, 3b, 4a, 4b, 4c, 5a, 5b, 5c, 6b, 6c, 7a, 7b, 7c** → 48 samples (×3 time windows)

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
| 2500 / f3 quad | 1a, 3a, 5a, 7a | 2500 | f3 | all 4 Y/Z-doc combos |
| 3500 / f5 quad | 2b, 4b, 6b, 8b | 3500 | f5 | all 4 Y/Z-doc combos |

**Test runs: 1a, 2b, 3a, 4b, 5a, 6b, 7a, 8b** → 24 samples (×3 time windows)

**Train runs: 1b, 1c, 2a, 2c, 3b, 3c, 4a, 4c, 5b, 5c, 6a, 6c, 7b, 7c, 8a, 8c** → 48 samples (×3 time windows)

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
| Test runs | 1a, 2a, 3b, 4b, 5c, 6c, 7a, 8a | 1a, 1b, 1c, 3c, 6a, 8a, 8b, 8c | 1a, 2b, 3a, 4b, 5a, 6b, 7a, 8b |
| Train runs | 1b,1c,2b,2c,3a,3c,4a,4c,5a,5b,6a,6b,7b,7c,8b,8c | 2a,2b,2c,3a,3b,4a,4b,4c,5a,5b,5c,6b,6c,7a,7b,7c | 1b,1c,2a,2c,3b,3c,4a,4c,5b,5c,6a,6c,7b,7c,8a,8c |
| f7 in test | 2 runs | 3 runs | 0 runs |

All splits have **48 training samples and 24 test samples**. Speed and Y/Z-doc are perfectly balanced (4/4) in every test set. Feed is intentionally uneven across splits because each split's structure prioritises a different axis of variation.
