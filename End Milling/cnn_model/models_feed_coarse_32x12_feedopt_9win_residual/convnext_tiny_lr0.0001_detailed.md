### convnext_tiny_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Med | Hi | Hi | Med | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Low | Low | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Low | Low | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Med | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Low | Med | Low | Low | Med | Med | Med | Med | Low | Med | Med | N |
| run45 | Med | Med | Med | Low | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Low | Hi | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run7 | Low | Low | Low | Med | Med | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Med | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **60.2%** (65/108)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **66.7%** (8/12)