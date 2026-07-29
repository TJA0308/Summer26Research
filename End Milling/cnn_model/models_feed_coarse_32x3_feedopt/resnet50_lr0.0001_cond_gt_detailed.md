### resnet50_lr0.0001_cond_gt  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Med | Low | Low | Low | Y |
| run17 | Med | Low | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Med | Low | Med | Med | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Med | Low | Low | Low | N |
| run31 | Med | Low | Med | Low | Low | Low | N |
| run36 | Hi | Low | Low | Med | Low | Med | N |
| run37 | Low | Low | Med | Low | Low | Med | Y |
| run45 | Med | Low | Med | Low | Low | Low | N |
| run5 | Hi | Low | Low | Low | Low | Low | N |
| run7 | Low | Low | Med | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **33.3%** (4/12)