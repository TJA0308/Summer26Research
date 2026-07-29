### resnet50_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Low | Low | Low | Low | Y |
| run17 | Med | Med | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Med | Med | Med | Med | N |
| run25 | Low | Hi | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Med | Hi | Hi | Hi | N |
| run36 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Med | Hi | Med | Med | Med | N |
| run9 | Med | Low | Hi | Med | Low | Med | ~ |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **50.0%** (6/12)