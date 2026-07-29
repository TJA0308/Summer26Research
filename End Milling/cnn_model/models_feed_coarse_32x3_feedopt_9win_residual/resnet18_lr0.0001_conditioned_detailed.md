### resnet18_lr0.0001_conditioned  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Hi | Hi | Hi | Hi | Low | Low | Hi | Y |
| run17 | Med | Low | Hi | Hi | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Low | Hi | Low | Y |
| run31 | Med | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Low | Hi | Hi | N |
| run36 | Hi | Low | Hi | Hi | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Low | Low | Low | Low | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Low | Low | Low | Low | Low | Hi | Hi | Hi | Low | Low | Low | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Hi | Low | Low | Low | Low | Low | Hi | Low | Low | Low | Y |
| run9 | Med | Low | Hi | Low | Hi | Low | Low | Hi | Hi | Hi | Hi | Hi | N |

Window accuracy: **51.9%** (56/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **41.7%** (5/12)