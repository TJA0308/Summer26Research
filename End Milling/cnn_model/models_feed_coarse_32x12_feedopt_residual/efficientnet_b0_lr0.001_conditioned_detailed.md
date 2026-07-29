### efficientnet_b0_lr0.001_conditioned  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Med | Low | Low | Y |
| run17 | Med | Low | Med | Low | Low | Low | N |
| run21 | Hi | Low | Med | Med | Med | Med | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Med | Low | Low | Low | N |
| run31 | Med | Med | Med | Low | Med | Med | Y |
| run36 | Hi | Low | Low | Low | Low | Low | N |
| run37 | Low | Low | Med | Med | Med | Med | N |
| run45 | Med | Low | Med | Low | Low | Low | N |
| run5 | Hi | Low | Med | Low | Low | Low | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Med | Med | Med | Med | Y |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)