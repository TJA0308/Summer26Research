### resnet18_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Hi | Med | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Hi | Hi | Hi | Hi | Med | Med | Med | Med | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Med | Low | Med | Med | Hi | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Hi | Hi | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Hi | Hi | Med | Hi | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run37 | Low | Low | Hi | Med | Low | Med | Med | Low | Low | Low | Low | Med | Y |
| run45 | Med | Med | Med | Low | Med | Hi | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Hi | Med | Med | Hi | Med | Med | Med | Med | Med | Med | Med | N |
| run9 | Med | Hi | Hi | Med | Med | Med | Med | Low | Low | Low | Med | Med | Y |

Window accuracy: **51.9%** (56/108)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **58.3%** (7/12)