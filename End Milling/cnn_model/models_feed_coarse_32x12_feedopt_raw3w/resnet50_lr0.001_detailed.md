### resnet50_lr0.001  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Med | Med | Med | Hi | ~ |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Med | Med | Med | Med | N |
| run45 | Med | Hi | Med | Med | Med | Hi | Y |
| run5 | Hi | Hi | Med | Med | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Low | Med | Med | Med | Y |

Window accuracy: **58.3%** (21/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)