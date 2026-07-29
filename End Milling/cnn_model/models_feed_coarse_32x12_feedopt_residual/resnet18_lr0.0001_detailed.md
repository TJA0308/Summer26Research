### resnet18_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Med | Low | Low | Y |
| run17 | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Med | Med | Med | Med | N |
| run25 | Low | Low | Low | Med | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Med | Med | Med | Med | N |
| run37 | Low | Med | Low | Med | Med | Med | N |
| run45 | Med | Low | Low | Med | Low | Low | N |
| run5 | Hi | Low | Low | Med | Low | Low | N |
| run7 | Low | Low | Low | Med | Low | Med | Y |
| run9 | Med | Med | Low | Med | Med | Med | Y |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **41.7%** (5/12)