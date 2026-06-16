# Holdout Test Run Selection — Rationale

This document explains which runs were held out for testing in each model and **why those specific runs were chosen**. All test runs were excluded before any training and were never used to update model weights.

---

## Guiding Principles

Three constraints shaped every holdout set:

1. **Class balance** — each target class must appear in the test set, so a single run-level failure cannot distort the reported accuracy by an entire class.
2. **Covariate diversity** — test runs must span different values of the *other* process parameters (DOC, speed, feed) so the model is forced to classify the target variable independently of confounders. A model that only passes tests at one DOC level may have learned DOC, not speed.
3. **Preserve training data** — with only 45 runs total and up to six classes, each held-out run costs the minority classes disproportionately. The holdout size was chosen to be the minimum that satisfies the two constraints above.

---

## 1. Spindle Speed (5-class: 1500 / 2000 / 3000 / 4000 / 5000 rpm)

**10 test runs — 2 per RPM class**

| Run | Speed | DOC (mm) | Feed (mm/rev) | Why selected |
|-----|-------|----------|---------------|--------------|
| run9  | 1500 rpm | 0.030 | 5 | Mid-DOC representative for 1500 rpm class |
| run22 | 1500 rpm | 0.060 | 3 | High-DOC representative; different feed from run9 |
| run12 | 2000 rpm | 0.030 | 5 | Mid-DOC representative for 2000 rpm class |
| run27 | 2000 rpm | 0.060 | 5 | High-DOC representative; same feed, different DOC |
| run15 | 3000 rpm | 0.030 | 6 | Mid-DOC representative for 3000 rpm class |
| run28 | 3000 rpm | 0.060 | 4 | High-DOC representative; different feed from run15 |
| run2  | 4000 rpm | 0.015 | 6 | Low-DOC representative for 4000 rpm class |
| run16 | 4000 rpm | 0.030 | 5 | Mid-DOC representative; different DOC from run2 |
| run5  | 5000 rpm | 0.015 | 7 | Low-DOC representative for 5000 rpm class |
| run36 | 5000 rpm | 0.060 | 8 | High-DOC representative; opposite end of DOC range from run5 |

**Selection logic:**

Each RPM class appears in three DOC groups (0.015 / 0.030 / 0.060 mm), with three runs per DOC group. Two of those three DOC levels are represented in the holdout for every speed class, ensuring the test set stresses the model across the full DOC range. No DOC level repeats within a speed class, so the model cannot pass the holdout by memorizing DOC-specific patterns.

The specific DOC levels chosen per class:
- **1500 / 2000 / 3000 rpm** → DOC=0.030 and DOC=0.060 held out (DOC=0.015 runs stay in training)
- **4000 / 5000 rpm** → DOC=0.015 and DOC=0.030 or DOC=0.060 held out (the opposite end stays in training)

This produces maximum spread in the held-out covariate space while keeping at least one full DOC group in training for every speed class.

---

## 2. Feed Rate Fine-Grained (6-class: 3 / 4 / 5 / 6 / 7 / 8 mm/rev)

**6 test runs — 1 per feed class**

| Run | Feed (mm/rev) | Speed | DOC (mm) | Why selected |
|-----|--------------|-------|----------|--------------|
| run25 | 3 | 2000 rpm | 0.060 | High-DOC, mid-speed option for the 3 mm/rev class |
| run13 | 4 | 3000 rpm | 0.030 | Mid-DOC, mid-speed; avoids confounding with extreme speeds |
| run31 | 5 | 4000 rpm | 0.060 | High-DOC, high-speed; different speed/DOC from run13 |
| run17 | 6 | 4000 rpm | 0.030 | Mid-DOC at the same speed as run31 to isolate feed effect |
| run5  | 7 | 5000 rpm | 0.015 | Low-DOC, highest speed; maximally different covariate profile |
| run36 | 8 | 5000 rpm | 0.060 | High-DOC, highest speed; same speed as run5, different DOC |

**Selection logic:**

Only 1 test run per class was feasible here. The rarest feed-rate class (8 mm/rev) has just 3 training runs total; holding out more than one would strip the minority class of over 30% of its training data.

Runs were selected to maximize spread in the (speed, DOC) plane:
- The six test runs span all three DOC values (0.015, 0.030, 0.060 mm) and four of five speed levels (2000, 3000, 4000, 5000 rpm).
- No two test runs share the same (speed, DOC) pair, which forces the model to classify feed independently of the dominant RPM spectral structure.
- run17 (6 mm/rev) and run31 (5 mm/rev) deliberately share the same speed (4000 rpm) at different DOC levels — if the model had learned speed rather than feed, both would receive the same prediction.

