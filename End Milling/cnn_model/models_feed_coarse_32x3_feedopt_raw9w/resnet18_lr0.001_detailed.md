### resnet18_lr0.001  |  target=feed_coarse  |  scalogram=32x3_feedopt_raw9w  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Hi | Hi | Hi | Hi | Low | Hi | Hi | Hi | Low | Hi | Low | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Low | Low | Low | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Low | Low | Low | Low | Hi | Hi | Hi | Low | Low | N |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run37 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Low | Low | Low | Low | Low | Hi | Low | Hi | Hi | Low | Low | N |
| run5 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Low | Med | Med | Y |

Window accuracy: **49.1%** (53/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)