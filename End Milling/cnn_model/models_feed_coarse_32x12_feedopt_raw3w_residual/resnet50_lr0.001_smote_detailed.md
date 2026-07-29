### resnet50_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Med | Low | Low | Y |
| run17 | Med | Low | Med | Hi | Low | Low | N |
| run21 | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Low | Med | Hi | Med | Y |
| run31 | Med | Low | Med | Hi | Low | Hi | N |
| run36 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Med | Low | Med | Med | N |
| run45 | Med | Low | Med | Hi | Low | Low | N |
| run5 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Med | Low | Low | Y |
| run9 | Med | Low | Hi | Low | Low | Low | N |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **50.0%** (6/12)