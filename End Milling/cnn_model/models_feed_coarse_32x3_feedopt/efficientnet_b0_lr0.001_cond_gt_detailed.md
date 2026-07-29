### efficientnet_b0_lr0.001_cond_gt  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Hi | Low | Low | N |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Low | Hi | Low | Low | Low | N |
| run37 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Low | Med | Hi | Low | Med | ~ |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Hi | Low | Low | Low | Y |
| run9 | Med | Low | Med | Low | Low | Low | N |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **50.0%** (6/12)