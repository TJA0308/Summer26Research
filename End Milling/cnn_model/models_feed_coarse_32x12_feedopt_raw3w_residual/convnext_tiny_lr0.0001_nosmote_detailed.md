### convnext_tiny_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Low | Med | Med | Med | Low | Y |
| run21 | Hi | Low | Low | Low | Low | Low | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Hi | Low | Hi | Med | Y |
| run31 | Med | Low | Low | Low | Low | Low | N |
| run36 | Hi | Low | Hi | Low | Low | Low | N |
| run37 | Low | Med | Med | Med | Med | Med | N |
| run45 | Med | Hi | Med | Med | Med | Med | Y |
| run5 | Hi | Low | Low | Low | Low | Low | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **33.3%** (4/12)