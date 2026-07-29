### efficientnet_b0_lr0.0001_conditioned  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Hi | Low | Low | Low | Hi | Med | Med | Hi | Med | N |
| run17 | Med | Med | Med | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Med | Low | Hi | Low | Hi | Med | Med | Med | Hi | Med | Med | N |
| run25 | Low | Hi | Hi | Low | Hi | Low | Low | Low | Low | Hi | Low | Low | Y |
| run3 | Hi | Low | Hi | Hi | Low | Hi | Med | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Med | Low | Hi | Med | Low | Low | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Low | Hi | Med | Low | Hi | Hi | Med | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Low | Low | Hi | Low | Hi | Low | Low | Low | Low | Low | Y |
| run45 | Med | Hi | Hi | Hi | Med | Med | Hi | Hi | Low | Low | Hi | Hi | N |
| run5 | Hi | Low | Low | Med | Med | Low | Med | Low | Low | Hi | Low | Low | N |
| run7 | Low | Hi | Med | Hi | Low | Low | Low | Low | Hi | Med | Low | Low | Y |
| run9 | Med | Hi | Hi | Hi | Hi | Low | Med | Hi | Low | Low | Hi | Hi | N |

Window accuracy: **38.9%** (42/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)