### efficientnet_b0_lr0.001_smote  |  target=feed_coarse  |  scalogram=band_feedopt_perdoc  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Hi | Low | Low | Y |
| run17 | Med | Low | Low | Hi | Low | Low | N |
| run21 | Hi | Low | Low | Low | Low | Low | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Hi | Low | Low | N |
| run31 | Med | Low | Med | Hi | Low | Med | ~ |
| run36 | Hi | Low | Low | Hi | Low | Low | N |
| run37 | Low | Low | Med | Hi | Low | Low | Y |
| run45 | Med | Low | Low | Hi | Low | Low | N |
| run5 | Hi | Low | Low | Hi | Low | Low | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **41.7%** (5/12)