---

## 3. Surface Roughness Ra (3-class: Smooth / Medium / Rough)

**6 test runs — 2 per Ra class**

| Run | Ra class | Ra (μm) | Speed | DOC (mm) | Why selected |
|-----|---------|---------|-------|----------|--------------|
| run5  | Smooth (Ra<0.7)  | 0.424 | 5000 rpm | 0.015 | Low DOC, high speed; solidly in Smooth range |
| run43 | Smooth (Ra<0.7)  | 0.364 | 3000 rpm | 0.015 | Low DOC, different speed from run5 |
| run7  | Medium (0.7–1.0) | 0.930 | 1500 rpm | 0.030 | Mid DOC, low speed; interior of Medium range |
| run27 | Medium (0.7–1.0) | 0.868 | 2000 rpm | 0.060 | Near the 1.0 upper boundary — deliberate stress test |
| run22 | Rough (Ra>1.0)   | 1.186 | 1500 rpm | 0.060 | High DOC, low speed; modest overshoot above 1.0 boundary |
| run34 | Rough (Ra>1.0)   | 2.084 | 5000 rpm | 0.060 | Extreme Ra value — tests large departures from threshold |

**Selection logic:**

**Smooth class (run5, run43):** Both have DOC=0.015 mm, the lowest DOC level. Shallow cuts produce the finest surface finish, so Smooth-class runs naturally concentrate at low DOC. The two speeds (5000 rpm and 3000 rpm) were chosen to differ substantially, confirming the model generalizes across RPM rather than keying on a single spindle harmonic pattern.

**Medium class (run7, run27):** Two DOC levels (0.030 and 0.060 mm) and two speeds (1500 and 2000 rpm). Run27 is a deliberate boundary probe: Ra=0.868 μm sits only 132 μm below the Rough threshold. A model with an imprecise decision boundary will push this run into Rough — the 3 misclassified windows in run27 (Medium→Rough) confirm this is the hardest point in the test set. Run7 (Ra=0.930 μm) probes from the other side: 70 μm below the boundary and unambiguously Medium.

**Rough class (run22, run34):** Both have DOC=0.060 mm, consistent with high DOC being the primary driver of rough surfaces. The two speeds are at opposite extremes (1500 rpm vs 5000 rpm) to confirm the model is not using a speed proxy for roughness. Run34 (Ra=2.084 μm) is far above the 1.0 threshold; its single misclassified window (Rough→Medium) illustrates why majority voting (9/10 Rough) is necessary even for clear-cut cases.

---

## 4. Feed Rate Coarse (3-class: low / medium / high)

**Same 6 runs as fine-grained feed, re-labeled by group**

| Run | Fine feed | Coarse class | Rationale for reuse |
|-----|----------|--------------|---------------------|
| run25 | 3 mm/rev | low (3–4)    | Interior of low group |
| run13 | 4 mm/rev | low (3–4)    | Near low/medium boundary — stress test |
| run31 | 5 mm/rev | medium (5–6) | Interior of medium group |
| run17 | 6 mm/rev | medium (5–6) | Interior of medium group, different DOC |
| run36 | 8 mm/rev | high (7–8)   | Interior of high group |
| run5  | 7 mm/rev | high (7–8)   | Near high/medium boundary — stress test |

Reusing the same six runs allows a direct, apples-to-apples comparison between the fine-grained and coarse-grained models on identical holdout data. The coarse grouping converts the 6-class problem to 3 classes, but the same run-level ceiling is exposed: run13 (4 mm/rev, bottom of the low group) and run5 (7 mm/rev, top of the high group) fail under coarse labeling for the same reason they fail in the fine-grained case — their CWT signatures are dominated by the RPM harmonic of their respective speeds rather than by chip-load modulation.

---

## Summary Table

| Model | Test runs | Per class | Key covariate spread |
|-------|-----------|-----------|----------------------|
| Speed (5-class) | 10 | 2 | 2 DOC levels per speed class |
| Feed fine (6-class) | 6 | 1 | 3 DOC levels, 4 speed levels across 6 runs |
| Feed coarse (3-class) | 6 | 2 | Same 6 runs re-labeled |
| Roughness (3-class) | 6 | 2 | 2 speeds per class; boundary run (run27) deliberately included |
