### resnet18_lr0.0001_ordinal_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run17 | Med | Low | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Low | Low | Hi | Low | Low | N |
| run25 | Low | Low | Low | Hi | Low | Hi | Y |
| run3 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Low | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Low | Low | Hi | Low | Low | Y |
| run45 | Med | Med | Hi | Hi | Hi | Hi | N |
| run5 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Hi | Hi | Hi | Hi | N |
| run9 | Med | Low | Hi | Hi | Hi | Hi | N |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **33.3%** (4/12)