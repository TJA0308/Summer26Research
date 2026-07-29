### resnet50_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_perdoc  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Low | Med | Med | Med | N |
| run17 | Med | Hi | Low | Hi | Hi | Hi | N |
| run21 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Hi | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Med | Med | Med | Med | N |
| run31 | Med | Hi | Low | Hi | Hi | Hi | N |
| run36 | Hi | Low | Low | Low | Low | Low | N |
| run37 | Low | Low | Low | Hi | Low | Low | Y |
| run45 | Med | Hi | Med | Med | Med | Med | Y |
| run5 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)