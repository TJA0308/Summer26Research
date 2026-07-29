### resnet50_lr0.0001_ordinal_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run17 | Med | Hi | Hi | Med | Hi | Med | ~ |
| run21 | Hi | Hi | Hi | Low | Hi | Low | Y |
| run25 | Low | Hi | Med | Low | Hi | Low | ~ |
| run3 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Med | Low | Hi | Med | ~ |
| run36 | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Low | Hi | Low | ~ |
| run45 | Med | Med | Med | Low | Med | Med | Y |
| run5 | Hi | Hi | Hi | Low | Hi | Hi | Y |
| run7 | Low | Hi | Hi | Low | Hi | Hi | N |
| run9 | Med | Hi | Low | Low | Low | Low | N |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **66.7%** (8/12)