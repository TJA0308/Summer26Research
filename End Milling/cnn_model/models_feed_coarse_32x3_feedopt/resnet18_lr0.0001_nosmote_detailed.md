### resnet18_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Low | Med | Med | N |
| run17 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run25 | Low | Low | Hi | Hi | Hi | Hi | N |
| run3 | Hi | Med | Hi | Low | Med | Low | N |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Low | Low | Hi | Low | Low | Y |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Hi | Hi | Hi | Hi | N |
| run9 | Med | Low | Low | Med | Low | Low | N |

Window accuracy: **47.2%** (17/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)