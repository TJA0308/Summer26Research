### efficientnet_b0_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_raw3w  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Low | Hi | Hi | Hi | N |
| run17 | Med | Low | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Med | Med | Med | Med | Med | N |
| run25 | Low | Hi | Low | Hi | Hi | Hi | N |
| run3 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Med | Med | Med | Med | Y |
| run36 | Hi | Low | Low | Hi | Low | Low | N |
| run37 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Hi | Low | Low | Y |
| run9 | Med | Med | Med | Hi | Med | Med | Y |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)