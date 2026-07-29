### convnext_tiny_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_raw9w_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Med | Med | Med | Hi | Hi | Hi | Med | Hi | Med | Med | Hi | ~ |
| run37 | Low | Hi | Hi | Hi | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Low | Low | Med | Med | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | Low | Med | Med | Low | Low | Low | N |

Window accuracy: **61.1%** (66/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **66.7%** (8/12)