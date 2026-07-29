### convnext_tiny_lr0.0001_cascade_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Med | Med | Med | N |
| run17 | Med | Hi | Med | Low | Hi | Med | ~ |
| run21 | Hi | Med | Med | Med | Med | Med | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Med | Hi | Hi | Hi | Y |
| run37 | Low | Med | Low | Med | Med | Med | N |
| run45 | Med | Hi | Low | Hi | Hi | Hi | N |
| run5 | Hi | Low | Hi | Low | Low | Low | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Low | Low | Low | Low | N |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **41.7%** (5/12)