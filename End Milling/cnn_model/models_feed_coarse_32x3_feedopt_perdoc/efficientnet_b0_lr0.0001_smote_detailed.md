### efficientnet_b0_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_perdoc  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Med | Low | Low | Low | Low | N |
| run21 | Hi | Low | Med | Low | Low | Low | N |
| run25 | Low | Med | Med | Low | Med | Med | N |
| run3 | Hi | Low | Low | Low | Low | Low | N |
| run31 | Med | Low | Low | Low | Low | Low | N |
| run36 | Hi | Low | Low | Med | Low | Low | N |
| run37 | Low | Low | Med | Low | Low | Low | Y |
| run45 | Med | Low | Low | Med | Low | Low | N |
| run5 | Hi | Low | Low | Low | Low | Low | N |
| run7 | Low | Low | Med | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **27.8%** (10/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **25.0%** (3/12)