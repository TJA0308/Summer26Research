### resnet18_lr0.001_cascade_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Hi | Med | Med | N |
| run17 | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Med | Med | Med | Med | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run37 | Low | Med | Low | Hi | Med | Hi | N |
| run45 | Med | Med | Med | Low | Med | Low | Y |
| run5 | Hi | Med | Hi | Med | Med | Med | N |
| run7 | Low | Low | Hi | Low | Low | Low | Y |
| run9 | Med | Med | Low | Low | Low | Low | N |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **41.7%** (5/12)