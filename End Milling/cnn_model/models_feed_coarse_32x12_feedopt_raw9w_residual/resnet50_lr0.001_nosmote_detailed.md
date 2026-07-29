### resnet50_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw9w_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Med | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Med | Med | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Med | Hi | Med | Hi | Med | Hi | Med | Hi | Med | Hi | N |
| run45 | Med | Med | Med | Med | Med | Med | Hi | Hi | Low | Hi | Med | Med | Y |
| run5 | Hi | Hi | Med | Med | Hi | Hi | Med | Hi | Med | Med | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **54.6%** (59/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)