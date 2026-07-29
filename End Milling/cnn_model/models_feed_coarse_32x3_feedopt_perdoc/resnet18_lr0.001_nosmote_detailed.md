### resnet18_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_perdoc  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Med | Med | Med | N |
| run17 | Med | Hi | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Med | Hi | Hi | Hi | Y |
| run25 | Low | Med | Med | Low | Med | Low | ~ |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Med | Hi | Hi | Hi | N |
| run36 | Hi | Med | Low | Hi | Med | Hi | ~ |
| run37 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Hi | Med | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **50.0%** (6/12)