### efficientnet_b0_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Med | Low | Low | Low | Y |
| run17 | Med | Med | Med | Low | Med | Med | Y |
| run21 | Hi | Low | Med | Low | Low | Low | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Med | Low | Low | N |
| run31 | Med | Med | Low | Low | Low | Low | N |
| run36 | Hi | Med | Low | Med | Med | Med | N |
| run37 | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Hi | Low | Low | Low | Low | N |
| run5 | Hi | Low | Low | Low | Low | Low | N |
| run7 | Low | Med | Low | Low | Low | Low | Y |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)