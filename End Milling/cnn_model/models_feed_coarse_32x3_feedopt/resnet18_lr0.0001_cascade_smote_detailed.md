### resnet18_lr0.0001_cascade_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Hi | Med | Med | N |
| run17 | Med | Med | Med | Hi | Med | Med | Y |
| run21 | Hi | Med | Med | Hi | Med | Med | N |
| run25 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run3 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Med | Med | Hi | Med | Hi | Y |
| run36 | Hi | Med | Low | Hi | Med | Hi | ~ |
| run37 | Low | Med | Med | Hi | Med | Hi | N |
| run45 | Med | Med | Med | Hi | Med | Hi | Y |
| run5 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Hi | Low | Hi | Y |
| run9 | Med | Low | Hi | Hi | Hi | Hi | N |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **33.3%** (4/12)