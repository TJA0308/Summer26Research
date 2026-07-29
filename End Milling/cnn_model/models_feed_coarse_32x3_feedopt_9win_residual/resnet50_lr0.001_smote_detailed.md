### resnet50_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Low | Med | Low | Low | Low | Low | Low | Med | Low | Low | Y |
| run17 | Med | Med | Hi | Low | Med | Low | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Low | Med | Med | Med | Med | Hi | Hi | Hi | Low | Med | Med | N |
| run25 | Low | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Hi | Med | Med | Low | Hi | Low | Hi | Low | Med | Low | N |
| run37 | Low | Low | Med | Med | Med | Med | Med | Med | Med | Low | Med | Med | N |
| run45 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run5 | Hi | Low | Low | Med | Med | Med | Hi | Med | Med | Med | Med | Med | N |
| run7 | Low | Med | Med | Low | Low | Low | Med | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Med | Low | Med | Low | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **46.3%** (50/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)