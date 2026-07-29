### efficientnet_b0_lr0.0001_cascade_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Hi | Med | Low | Med | Y |
| run17 | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Low | Med | Hi | Low | Low | N |
| run25 | Low | Med | Med | Low | Med | Med | N |
| run3 | Hi | Hi | Med | Med | Med | Med | N |
| run31 | Med | Low | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Low | Med | Med | Med | N |
| run37 | Low | Med | Med | Med | Med | Med | N |
| run45 | Med | Low | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run7 | Low | Hi | Med | Med | Med | Med | N |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **41.7%** (5/12)