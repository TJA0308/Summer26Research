### resnet50_lr0.001_cascade_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Low | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Hi | Hi | Hi | Med | Y |
| run25 | Low | Med | Med | Med | Med | Med | N |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Low | Med | Med | Med | Med | N |
| run37 | Low | Med | Hi | Med | Med | Med | N |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Low | Med | Hi | Low | Med | N |
| run7 | Low | Med | Med | Low | Med | Med | N |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **33.3%** (4/12)