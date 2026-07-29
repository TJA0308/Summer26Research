### resnet50_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Low | Low | Low | Low | Y |
| run17 | Med | Med | Low | Low | Low | Low | N |
| run21 | Hi | Med | Low | Low | Low | Low | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Low | Low | Low | N |
| run31 | Med | Low | Low | Med | Low | Low | N |
| run36 | Hi | Low | Low | Med | Low | Low | N |
| run37 | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Low | Med | Med | Med | Low | Y |
| run5 | Hi | Low | Low | Low | Low | Low | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Low | Med | Med | Med | Y |

Window accuracy: **47.2%** (17/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **41.7%** (5/12)