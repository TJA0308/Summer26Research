### resnet18_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Med | Low | Low | Low | Y |
| run17 | Med | Hi | Med | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Med | Med | Hi | Med | Med | Y |
| run36 | Hi | Med | Hi | Hi | Hi | Med | Y |
| run37 | Low | Hi | Hi | Med | Hi | Med | N |
| run45 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Hi | Hi | Low | Hi | Low | N |

Window accuracy: **58.3%** (21/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **58.3%** (7/12)