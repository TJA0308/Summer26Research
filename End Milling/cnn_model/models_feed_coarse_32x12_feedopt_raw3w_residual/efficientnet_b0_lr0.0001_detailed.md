### efficientnet_b0_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Med | Hi | Hi | N |
| run17 | Med | Low | Low | Hi | Low | Low | N |
| run21 | Hi | Med | Med | Hi | Med | Med | N |
| run25 | Low | Low | Hi | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Low | Med | Hi | Low | N |
| run36 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Low | Hi | Med | Low | ~ |
| run45 | Med | Med | Low | Hi | Med | Low | Y |
| run5 | Hi | Low | Med | Med | Med | Med | N |
| run7 | Low | Med | Hi | Low | Med | Low | ~ |
| run9 | Med | Med | Low | Med | Med | Med | Y |

Window accuracy: **30.6%** (11/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **41.7%** (5/12)