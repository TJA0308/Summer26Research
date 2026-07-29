### efficientnet_b0_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Low | Low | Low | Low | Y |
| run17 | Med | Med | Med | Low | Med | Med | Y |
| run21 | Hi | Low | Med | Low | Low | Low | N |
| run25 | Low | Low | Low | Med | Low | Low | Y |
| run3 | Hi | Med | Low | Low | Low | Low | N |
| run31 | Med | Low | Med | Low | Low | Low | N |
| run36 | Hi | Low | Low | Low | Low | Low | N |
| run37 | Low | Low | Med | Low | Low | Low | Y |
| run45 | Med | Hi | Med | Low | Hi | Low | N |
| run5 | Hi | Low | Low | Med | Low | Low | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)