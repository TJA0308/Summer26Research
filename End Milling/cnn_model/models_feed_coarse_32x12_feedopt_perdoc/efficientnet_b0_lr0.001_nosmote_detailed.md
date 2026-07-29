### efficientnet_b0_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_perdoc  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Low | Hi | Low | Low | Low | N |
| run21 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Hi | Low | Low | Y |
| run3 | Hi | Low | Med | Low | Low | Low | N |
| run31 | Med | Low | Hi | Low | Low | Low | N |
| run36 | Hi | Low | Med | Hi | Low | Hi | ~ |
| run37 | Low | Low | Hi | Med | Low | Hi | Y |
| run45 | Med | Low | Med | Low | Low | Low | N |
| run5 | Hi | Low | Hi | Low | Low | Low | N |
| run7 | Low | Hi | Hi | Low | Hi | Hi | N |
| run9 | Med | Hi | Hi | Hi | Hi | Hi | N |

Window accuracy: **33.3%** (12/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)