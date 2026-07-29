### resnet50_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Low | Med | Hi | Med | Y |
| run25 | Low | Med | Med | Hi | Med | Med | N |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Med | Hi | Med | Med | N |
| run37 | Low | Low | Low | Med | Low | Low | Y |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Hi | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Med | Med | Med | Med | Y |

Window accuracy: **52.8%** (19/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **50.0%** (6/12)