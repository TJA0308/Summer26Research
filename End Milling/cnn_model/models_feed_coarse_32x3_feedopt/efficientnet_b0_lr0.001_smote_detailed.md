### efficientnet_b0_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Med | Med | Med | N |
| run17 | Med | Hi | Med | Hi | Hi | Med | ~ |
| run21 | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run25 | Low | Med | Med | Med | Med | Med | N |
| run3 | Hi | Hi | Low | Med | Hi | Med | Y |
| run31 | Med | Med | Med | Hi | Med | Med | Y |
| run36 | Hi | Med | Med | Hi | Med | Med | N |
| run37 | Low | Hi | Hi | Med | Hi | Hi | N |
| run45 | Med | Hi | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Low | Med | Hi | Med | Y |
| run7 | Low | Med | Hi | Low | Med | Low | ~ |
| run9 | Med | Hi | Med | Med | Med | Med | Y |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)