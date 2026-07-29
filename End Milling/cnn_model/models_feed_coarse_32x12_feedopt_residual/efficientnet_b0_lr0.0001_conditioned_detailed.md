### efficientnet_b0_lr0.0001_conditioned  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Med | Med | Med | N |
| run17 | Med | Med | Med | Hi | Med | Med | Y |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Hi | Med | Med | Med | Med | N |
| run3 | Hi | Med | Low | Low | Low | Low | N |
| run31 | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Hi | Low | Hi | Hi | Y |
| run37 | Low | Med | Med | Med | Med | Med | N |
| run45 | Med | Hi | Med | Med | Med | Med | Y |
| run5 | Hi | Low | Hi | Med | Low | Low | N |
| run7 | Low | Hi | Low | Med | Hi | Low | ~ |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **47.2%** (17/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **58.3%** (7/12)