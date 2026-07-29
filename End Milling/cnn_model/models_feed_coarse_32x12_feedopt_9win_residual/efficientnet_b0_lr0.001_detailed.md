### efficientnet_b0_lr0.001  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Med | Low | Med | Hi | Med | Med | Low | Low | Low | Med | Y |
| run17 | Med | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Low | Hi | Hi | N |
| run21 | Hi | Med | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Med | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Med | Hi | Med | Med | Med | Hi | Hi | Hi | Med | Med | N |
| run31 | Med | Med | Med | Med | Hi | Hi | Hi | Hi | Hi | Low | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Low | Med | Low | Low | Med | Low | Low | Low | Low | Low | Low | N |
| run5 | Hi | Low | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Med | Low | Med | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **59.3%** (64/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **50.0%** (6/12)