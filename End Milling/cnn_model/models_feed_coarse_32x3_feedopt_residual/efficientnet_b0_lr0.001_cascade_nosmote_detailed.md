### efficientnet_b0_lr0.001_cascade_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Med | Hi | Med | Med | Med | Y |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run3 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Med | Hi | Med | Med | Med | Y |
| run36 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Med | Hi | Hi | N |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run9 | Med | Hi | Med | Med | Med | Med | Y |

Window accuracy: **52.8%** (19/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **66.7%** (8/12)