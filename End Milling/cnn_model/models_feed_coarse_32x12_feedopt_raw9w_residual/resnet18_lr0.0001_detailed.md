### resnet18_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw9w_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Med | Med | Med | Med | Low | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Hi | Hi | Low | Med | Med | Low | Med | Low | Hi | Med | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Low | Med | Low | Med | Med | Low | Hi | Med | Med | Med | N |
| run31 | Med | Med | Low | Med | Med | Low | Med | Med | Hi | Med | Med | Med | Y |
| run36 | Hi | Med | Med | Med | Med | Low | Hi | Low | Low | Low | Med | Med | N |
| run37 | Low | Low | Low | Low | Low | Med | Low | Low | Low | Med | Low | Low | Y |
| run45 | Med | Med | Low | Low | Low | Med | Low | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run7 | Low | Low | Low | Low | Low | Low | Low | Low | Hi | Hi | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | Hi | Low | Low | Low | Low | Low | N |

Window accuracy: **50.9%** (55/108)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **58.3%** (7/12)