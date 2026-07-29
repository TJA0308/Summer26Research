### resnet18_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Low | Low | Low | Hi | Low | Low | Low | Hi | Low | Low | Y |
| run17 | Med | Hi | Low | Low | Low | Low | Hi | Low | Low | Low | Low | Low | N |
| run21 | Hi | Low | Low | Low | Low | Low | Low | Low | Low | Hi | Low | Low | N |
| run25 | Low | Hi | Low | Low | Low | Low | Low | Low | Hi | Low | Low | Low | Y |
| run3 | Hi | Hi | Low | Low | Hi | Hi | Hi | Low | Low | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Low | Low | Low | Low | Low | Low | Low | Hi | Low | Low | N |
| run36 | Hi | Hi | Hi | Low | Hi | Low | Hi | Hi | Hi | Low | Hi | Hi | Y |
| run37 | Low | Low | Hi | Hi | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Hi | Hi | Low | Low | Hi | Low | Low | Low | Hi | Low | Hi | N |
| run5 | Hi | Hi | Low | Hi | Hi | Hi | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Hi | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **44.4%** (48/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)