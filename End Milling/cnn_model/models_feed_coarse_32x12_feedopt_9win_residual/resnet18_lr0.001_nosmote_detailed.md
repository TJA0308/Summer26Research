### resnet18_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Hi | Med | Low | Low | Low | Low | Low | Low | Med | Y |
| run17 | Med | Hi | Med | Hi | Hi | Hi | Med | Low | Low | Med | Hi | Med | ~ |
| run21 | Hi | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Low | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Hi | Hi | Hi | Low | Med | Med | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Low | Med | Low | Med | Med | Med | Med | Low | Med | Med | N |
| run45 | Med | Hi | Hi | Low | Low | Med | Low | Low | Med | Low | Low | Low | N |
| run5 | Hi | Med | Hi | Hi | Med | Hi | Hi | Med | Hi | Med | Hi | Hi | Y |
| run7 | Low | Med | Low | Med | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Low | Med | Med | Med | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **58.3%** (63/108)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **66.7%** (8/12)