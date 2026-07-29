### resnet50_lr0.001_conditioned  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Hi | Med | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Hi | Low | Hi | Low | Y |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Med | Med | Med | Med | Y |

Window accuracy: **63.9%** (23/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **58.3%** (7/12)