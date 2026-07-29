### efficientnet_b0_lr0.001  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Med | Med | Med | Med | N |
| run17 | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Med | Med | Med | Med | N |
| run25 | Low | Hi | Med | Hi | Hi | Hi | N |
| run3 | Hi | Low | Hi | Med | Low | Hi | ~ |
| run31 | Med | Med | Hi | Med | Med | Med | Y |
| run36 | Hi | Hi | Med | Med | Med | Med | N |
| run37 | Low | Med | Low | Hi | Med | Med | N |
| run45 | Med | Med | Hi | Med | Med | Med | Y |
| run5 | Hi | Hi | Med | Med | Med | Med | N |
| run7 | Low | Med | Med | Med | Med | Med | N |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **41.7%** (5/12)