### efficientnet_b0_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Med | Med | Med | Med | N |
| run17 | Med | Low | Med | Low | Low | Low | N |
| run21 | Hi | Low | Med | Low | Low | Low | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Med | Med | Med | Med | N |
| run31 | Med | Low | Med | Low | Low | Low | N |
| run36 | Hi | Low | Low | Low | Low | Low | N |
| run37 | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Low | Med | Med | Med | Med | Y |
| run5 | Hi | Low | Med | Hi | Low | Low | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Med | Low | Low | Low | N |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)