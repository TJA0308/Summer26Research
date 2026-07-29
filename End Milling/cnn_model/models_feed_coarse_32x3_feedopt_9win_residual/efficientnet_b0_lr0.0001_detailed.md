### efficientnet_b0_lr0.0001  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Med | Hi | Hi | Med | Hi | Hi | Med | Low | Hi | Hi | N |
| run17 | Med | Hi | Med | Low | Med | Med | Low | Med | Low | Hi | Med | Med | Y |
| run21 | Hi | Low | Med | Med | Med | Med | Hi | Hi | Low | Hi | Med | Med | N |
| run25 | Low | Med | Low | Med | Hi | Hi | Hi | Hi | Hi | Low | Hi | Hi | N |
| run3 | Hi | Low | Med | Hi | Med | Low | Med | Hi | Med | Hi | Med | Med | N |
| run31 | Med | Low | Med | Med | Med | Med | Med | Med | Med | Low | Med | Med | Y |
| run36 | Hi | Med | Med | Med | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Med | Hi | Low | Low | Med | Hi | Med | Med | Med | Med | N |
| run45 | Med | Med | Low | Med | Med | Hi | Hi | Low | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Hi | Hi | Hi | Hi | Med | Low | Med | Med | Med | Hi | ~ |
| run7 | Low | Low | Low | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run9 | Med | Low | Low | Hi | Med | Hi | Hi | Hi | Hi | Med | Hi | Hi | N |

Window accuracy: **38.0%** (41/108)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **41.7%** (5/12)