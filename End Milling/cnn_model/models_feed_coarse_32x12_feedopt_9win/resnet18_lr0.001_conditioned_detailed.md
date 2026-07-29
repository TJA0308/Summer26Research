### resnet18_lr0.001_conditioned  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Low | Low | Low | Low | Low | Low | Low | Hi | Low | Low | Y |
| run17 | Med | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Hi | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Low | Low | Low | Low | Low | Low | Low | Hi | Low | Low | N |
| run31 | Med | Med | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Low | Low | Hi | Low | Hi | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run5 | Hi | Hi | Low | Low | Low | Low | Low | Hi | Hi | Hi | Low | Low | N |
| run7 | Low | Low | Low | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run9 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **48.1%** (52/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)