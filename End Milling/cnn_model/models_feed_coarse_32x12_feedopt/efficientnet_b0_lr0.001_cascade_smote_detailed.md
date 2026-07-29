### efficientnet_b0_lr0.001_cascade_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Low | Low | Low | Low | Y |
| run17 | Med | Med | Low | Low | Low | Low | N |
| run21 | Hi | Med | Low | Low | Low | Low | N |
| run25 | Low | Med | Low | Med | Med | Med | N |
| run3 | Hi | Med | Low | Low | Low | Low | N |
| run31 | Med | Med | Low | Low | Low | Low | N |
| run36 | Hi | Med | Low | Low | Low | Low | N |
| run37 | Low | Med | Low | Low | Low | Low | Y |
| run45 | Med | Med | Low | Low | Low | Low | N |
| run5 | Hi | Med | Hi | Med | Med | Hi | ~ |
| run7 | Low | Med | Low | Low | Low | Low | Y |
| run9 | Med | Med | Low | Low | Low | Low | N |

Window accuracy: **33.3%** (12/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **33.3%** (4/12)