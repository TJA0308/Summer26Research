### resnet50_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Low | Med | Med | Med | Med | Y |
| run21 | Hi | Low | Med | Med | Med | Low | N |
| run25 | Low | Low | Low | Med | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Low | Med | Med | Y |
| run36 | Hi | Med | Med | Med | Med | Med | N |
| run37 | Low | Low | Low | Med | Low | Med | Y |
| run45 | Med | Med | Low | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Low | Med | Med | N |
| run7 | Low | Low | Low | Med | Low | Low | Y |
| run9 | Med | Low | Med | Low | Low | Med | ~ |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)