### resnet18_lr0.0001_cond_gt  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Hi | Hi | Hi | N |
| run17 | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Med | Hi | Med | Hi | ~ |
| run25 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run3 | Hi | Med | Med | Hi | Med | Hi | ~ |
| run31 | Med | Hi | Med | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Med | Hi | Med | Hi | N |
| run45 | Med | Med | Hi | Hi | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run9 | Med | Hi | Hi | Hi | Hi | Hi | N |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **41.7%** (5/12)