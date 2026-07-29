### resnet18_lr0.001  |  target=feed_coarse  |  scalogram=32x12_feedopt  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Med | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Med | Med | Med | Med | Med | N |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Med | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Low | Low | Low | Med | Y |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Hi | Med | Med | N |
| run7 | Low | Hi | Low | Med | Hi | Med | N |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **33.3%** (4/12)