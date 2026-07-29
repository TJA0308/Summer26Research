### convnext_tiny_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw9w_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | Low | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Low | Low | Low | Low | Med | Low | Med | Med | Low | Low | N |
| run36 | Hi | Med | Med | Med | Low | Med | Med | Med | Med | Med | Med | Med | N |
| run37 | Low | Low | Med | Med | Med | Low | Med | Med | Med | Med | Med | Med | N |
| run45 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Med | Med | Med | Med | Low | Med | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **47.2%** (51/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)