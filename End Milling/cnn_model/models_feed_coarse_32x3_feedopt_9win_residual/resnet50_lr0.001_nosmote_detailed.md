### resnet50_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Low | Hi | Med | Low | Low | Low | Low | Low | Hi | Y |
| run17 | Med | Hi | Hi | Hi | Low | Hi | Hi | Hi | Med | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Hi | Hi | Hi | Hi | Low | Low | Y |
| run3 | Hi | Hi | Med | Low | Low | Low | Low | Low | Med | Low | Low | Med | N |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Low | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Low | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Low | Hi | Low | Low | Low | Low | Low | Hi | Low | Low | Y |
| run45 | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Low | Hi | Hi | Med | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Low | Low | Hi | Low | Med | Med | Low | Low | Y |
| run9 | Med | Low | Low | Med | Med | Hi | Hi | Hi | Hi | Low | Hi | Hi | N |

Window accuracy: **46.3%** (50/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **50.0%** (6/12)