### resnet50_lr0.0001_ordinal_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Med | Med | Med | Low | ~ |
| run17 | Med | Low | Med | Med | Med | Low | Y |
| run21 | Hi | Low | Med | Med | Med | Med | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Med | Hi | Low | Low | N |
| run31 | Med | Low | Med | Med | Med | Low | Y |
| run36 | Hi | Low | Med | Med | Med | Low | N |
| run37 | Low | Low | Med | Med | Med | Low | ~ |
| run45 | Med | Low | Low | Med | Low | Low | N |
| run5 | Hi | Low | Low | Med | Low | Low | N |
| run7 | Low | Low | Med | Med | Med | Low | ~ |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **33.3%** (12/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **33.3%** (4/12)