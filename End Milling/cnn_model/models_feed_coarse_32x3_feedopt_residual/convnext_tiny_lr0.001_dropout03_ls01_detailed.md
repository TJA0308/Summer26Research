### convnext_tiny_lr0.001_dropout03_ls01  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Med | Med | Med | Med | N |
| run25 | Low | Med | Med | Med | Med | Med | N |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Med | Med | Med | Med | N |
| run37 | Low | Med | Med | Med | Med | Med | N |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Med | Med | N |
| run7 | Low | Med | Med | Med | Med | Med | N |
| run9 | Med | Med | Hi | Low | Med | Hi | Y |

Window accuracy: **27.8%** (10/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **25.0%** (3/12)