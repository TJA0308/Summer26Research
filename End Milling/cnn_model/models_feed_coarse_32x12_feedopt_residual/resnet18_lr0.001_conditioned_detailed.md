### resnet18_lr0.001_conditioned  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Med | Med | Med | Hi | Y |
| run21 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Med | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Low | Med | Med | Med | N |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Med | Med | Hi | Med | Med | N |
| run9 | Med | Med | Med | Low | Med | Low | Y |

Window accuracy: **58.3%** (21/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **50.0%** (6/12)