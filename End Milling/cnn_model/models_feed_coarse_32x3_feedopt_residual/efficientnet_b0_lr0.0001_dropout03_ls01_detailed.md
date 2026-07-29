### efficientnet_b0_lr0.0001_dropout03_ls01  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Med | Low | Low | Y |
| run17 | Med | Med | Low | Hi | Med | Med | Y |
| run21 | Hi | Low | Low | Med | Low | Low | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Low | Low | Low | N |
| run31 | Med | Low | Hi | Low | Low | Low | N |
| run36 | Hi | Low | Low | Low | Low | Low | N |
| run37 | Low | Med | Low | Low | Low | Low | Y |
| run45 | Med | Med | Low | Hi | Med | Low | Y |
| run5 | Hi | Hi | Med | Med | Med | Med | N |
| run7 | Low | Low | Hi | Low | Low | Low | Y |
| run9 | Med | Med | Low | Low | Low | Low | N |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **41.7%** (5/12)