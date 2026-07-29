### efficientnet_b0_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Hi | Low | Low | Y |
| run17 | Med | Low | Low | Low | Low | Low | N |
| run21 | Hi | Low | Low | Low | Low | Low | N |
| run25 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run3 | Hi | Hi | Low | Low | Low | Low | N |
| run31 | Med | Low | Low | Hi | Low | Low | N |
| run36 | Hi | Low | Low | Low | Low | Low | N |
| run37 | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Low | Low | Low | Low | Low | N |
| run5 | Hi | Low | Low | Low | Low | Low | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Hi | Low | Low | Low | Low | N |

Window accuracy: **25.0%** (9/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **25.0%** (3/12)