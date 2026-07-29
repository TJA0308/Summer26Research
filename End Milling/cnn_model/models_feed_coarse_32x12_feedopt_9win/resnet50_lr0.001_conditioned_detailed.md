### resnet50_lr0.001_conditioned  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Low | Med | Hi | Hi | Hi | Med | Med | Hi | Hi | Med | ~ |
| run36 | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Med | Med | Hi | Med | Hi | Hi | Med | Hi | Hi | Med | Y |
| run7 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Low | Med | Med | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **58.3%** (63/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)