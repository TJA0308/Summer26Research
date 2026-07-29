### resnet18_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Hi | Med | Hi | Y |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **47.2%** (17/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **41.7%** (5/12)