### efficientnet_b0_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=harmonic_feedopt_perdoc  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Hi | Med | Low | Med | Y |
| run17 | Med | Med | Low | Hi | Med | Low | Y |
| run21 | Hi | Low | Low | Hi | Low | Low | N |
| run25 | Low | Med | Low | Hi | Med | Hi | N |
| run3 | Hi | Low | Med | Med | Med | Med | N |
| run31 | Med | Hi | Low | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Low | Med | Hi | Med | Y |
| run37 | Low | Med | Low | Med | Med | Med | N |
| run45 | Med | Med | Low | Hi | Med | Low | Y |
| run5 | Hi | Low | Low | Low | Low | Low | N |
| run7 | Low | Med | Med | Low | Med | Med | N |
| run9 | Med | Low | Low | Hi | Low | Low | N |

Window accuracy: **22.2%** (8/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **0.0%** (0/12)