### convnext_tiny_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Med | Low | Low | Y |
| run17 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run25 | Low | Hi | Low | Low | Low | Low | Hi | Low | Low | Hi | Low | Low | Y |
| run3 | Hi | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run31 | Med | Med | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Med | Hi | Low | Low | Low | Med | Hi | Hi | Med | Med | N |
| run37 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run45 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Med | Low | Low | N |
| run5 | Hi | Hi | Low | Low | Low | Low | Low | Low | Low | Hi | Low | Low | N |
| run7 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **42.6%** (46/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)