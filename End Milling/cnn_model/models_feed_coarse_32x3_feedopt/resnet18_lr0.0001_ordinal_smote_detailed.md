### resnet18_lr0.0001_ordinal_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Hi | Hi | Hi | N |
| run17 | Med | Hi | Med | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run25 | Low | Low | Hi | Hi | Hi | Hi | N |
| run3 | Hi | Med | Med | Hi | Med | Med | N |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Low | Med | Hi | Low | ~ |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Hi | Hi | Hi | Hi | N |
| run9 | Med | Low | Med | Med | Med | Med | Y |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **50.0%** (6/12)