### efficientnet_b0_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_raw3w_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Low | Low | Low | Low | Y |
| run17 | Med | Med | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Med | Med | Med | Med | Med | N |
| run3 | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run31 | Med | Med | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Low | Hi | Med | Low | Low | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Hi | Med | Med | Med | Med | N |
| run9 | Med | Med | Med | Hi | Med | Med | Y |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)