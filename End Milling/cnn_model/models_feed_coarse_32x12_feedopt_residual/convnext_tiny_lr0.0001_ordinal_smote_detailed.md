### convnext_tiny_lr0.0001_ordinal_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Med | Med | Med | Med | N |
| run17 | Med | Hi | Hi | Med | Hi | Med | ~ |
| run21 | Hi | Med | Med | Med | Med | Med | N |
| run25 | Low | Med | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Low | Med | Hi | Low | Med | N |
| run37 | Low | Med | Med | Med | Med | Med | N |
| run45 | Med | Low | Med | Low | Low | Low | N |
| run5 | Hi | Low | Med | Med | Med | Med | N |
| run7 | Low | Med | Med | Med | Med | Med | N |
| run9 | Med | Med | Med | Low | Med | Med | Y |

Window accuracy: **30.6%** (11/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **33.3%** (4/12)