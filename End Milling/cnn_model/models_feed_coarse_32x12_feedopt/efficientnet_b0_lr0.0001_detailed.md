### efficientnet_b0_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Hi | Med | Med | Med | N |
| run17 | Med | Med | Low | Med | Med | Med | Y |
| run21 | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run25 | Low | Med | Hi | Med | Med | Med | N |
| run3 | Hi | Med | Med | Low | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Med | Low | Med | Med | N |
| run37 | Low | Hi | Low | Hi | Hi | Hi | N |
| run45 | Med | Med | Low | Hi | Med | Low | Y |
| run5 | Hi | Med | Med | Hi | Med | Med | N |
| run7 | Low | Med | Hi | Hi | Hi | Hi | N |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **33.3%** (4/12)