### resnet50_lr0.001  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw9w_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Low | Low | Low | Hi | Med | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Hi | Hi | Hi | Hi | Med | Hi | Med | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Hi | Hi | Hi | Med | Med | Med | Hi | Med | Med | Hi | ~ |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | Med | Med | Med | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Med | Low | Low | Low | Low | Hi | Med | Med | Low | Low | Y |
| run45 | Med | Med | Med | Med | Med | Med | Med | Hi | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Med | Med | Hi | Med | Med | Med | Hi | Med | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | Low | Med | Low | Low | Low | Low | N |

Window accuracy: **58.3%** (63/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **58.3%** (7/12)