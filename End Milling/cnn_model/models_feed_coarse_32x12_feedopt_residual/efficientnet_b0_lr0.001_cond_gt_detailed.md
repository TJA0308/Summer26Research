### efficientnet_b0_lr0.001_cond_gt  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Low | Hi | Hi | Hi | N |
| run17 | Med | Med | Hi | Low | Med | Low | Y |
| run21 | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run25 | Low | Hi | Med | Hi | Hi | Hi | N |
| run3 | Hi | Hi | Med | Low | Hi | Med | Y |
| run31 | Med | Hi | Low | Low | Low | Low | N |
| run36 | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run37 | Low | Low | Hi | Low | Low | Hi | Y |
| run45 | Med | Hi | Hi | Low | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Low | Hi | Hi | Y |
| run7 | Low | Hi | Low | Low | Low | Low | Y |
| run9 | Med | Hi | Hi | Hi | Hi | Hi | N |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **33.3%** (4/12)