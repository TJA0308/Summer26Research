### resnet50_lr0.0001_cascade_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Low | Med | Low | ~ |
| run17 | Med | Med | Med | Low | Med | Med | Y |
| run21 | Hi | Med | Med | Low | Med | Med | N |
| run25 | Low | Med | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Low | Med | Med | N |
| run31 | Med | Med | Med | Low | Med | Med | Y |
| run36 | Hi | Med | Med | Low | Med | Med | N |
| run37 | Low | Low | Med | Low | Low | Low | Y |
| run45 | Med | Med | Med | Low | Med | Med | Y |
| run5 | Hi | Low | Med | Low | Low | Low | N |
| run7 | Low | Med | Med | Low | Med | Low | ~ |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **33.3%** (12/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **58.3%** (7/12)