### convnext_tiny_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run17 | Med | Hi | Hi | Low | Low | Low | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Low | Low | Low | Low | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Hi | Low | Low | Low | Low | Hi | Hi | Hi | Hi | Hi | Low | ~ |
| run3 | Hi | Hi | Low | Low | Hi | Low | Hi | Hi | Hi | Low | Hi | Hi | Y |
| run31 | Med | Hi | Hi | Low | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Low | Low | Low | Low | Hi | Hi | Hi | Hi | Hi | Low | ~ |
| run45 | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Low | Low | Hi | Hi | Hi | Hi | Low | Low | Y |
| run9 | Med | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |

Window accuracy: **37.0%** (40/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **58.3%** (7/12)