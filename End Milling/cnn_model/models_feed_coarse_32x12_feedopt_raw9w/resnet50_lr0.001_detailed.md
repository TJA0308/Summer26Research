### resnet50_lr0.001  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw9w  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Hi | Hi | Med | Med | Med | Med | Med | N |
| run17 | Med | Med | Hi | Hi | Hi | Hi | Med | Hi | Med | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Hi | Hi | Hi | Med | Hi | Med | Hi | Med | Hi | Med | Y |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Low | Low | Low | Low | Med | Med | Low | Med | Low | Low | Med | Y |
| run45 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Med | Med | Med | Med | Med | Med | Low | Hi | Med | Med | Y |

Window accuracy: **67.6%** (73/108)
Run hard-vote accuracy: **75.0%** (9/12)
Run soft-vote accuracy: **58.3%** (7/12)