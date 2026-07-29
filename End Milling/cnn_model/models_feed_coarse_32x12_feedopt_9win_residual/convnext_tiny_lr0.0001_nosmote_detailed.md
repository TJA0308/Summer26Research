### convnext_tiny_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Med | Med | Hi | Hi | Hi | Hi | Med | Hi | Hi | N |
| run17 | Med | Hi | Low | Hi | Hi | Hi | Med | Med | Med | Med | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Low | Low | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Med | Med | Med | Hi | Med | Hi | Med | Med | Med | Hi | Y |
| run36 | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Med | Low | Low | Med | Med | Med | Med | Med | Med | Med | N |
| run45 | Med | Med | Med | Low | Med | Hi | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Med | Med | Med | Low | Med | Med | Med | Med | Med | N |
| run9 | Med | Low | Low | Low | Low | Med | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **58.3%** (63/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **50.0%** (6/12)