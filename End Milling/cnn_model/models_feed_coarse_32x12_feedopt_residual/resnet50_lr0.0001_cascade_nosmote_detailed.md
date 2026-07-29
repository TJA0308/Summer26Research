### resnet50_lr0.0001_cascade_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Med | Low | Low | Low | Med | ~ |
| run21 | Hi | Med | Low | Low | Low | Low | N |
| run25 | Low | Low | Med | Med | Med | Med | N |
| run3 | Hi | Med | Med | Low | Med | Med | N |
| run31 | Med | Med | Low | Low | Low | Low | N |
| run36 | Hi | Med | Low | Low | Low | Low | N |
| run37 | Low | Med | Low | Low | Low | Low | Y |
| run45 | Med | Med | Low | Med | Med | Med | Y |
| run5 | Hi | Low | Low | Low | Low | Low | N |
| run7 | Low | Med | Med | Low | Med | Low | ~ |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **30.6%** (11/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **41.7%** (5/12)