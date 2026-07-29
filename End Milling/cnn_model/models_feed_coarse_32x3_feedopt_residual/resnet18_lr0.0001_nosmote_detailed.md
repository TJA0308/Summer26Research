### resnet18_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Low | Med | Hi | N |
| run17 | Med | Low | Hi | Med | Low | Low | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Hi | Hi | Hi | Med | Y |
| run31 | Med | Hi | Hi | Med | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Low | Low | Med | Low | Low | N |
| run5 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Med | Low | Med | Med | Y |

Window accuracy: **61.1%** (22/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **50.0%** (6/12)