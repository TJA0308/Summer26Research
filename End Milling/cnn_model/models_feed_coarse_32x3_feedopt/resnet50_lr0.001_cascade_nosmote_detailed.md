### resnet50_lr0.001_cascade_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Med | Hi | Med | Med | Med | Y |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Med | Hi | Low | Hi | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Hi | Med | Med | Med | Y |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Hi | Med | Med | Med | N |
| run7 | Low | Med | Med | Low | Med | Med | N |
| run9 | Med | Med | Med | Low | Med | Med | Y |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **50.0%** (6/12)