### resnet18_lr0.001_cascade_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Hi | Med | Med | N |
| run17 | Med | Hi | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Hi | Med | Med | Med | N |
| run25 | Low | Low | Med | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Low | Hi | Hi | Hi | N |
| run45 | Med | Low | Med | Low | Low | Low | N |
| run5 | Hi | Med | Med | Med | Med | Med | N |
| run7 | Low | Low | Med | Low | Low | Med | Y |
| run9 | Med | Med | Low | Low | Low | Low | N |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **25.0%** (3/12)