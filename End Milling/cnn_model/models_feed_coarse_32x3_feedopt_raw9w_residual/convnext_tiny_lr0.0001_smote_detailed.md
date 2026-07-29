### convnext_tiny_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_raw9w_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Low | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run21 | Hi | Low | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Low | Low | Low | Low | Low | Med | Low | Low | Low | N |
| run31 | Med | Low | Low | Low | Hi | Low | Low | Low | Low | Low | Low | Low | N |
| run36 | Hi | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run37 | Low | Low | Low | Med | Low | Low | Med | Med | Med | Med | Med | Low | ~ |
| run45 | Med | Med | Med | Low | Med | Med | Med | Med | Med | Low | Med | Med | Y |
| run5 | Hi | Low | Hi | Med | Med | Low | Low | Med | Med | Med | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Low | Med | Med | Med | Med | Med | Low | Low | Med | Med | Y |

Window accuracy: **42.6%** (46/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **50.0%** (6/12)