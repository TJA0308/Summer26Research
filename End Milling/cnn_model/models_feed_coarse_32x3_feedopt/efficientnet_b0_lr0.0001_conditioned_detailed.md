### efficientnet_b0_lr0.0001_conditioned  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Low | Med | Low | Low | Low | N |
| run25 | Low | Low | Med | Med | Med | Med | N |
| run3 | Hi | Low | Low | Low | Low | Low | N |
| run31 | Med | Med | Med | Low | Med | Med | Y |
| run36 | Hi | Med | Low | Low | Low | Low | N |
| run37 | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Med | Low | Low | Low | Low | N |
| run5 | Hi | Med | Low | Low | Low | Low | N |
| run7 | Low | Med | Low | Low | Low | Low | Y |
| run9 | Med | Med | Med | Low | Med | Med | Y |

Window accuracy: **47.2%** (17/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)