### efficientnet_b0_lr0.0001_smote  |  target=feed_coarse  |  scalogram=harmonic_feedopt_perdoc  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Hi | Low | Med | Med | N |
| run17 | Med | Med | Low | Hi | Med | Low | Y |
| run21 | Hi | Low | Low | Hi | Low | Low | N |
| run25 | Low | Low | Low | Hi | Low | Low | Y |
| run3 | Hi | Low | Med | Med | Med | Med | N |
| run31 | Med | Hi | Low | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Low | Med | Hi | Med | Y |
| run37 | Low | Low | Low | Med | Low | Low | Y |
| run45 | Med | Med | Low | Hi | Med | Low | Y |
| run5 | Hi | Low | Low | Med | Low | Low | N |
| run7 | Low | Med | Low | Med | Med | Med | N |
| run9 | Med | Med | Low | Hi | Med | Low | Y |

Window accuracy: **30.6%** (11/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **16.7%** (2/12)