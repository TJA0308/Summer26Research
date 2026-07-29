### resnet50_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run17 | Med | Hi | Low | Low | Low | Low | Low | Hi | Hi | Hi | Low | Hi | N |
| run21 | Hi | Hi | Low | Low | Hi | Low | Low | Low | Low | Hi | Low | Low | N |
| run25 | Low | Low | Low | Hi | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run3 | Hi | Med | Med | Med | Med | Med | Hi | Med | Med | Low | Med | Med | N |
| run31 | Med | Hi | Low | Low | Med | Low | Low | Low | Low | Hi | Low | Low | N |
| run36 | Hi | Hi | Med | Low | Med | Low | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Med | Hi | Hi | Hi | Low | Low | Low | Hi | Hi | Hi | N |
| run45 | Med | Med | Med | Med | Med | Med | Med | Low | Med | Hi | Med | Med | Y |
| run5 | Hi | Hi | Low | Low | Med | Low | Med | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Med | Low | Hi | Hi | Hi | Hi | Low | Low | Y |
| run9 | Med | Low | Low | Low | Med | Low | Low | Low | Low | Med | Low | Low | N |

Window accuracy: **30.6%** (33/108)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)