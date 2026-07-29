### efficientnet_b0_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run17 | Med | Hi | Med | Hi | Med | Med | Low | Low | Low | Med | Med | Med | Y |
| run21 | Hi | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run25 | Low | Med | Hi | Low | Low | Low | Low | Med | Med | Med | Med | Low | ~ |
| run3 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run31 | Med | Hi | Med | Hi | Hi | Hi | Low | Low | Low | Med | Hi | Med | ~ |
| run36 | Hi | Hi | Med | Hi | Hi | Med | Low | Hi | Low | Med | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run5 | Hi | Med | Hi | Med | Hi | Hi | Low | Low | Low | Med | Med | Low | N |
| run7 | Low | Hi | Hi | Med | Hi | Med | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |

Window accuracy: **28.7%** (31/108)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **50.0%** (6/12)