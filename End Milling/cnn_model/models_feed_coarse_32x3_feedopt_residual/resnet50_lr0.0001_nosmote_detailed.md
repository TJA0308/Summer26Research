### resnet50_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Med | Hi | Hi | Hi | Med | ~ |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Med | Med | Hi | Med | Med | N |
| run3 | Hi | Med | Med | Hi | Med | Med | N |
| run31 | Med | Med | Hi | Med | Med | Med | Y |
| run36 | Hi | Med | Med | Hi | Med | Hi | ~ |
| run37 | Low | Med | Hi | Hi | Hi | Hi | N |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Hi | Med | Med | N |
| run7 | Low | Med | Med | Hi | Med | Med | N |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **50.0%** (6/12)