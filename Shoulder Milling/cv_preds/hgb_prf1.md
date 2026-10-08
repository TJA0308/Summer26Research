### doc | 32x12 | hgb | group=primary | seed 42

Run-level soft vote over 24 held-out runs (LOCO): accuracy **0.833**, macro-P **0.839**, macro-R **0.833**, macro-F1 **0.833** (window-level macro-F1 0.752)

| Class | Precision | Recall | F1 | Support (runs) |
|---|---|---|---|---|
| 0 | 0.857 | 1.000 | 0.923 | 6 |
| 1 | 0.667 | 0.667 | 0.667 | 6 |
| 2 | 1.000 | 0.833 | 0.909 | 6 |
| 3 | 0.833 | 0.833 | 0.833 | 6 |

Confusion matrix (rows = true, cols = predicted):

```
[[6 0 0 0]
 [1 4 0 1]
 [0 1 5 0]
 [0 1 0 5]]
```

### feed | 32x12 | hgb | group=primary | seed 42

Run-level soft vote over 24 held-out runs (LOCO): accuracy **0.625**, macro-P **0.617**, macro-R **0.625**, macro-F1 **0.615** (window-level macro-F1 0.579)

| Class | Precision | Recall | F1 | Support (runs) |
|---|---|---|---|---|
| 0 | 0.750 | 0.750 | 0.750 | 8 |
| 1 | 0.500 | 0.375 | 0.429 | 8 |
| 2 | 0.600 | 0.750 | 0.667 | 8 |

Confusion matrix (rows = true, cols = predicted):

```
[[6 1 1]
 [2 3 3]
 [0 2 6]]
```

### roughness | 32x12 | hgb | group=primary | seed 42

Run-level soft vote over 24 held-out runs (LOCO): accuracy **0.583**, macro-P **0.583**, macro-R **0.583**, macro-F1 **0.583** (window-level macro-F1 0.610)

| Class | Precision | Recall | F1 | Support (runs) |
|---|---|---|---|---|
| 0 | 0.583 | 0.583 | 0.583 | 12 |
| 1 | 0.583 | 0.583 | 0.583 | 12 |

Confusion matrix (rows = true, cols = predicted):

```
[[7 5]
 [5 7]]
```

### speed | 32x12 | hgb | group=primary | seed 42

Run-level soft vote over 24 held-out runs (LOCO): accuracy **0.917**, macro-P **0.929**, macro-R **0.917**, macro-F1 **0.916** (window-level macro-F1 0.902)

| Class | Precision | Recall | F1 | Support (runs) |
|---|---|---|---|---|
| 0 | 0.857 | 1.000 | 0.923 | 12 |
| 1 | 1.000 | 0.833 | 0.909 | 12 |

Confusion matrix (rows = true, cols = predicted):

```
[[12  0]
 [ 2 10]]
```
