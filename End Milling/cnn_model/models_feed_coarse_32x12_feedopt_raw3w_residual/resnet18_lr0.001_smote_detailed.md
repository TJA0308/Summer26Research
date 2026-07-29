### resnet18_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Med | Low | Low | Y |
| run17 | Med | Med | Low | Med | Med | Med | Y |
| run21 | Hi | Med | Hi | Med | Med | Med | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Low | Low | Low | Med | Y |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Med | Low | Low | Low | N |

Window accuracy: **63.9%** (23/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **58.3%** (7/12)