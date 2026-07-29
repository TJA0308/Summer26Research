### resnet18_lr0.0001  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Low | Hi | Low | Hi | Hi | Low | Hi | Hi | Hi | N |
| run17 | Med | Hi | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Hi | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Low | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Low | Low | Low | Low | Low | Hi | Hi | Hi | Hi | Low | Hi | Y |
| run45 | Med | Low | Low | Low | Low | Low | Med | Med | Low | Med | Low | Low | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Hi | Low | Low | Hi | Hi | Hi | Low | Low | Y |
| run9 | Med | Low | Hi | Low | Hi | Hi | Low | Med | Med | Low | Low | Low | N |

Window accuracy: **53.7%** (58/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **50.0%** (6/12)