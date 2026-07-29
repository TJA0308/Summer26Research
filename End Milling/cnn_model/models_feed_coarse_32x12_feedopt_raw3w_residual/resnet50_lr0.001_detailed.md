### resnet50_lr0.001  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Low | Med | Hi | Med | N |
| run17 | Med | Med | Low | Med | Med | Med | Y |
| run21 | Hi | Med | Hi | Med | Med | Med | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Hi | Med | Hi | Med | Y |
| run31 | Med | Med | Med | Hi | Med | Med | Y |
| run36 | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Low | Low | Low | Low | Y |
| run45 | Med | Med | Med | Hi | Med | Hi | Y |
| run5 | Hi | Med | Hi | Med | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Med | Low | Low | Low | N |

Window accuracy: **61.1%** (22/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **50.0%** (6/12)