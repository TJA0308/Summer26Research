### resnet50_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Med | Low | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Low | Hi | Hi | Y |
| run25 | Low | Low | Low | Med | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Med | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Low | Low | Low | Low | N |
| run37 | Low | Hi | Low | Low | Low | Low | Y |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)