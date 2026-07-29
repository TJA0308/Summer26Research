### resnet18_lr0.001_cascade_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Hi | Med | Med | N |
| run17 | Med | Low | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Hi | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Hi | Med | Hi | Y |
| run36 | Hi | Hi | Low | Med | Hi | Low | Y |
| run37 | Low | Hi | Low | Low | Low | Low | Y |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Low | Low | Hi | Low | Low | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **50.0%** (6/12)