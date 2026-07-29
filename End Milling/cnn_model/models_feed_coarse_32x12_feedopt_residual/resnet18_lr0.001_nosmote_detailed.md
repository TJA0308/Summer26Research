### resnet18_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Low | Low | Low | Low | Y |
| run17 | Med | Hi | Low | Low | Low | Hi | N |
| run21 | Hi | Hi | Med | Hi | Hi | Hi | Y |
| run25 | Low | Hi | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Med | Med | Med | Med | N |
| run31 | Med | Hi | Med | Med | Med | Hi | Y |
| run36 | Hi | Hi | Med | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Low | Low | Low | Low | Y |
| run45 | Med | Hi | Low | Low | Low | Low | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Hi | Low | Low | Low | Med | Y |
| run9 | Med | Hi | Low | Low | Low | Low | N |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **50.0%** (6/12)