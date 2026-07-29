### resnet50_lr0.001_conditioned  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Hi | Med | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run25 | Low | Low | Low | Hi | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Hi | Low | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Low | Low | Low | Hi | Y |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Med | Hi | Hi | Med | Y |
| run7 | Low | Low | Med | Low | Low | Low | Y |
| run9 | Med | Med | Med | Low | Med | Low | Y |

Window accuracy: **52.8%** (19/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **41.7%** (5/12)