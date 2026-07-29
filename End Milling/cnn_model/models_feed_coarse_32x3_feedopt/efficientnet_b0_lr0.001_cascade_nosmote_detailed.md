### efficientnet_b0_lr0.001_cascade_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Low | Low | Low | Low | Y |
| run17 | Med | Hi | Hi | Med | Hi | Hi | N |
| run21 | Hi | Hi | Med | Low | Hi | Low | Y |
| run25 | Low | Hi | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Low | Med | Hi | Low | Y |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Med | Hi | Low | Med | Hi | ~ |
| run37 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Hi | Hi | Low | Hi | Low | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Med | Hi | Low | Med | Low | ~ |
| run9 | Med | Hi | Hi | Hi | Hi | Hi | N |

Window accuracy: **33.3%** (12/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)