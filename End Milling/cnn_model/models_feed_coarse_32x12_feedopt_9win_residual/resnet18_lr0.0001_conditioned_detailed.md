### resnet18_lr0.0001_conditioned  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Med | Low | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run17 | Med | Low | Hi | Low | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Low | Med | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Hi | Med | Med | Med | Med | Med | Low | Med | Med | N |
| run31 | Med | Low | Hi | Med | Low | Med | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Low | Med | Low | Med | Hi | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run37 | Low | Low | Med | Hi | Low | Med | Med | Med | Med | Med | Med | Med | N |
| run45 | Med | Med | Low | Low | Med | Med | Hi | Hi | Med | Med | Med | Low | Y |
| run5 | Hi | Med | Low | Low | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Med | Low | Low | Med | Low | Low | Med | Low | Low | Y |
| run9 | Med | Low | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **48.1%** (52/108)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **58.3%** (7/12)