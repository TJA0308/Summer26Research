### resnet50_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Med | Low | Low | Low | Low | N |
| run21 | Hi | Med | Low | Low | Low | Low | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Low | Med | Hi | Low | Y |
| run31 | Med | Med | Low | Hi | Med | Hi | Y |
| run36 | Hi | Low | Low | Hi | Low | Low | N |
| run37 | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Med | Low | Hi | Med | Med | Y |
| run5 | Hi | Low | Low | Low | Low | Low | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **47.2%** (17/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **41.7%** (5/12)