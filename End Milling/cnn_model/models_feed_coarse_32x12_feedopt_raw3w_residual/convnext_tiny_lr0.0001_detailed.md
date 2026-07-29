### convnext_tiny_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Med | Low | Med | Med | Med | Y |
| run21 | Hi | Med | Med | Med | Med | Med | N |
| run25 | Low | Low | Low | Med | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Med | Low | Med | Med | N |
| run37 | Low | Low | Med | Med | Med | Med | N |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Low | Low | Low | Low | N |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)