### resnet18_lr0.001_cascade_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Low | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Med | Hi | Med | Med | N |
| run25 | Low | Low | Low | Med | Low | Low | Y |
| run3 | Hi | Low | Med | Med | Med | Med | N |
| run31 | Med | Low | Med | Hi | Low | Med | ~ |
| run36 | Hi | Low | Med | Med | Med | Med | N |
| run37 | Low | Med | Low | Low | Low | Low | Y |
| run45 | Med | Med | Low | Low | Low | Med | ~ |
| run5 | Hi | Low | Med | Med | Med | Med | N |
| run7 | Low | Low | Low | Med | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **30.6%** (11/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **50.0%** (6/12)