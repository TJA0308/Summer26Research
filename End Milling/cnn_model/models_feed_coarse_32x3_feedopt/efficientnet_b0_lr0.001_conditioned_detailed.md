### efficientnet_b0_lr0.001_conditioned  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Low | Low | Low | Low | Low | N |
| run21 | Hi | Hi | Low | Low | Low | Low | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Low | Low | Low | N |
| run31 | Med | Low | Low | Low | Low | Low | N |
| run36 | Hi | Low | Hi | Low | Low | Low | N |
| run37 | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Med | Med | Low | Med | Med | Y |
| run5 | Hi | Low | Hi | Low | Low | Low | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Hi | Low | Med | Low | Y |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **41.7%** (5/12)