### convnext_tiny_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Hi | Hi | Hi | Hi | Low | Low | Low | Hi | Hi | N |
| run17 | Med | Hi | Med | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Med | Hi | Low | Low | Med | Low | Low | Y |
| run3 | Hi | Hi | Low | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Med | Low | Low | Med | Hi | Hi | Hi | Hi | Med | N |
| run45 | Med | Med | Hi | Med | Hi | Hi | Hi | Hi | Med | Low | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Med | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **56.5%** (61/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)