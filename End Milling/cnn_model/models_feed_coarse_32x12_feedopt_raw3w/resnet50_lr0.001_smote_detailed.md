### resnet50_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Low | Low | Low | Low | Y |
| run17 | Med | Med | Low | Med | Med | Med | Y |
| run21 | Hi | Hi | Med | Med | Med | Hi | ~ |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Low | Med | Med | Med | N |
| run31 | Med | Med | Med | Low | Med | Med | Y |
| run36 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Med | Med | Med | Med | N |
| run45 | Med | Hi | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Med | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Low | Med | Med | Med | Y |

Window accuracy: **58.3%** (21/36)
Run hard-vote accuracy: **75.0%** (9/12)
Run soft-vote accuracy: **83.3%** (10/12)