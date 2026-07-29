### efficientnet_b0_lr0.0001_conditioned  |  target=feed_coarse  |  scalogram=32x12_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Low | Low | Low | Low | Y |
| run17 | Med | Med | Hi | Med | Med | Med | Y |
| run21 | Hi | Low | Hi | Low | Low | Low | N |
| run25 | Low | Low | Low | Med | Low | Low | Y |
| run3 | Hi | Med | Hi | Low | Med | Low | N |
| run31 | Med | Med | Hi | Low | Med | Low | Y |
| run36 | Hi | Med | Med | Hi | Med | Med | N |
| run37 | Low | Low | Hi | Med | Low | Low | Y |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Low | Med | Low | Low | Low | N |
| run7 | Low | Med | Med | Low | Med | Med | N |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **50.0%** (6/12)