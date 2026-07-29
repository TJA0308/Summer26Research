### efficientnet_b0_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=band_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Med | Med | Med | Med | N |
| run17 | Med | Hi | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Med | Med | Med | Med | N |
| run25 | Low | Hi | Med | Hi | Hi | Hi | N |
| run3 | Hi | Low | Med | Low | Low | Low | N |
| run31 | Med | Low | Med | Low | Low | Low | N |
| run36 | Hi | Hi | Med | Med | Med | Med | N |
| run37 | Low | Hi | Med | Low | Hi | Low | ~ |
| run45 | Med | Low | Med | Low | Low | Low | N |
| run5 | Hi | Low | Med | Hi | Low | Low | N |
| run7 | Low | Low | Med | Low | Low | Low | Y |
| run9 | Med | Low | Med | Med | Med | Med | Y |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **33.3%** (4/12)