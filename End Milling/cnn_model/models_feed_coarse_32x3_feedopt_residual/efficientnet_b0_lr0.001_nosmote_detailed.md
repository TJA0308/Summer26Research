### efficientnet_b0_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Low | Med | Med | Med | N |
| run17 | Med | Med | Low | Low | Low | Low | N |
| run21 | Hi | Med | Hi | Low | Med | Hi | ~ |
| run25 | Low | Hi | Low | Med | Hi | Hi | N |
| run3 | Hi | Low | Low | Med | Low | Med | N |
| run31 | Med | Med | Low | Med | Med | Med | Y |
| run36 | Hi | Hi | Low | Med | Hi | Med | Y |
| run37 | Low | Low | Hi | Med | Low | Low | Y |
| run45 | Med | Hi | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Hi | Med | Med | Med | N |
| run7 | Low | Hi | Low | Med | Hi | Hi | N |
| run9 | Med | Med | Low | Med | Med | Med | Y |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)