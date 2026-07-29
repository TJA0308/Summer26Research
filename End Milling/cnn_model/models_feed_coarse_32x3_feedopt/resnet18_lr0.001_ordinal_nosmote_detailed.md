### resnet18_lr0.001_ordinal_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Low | Low | Low | Low | Low | N |
| run21 | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run25 | Low | Med | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Low | Med | Hi | Low | Med | ~ |
| run36 | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Low | Hi | Hi | Low | ~ |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Med | Med | N |
| run7 | Low | Low | Med | Med | Med | Low | ~ |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **33.3%** (12/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **58.3%** (7/12)