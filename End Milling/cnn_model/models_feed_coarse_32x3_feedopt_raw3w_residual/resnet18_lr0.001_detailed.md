### resnet18_lr0.001  |  target=feed_coarse  |  scalogram=32x3_feedopt_raw3w_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Low | Med | Med | N |
| run17 | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Med | Med | Hi | Med | Med | Y |
| run5 | Hi | Hi | Med | Med | Med | Med | N |
| run7 | Low | Low | Med | Med | Med | Low | ~ |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **61.1%** (22/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **66.7%** (8/12)