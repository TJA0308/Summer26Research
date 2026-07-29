### efficientnet_b0_lr0.001  |  target=feed_coarse  |  scalogram=32x3_feedopt_raw3w_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Low | Low | Low | Low | Low | N |
| run21 | Hi | Low | Med | Med | Med | Med | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Low | Med | Med | N |
| run31 | Med | Med | Med | Low | Med | Med | Y |
| run36 | Hi | Med | Med | Low | Med | Med | N |
| run37 | Low | Low | Low | Med | Low | Low | Y |
| run45 | Med | Med | Low | Med | Med | Med | Y |
| run5 | Hi | Low | Low | Med | Low | Low | N |
| run7 | Low | Med | Low | Low | Low | Low | Y |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **47.2%** (17/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)