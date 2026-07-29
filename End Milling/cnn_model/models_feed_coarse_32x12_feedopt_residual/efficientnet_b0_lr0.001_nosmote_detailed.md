### efficientnet_b0_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Low | Low | Low | Low | Y |
| run17 | Med | Hi | Hi | Low | Hi | Low | N |
| run21 | Hi | Low | Hi | Low | Low | Low | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Low | Low | Low | Low | N |
| run31 | Med | Low | Med | Med | Med | Low | Y |
| run36 | Hi | Low | Med | Low | Low | Low | N |
| run37 | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Med | Hi | Low | Med | Low | Y |
| run5 | Hi | Hi | Low | Low | Low | Low | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **47.2%** (17/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **33.3%** (4/12)