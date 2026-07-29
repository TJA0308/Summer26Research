### efficientnet_b0_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_perdoc  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Low | Hi | Med | Med | N |
| run17 | Med | Med | Med | Hi | Med | Med | Y |
| run21 | Hi | Med | Med | Hi | Med | Med | N |
| run25 | Low | Med | Hi | Low | Med | Med | N |
| run3 | Hi | Hi | Med | Low | Hi | Med | Y |
| run31 | Med | Hi | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Low | Low | Low | Low | N |
| run37 | Low | Med | Hi | Low | Med | Low | ~ |
| run45 | Med | Hi | Med | Hi | Hi | Hi | N |
| run5 | Hi | Med | Hi | Med | Med | Med | N |
| run7 | Low | Med | Low | Med | Med | Med | N |
| run9 | Med | Low | Med | Hi | Low | Med | ~ |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **33.3%** (4/12)