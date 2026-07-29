### efficientnet_b0_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Med | Low | Low | Y |
| run17 | Med | Med | Hi | Med | Med | Hi | Y |
| run21 | Hi | Med | Hi | Med | Med | Med | N |
| run25 | Low | Low | Low | Hi | Low | Low | Y |
| run3 | Hi | Hi | Med | Low | Hi | Med | Y |
| run31 | Med | Med | Med | Hi | Med | Med | Y |
| run36 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Low | Low | Low | Low | Y |
| run45 | Med | Med | Hi | Med | Med | Med | Y |
| run5 | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run7 | Low | Low | Hi | Low | Low | Low | Y |
| run9 | Med | Hi | Low | Low | Low | Low | N |

Window accuracy: **55.6%** (20/36)
Run hard-vote accuracy: **83.3%** (10/12)
Run soft-vote accuracy: **66.7%** (8/12)