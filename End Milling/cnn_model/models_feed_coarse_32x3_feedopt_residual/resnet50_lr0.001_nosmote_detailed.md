### resnet50_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Low | Med | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Med | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Hi | Med | Hi | Hi | N |
| run36 | Hi | Hi | Med | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Low | Med | Hi | Hi | N |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Med | Med | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **55.6%** (20/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)