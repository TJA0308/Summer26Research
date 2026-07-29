### resnet50_lr0.001_cond_gt  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Hi | Low | Low | Y |
| run3 | Hi | Med | Hi | Med | Med | Med | N |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Med | Hi | Med | Med | Med | Y |
| run5 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Med | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **47.2%** (17/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)