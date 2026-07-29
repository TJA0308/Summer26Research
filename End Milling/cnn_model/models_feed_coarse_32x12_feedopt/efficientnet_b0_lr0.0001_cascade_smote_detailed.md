### efficientnet_b0_lr0.0001_cascade_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Med | Med | Med | Med | N |
| run17 | Med | Hi | Hi | Med | Hi | Hi | N |
| run21 | Hi | Med | Hi | Med | Med | Med | N |
| run25 | Low | Hi | Med | Med | Med | Med | N |
| run3 | Hi | Med | Hi | Med | Med | Med | N |
| run31 | Med | Med | Hi | Low | Med | Low | Y |
| run36 | Hi | Med | Hi | Med | Med | Med | N |
| run37 | Low | Low | Hi | Hi | Hi | Hi | N |
| run45 | Med | Med | Med | Hi | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Med | Med | N |
| run7 | Low | Hi | Hi | Low | Hi | Hi | N |
| run9 | Med | Hi | Hi | Low | Hi | Hi | N |

Window accuracy: **27.8%** (10/36)
Run hard-vote accuracy: **16.7%** (2/12)
Run soft-vote accuracy: **8.3%** (1/12)