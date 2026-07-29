### resnet50_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_perdoc  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Med | Med | Med | Hi | Y |
| run21 | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run25 | Low | Low | Med | Low | Low | Med | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Med | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Med | Med | Med | Med | N |
| run37 | Low | Med | Med | Med | Med | Med | N |
| run45 | Med | Low | Med | Med | Med | Med | Y |
| run5 | Hi | Low | Hi | Med | Low | Low | N |
| run7 | Low | Med | Hi | Low | Med | Med | N |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **33.3%** (12/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **16.7%** (2/12)