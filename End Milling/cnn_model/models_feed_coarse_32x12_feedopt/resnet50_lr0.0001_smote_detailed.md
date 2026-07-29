### resnet50_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Med | Med | Low | Med | Med | Y |
| run21 | Hi | Med | Med | Low | Med | Med | N |
| run25 | Low | Med | Med | Low | Med | Med | N |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Low | Med | Med | Y |
| run36 | Hi | Med | Med | Low | Med | Med | N |
| run37 | Low | Med | Med | Med | Med | Med | N |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Low | Med | Med | Med | Med | N |
| run7 | Low | Med | Med | Low | Med | Med | N |
| run9 | Med | Low | Med | Low | Low | Med | ~ |

Window accuracy: **27.8%** (10/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **33.3%** (4/12)