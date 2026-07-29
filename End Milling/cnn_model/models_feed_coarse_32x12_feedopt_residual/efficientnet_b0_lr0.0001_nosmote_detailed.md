### efficientnet_b0_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Low | Med | Med | N |
| run17 | Med | Med | Med | Low | Med | Med | Y |
| run21 | Hi | Med | Med | Low | Med | Med | N |
| run25 | Low | Med | Low | Med | Med | Med | N |
| run3 | Hi | Med | Med | Low | Med | Med | N |
| run31 | Med | Med | Med | Hi | Med | Med | Y |
| run36 | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run37 | Low | Med | Med | Med | Med | Med | N |
| run45 | Med | Med | Low | Low | Low | Low | N |
| run5 | Hi | Med | Hi | Med | Med | Med | N |
| run7 | Low | Med | Low | Hi | Med | Low | ~ |
| run9 | Med | Hi | Med | Hi | Hi | Hi | N |

Window accuracy: **33.3%** (12/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **33.3%** (4/12)