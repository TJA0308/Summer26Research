### resnet18_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Low | Hi | Low | Low | Low | N |
| run37 | Low | Med | Med | Low | Med | Low | ~ |
| run45 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Med | Low | Med | Med | Y |

Window accuracy: **58.3%** (21/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **66.7%** (8/12)