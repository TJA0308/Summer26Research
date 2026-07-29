### convnext_tiny_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Med | Hi | Med | N |
| run17 | Med | Med | Med | Low | Med | Med | Y |
| run21 | Hi | Hi | Med | Med | Med | Med | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run31 | Med | Low | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Hi | Med | Med | Med | N |
| run37 | Low | Low | Low | Med | Low | Med | Y |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Med | Low | Low | N |

Window accuracy: **61.1%** (22/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **58.3%** (7/12)