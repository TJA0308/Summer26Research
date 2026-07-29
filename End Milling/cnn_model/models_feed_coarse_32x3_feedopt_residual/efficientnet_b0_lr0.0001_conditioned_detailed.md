### efficientnet_b0_lr0.0001_conditioned  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Med | Low | Low | Low | Y |
| run17 | Med | Hi | Med | Low | Hi | Low | N |
| run21 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Med | Low | Low | Low | Y |
| run3 | Hi | Med | Low | Hi | Med | Low | N |
| run31 | Med | Med | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Med | Med | Med | Med | Med | N |
| run37 | Low | Med | Med | Med | Med | Med | N |
| run45 | Med | Low | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Low | Med | Med | Med | N |
| run7 | Low | Med | Low | Med | Med | Med | N |
| run9 | Med | Med | Med | Hi | Med | Med | Y |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)