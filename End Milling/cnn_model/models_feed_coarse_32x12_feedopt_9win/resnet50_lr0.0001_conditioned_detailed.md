### resnet50_lr0.0001_conditioned  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Med | Low | Low | Low | Med | Low | Low | Low | Low | Low | Y |
| run17 | Med | Low | Low | Hi | Hi | Hi | Med | Med | Med | Med | Med | Low | Y |
| run21 | Hi | Hi | Low | Hi | Hi | Hi | Low | Low | Low | Med | Hi | Low | Y |
| run25 | Low | Low | Hi | Low | Med | Low | Low | Hi | Hi | Hi | Low | Low | Y |
| run3 | Hi | Low | Low | Med | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run31 | Med | Low | Low | Low | Hi | Hi | Low | Low | Low | Low | Low | Low | N |
| run36 | Hi | Hi | Med | Med | Hi | Low | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run37 | Low | Low | Low | Med | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Low | Med | Low | Med | Low | Med | Med | Low | Low | Low | Low | N |
| run5 | Hi | Low | Low | Hi | Hi | Hi | Hi | Med | Hi | Med | Hi | Med | Y |
| run7 | Low | Low | Med | Low | Hi | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Hi | Hi | Med | Med | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **46.3%** (50/108)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **41.7%** (5/12)