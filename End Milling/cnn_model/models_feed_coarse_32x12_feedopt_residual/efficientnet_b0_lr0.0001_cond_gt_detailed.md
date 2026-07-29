### efficientnet_b0_lr0.0001_cond_gt  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Med | Med | Med | Med | N |
| run17 | Med | Low | Low | Hi | Low | Low | N |
| run21 | Hi | Low | Med | Low | Low | Low | N |
| run25 | Low | Hi | Med | Med | Med | Med | N |
| run3 | Hi | Med | Med | Low | Med | Med | N |
| run31 | Med | Med | Med | Low | Med | Med | Y |
| run36 | Hi | Med | Low | Med | Med | Med | N |
| run37 | Low | Low | Med | Med | Med | Med | N |
| run45 | Med | Low | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Low | Med | Hi | Low | Y |
| run7 | Low | Low | Med | Med | Med | Med | N |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **30.6%** (11/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **25.0%** (3/12)