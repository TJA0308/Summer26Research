### convnext_tiny_lr0.0001_cascade_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Med | Med | Med | Hi | Low | Low | Low | Med | Med | N |
| run17 | Med | Hi | Low | Med | Hi | Med | Low | Low | Low | Hi | Low | Low | N |
| run21 | Hi | Hi | Med | Hi | Hi | Hi | Med | Med | Med | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Med | Med | Hi | Med | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Med | Hi | Hi | Low | Low | Hi | Hi | Med | Hi | Hi | Y |
| run37 | Low | Med | Low | Med | Low | Low | Med | Med | Med | Hi | Med | Med | N |
| run45 | Med | Med | Med | Med | Hi | Hi | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Med | Hi | Med | Med | Hi | Hi | Med | Med | N |
| run7 | Low | Low | Med | Low | Med | Low | Low | Low | Med | Med | Low | Low | Y |
| run9 | Med | Low | Low | Med | Low | Med | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **48.1%** (52/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)