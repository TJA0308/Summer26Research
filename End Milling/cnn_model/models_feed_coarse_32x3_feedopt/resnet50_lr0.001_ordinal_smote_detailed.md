### resnet50_lr0.001_ordinal_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Med | Med | Med | Med | N |
| run25 | Low | Low | Hi | Hi | Hi | Hi | N |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Hi | Hi | Hi | Med | Y |
| run37 | Low | Med | Med | Med | Med | Med | N |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Med | Low | Low | Med | Y |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **55.6%** (20/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **41.7%** (5/12)