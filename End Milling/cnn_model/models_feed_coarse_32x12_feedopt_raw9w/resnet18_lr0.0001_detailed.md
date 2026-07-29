### resnet18_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw9w  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Low | Low | Low | Hi | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Low | Low | Low | Hi | Hi | Low | Low | Low | Hi | Low | Low | N |
| run21 | Hi | Hi | Hi | Hi | Low | Low | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run31 | Med | Low | Low | Low | Hi | Hi | Low | Low | Low | Hi | Low | Low | N |
| run36 | Hi | Low | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run5 | Hi | Hi | Hi | Low | Low | Hi | Low | Low | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Hi | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Hi | Low | Hi | Low | Low | Low | Low | Low | N |

Window accuracy: **47.2%** (51/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)