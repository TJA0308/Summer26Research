### resnet18_lr0.001  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Med | Low | Low | Low | Low | N |
| run21 | Hi | Med | Med | Low | Med | Med | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Low | Low | Low | N |
| run31 | Med | Low | Med | Med | Med | Med | Y |
| run36 | Hi | Low | Low | Low | Low | Low | N |
| run37 | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Low | Med | Low | Low | Low | N |
| run5 | Hi | Hi | Med | Med | Med | Med | N |
| run7 | Low | Low | Low | Med | Low | Med | Y |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **52.8%** (19/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **41.7%** (5/12)