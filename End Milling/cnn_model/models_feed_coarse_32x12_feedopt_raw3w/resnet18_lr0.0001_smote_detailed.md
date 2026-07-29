### resnet18_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Med | Low | Low | Low | Y |
| run17 | Med | Med | Low | Med | Med | Med | Y |
| run21 | Hi | Med | Med | Low | Med | Med | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Low | Med | Med | Y |
| run36 | Hi | Low | Low | Med | Low | Med | N |
| run37 | Low | Med | Med | Low | Med | Med | N |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Low | Med | Low | Low | Low | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Low | Med | Med | Med | Y |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)