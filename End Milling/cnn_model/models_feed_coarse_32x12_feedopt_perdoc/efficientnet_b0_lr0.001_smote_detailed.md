### efficientnet_b0_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_perdoc  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Hi | Low | Med | Low | ~ |
| run17 | Med | Med | Hi | Med | Med | Med | Y |
| run21 | Hi | Low | Hi | Med | Low | Hi | ~ |
| run25 | Low | Low | Hi | Low | Low | Low | Y |
| run3 | Hi | Med | Hi | Low | Med | Low | N |
| run31 | Med | Med | Low | Med | Med | Med | Y |
| run36 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Hi | Low | Med | Hi | N |
| run45 | Med | Med | Low | Low | Low | Low | N |
| run5 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Med | Hi | Med | Med | Med | N |
| run9 | Med | Med | Hi | Low | Med | Hi | Y |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **58.3%** (7/12)