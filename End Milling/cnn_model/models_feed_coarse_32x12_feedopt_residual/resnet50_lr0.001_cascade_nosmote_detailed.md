### resnet50_lr0.001_cascade_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Med | Med | Med | Med | N |
| run17 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Med | Low | Med | Med | Low | ~ |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Hi | Med | Hi | Hi | N |
| run36 | Hi | Hi | Med | Med | Med | Med | N |
| run37 | Low | Hi | Low | Med | Hi | Med | N |
| run45 | Med | Low | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Med | Hi | Hi | Med | Y |
| run7 | Low | Low | Med | Low | Low | Low | Y |
| run9 | Med | Low | Med | Med | Med | Med | Y |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)