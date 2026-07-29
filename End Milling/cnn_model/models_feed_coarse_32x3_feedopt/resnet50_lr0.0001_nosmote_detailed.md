### resnet50_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run17 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Low | Hi | Hi | Y |
| run25 | Low | Low | Hi | Hi | Hi | Hi | N |
| run3 | Hi | Low | Hi | Low | Low | Low | N |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Low | Hi | Hi | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Hi | Low | Hi | Hi | Hi | N |
| run9 | Med | Low | Low | Hi | Low | Low | N |

Window accuracy: **27.8%** (10/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **25.0%** (3/12)