### resnet18_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Med | Low | Low | Low | Low | N |
| run21 | Hi | Low | Low | Low | Low | Low | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Med | Low | Low | N |
| run31 | Med | Med | Low | Low | Low | Low | N |
| run36 | Hi | Low | Low | Med | Low | Low | N |
| run37 | Low | Med | Med | Low | Med | Low | ~ |
| run45 | Med | Med | Med | Low | Med | Med | Y |
| run5 | Hi | Med | Med | Low | Med | Med | N |
| run7 | Low | Low | Med | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **41.7%** (5/12)