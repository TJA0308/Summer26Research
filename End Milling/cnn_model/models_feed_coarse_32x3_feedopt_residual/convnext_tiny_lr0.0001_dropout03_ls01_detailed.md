### convnext_tiny_lr0.0001_dropout03_ls01  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Low | Hi | Hi | N |
| run17 | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Med | Med | Med | Med | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Med | Med | Med | Med | N |
| run37 | Low | Hi | Low | Med | Hi | Med | N |
| run45 | Med | Low | Low | Med | Low | Med | ~ |
| run5 | Hi | Low | Hi | Med | Low | Med | N |
| run7 | Low | Low | Med | Low | Low | Low | Y |
| run9 | Med | Med | Low | Low | Low | Low | N |

Window accuracy: **47.2%** (17/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **41.7%** (5/12)