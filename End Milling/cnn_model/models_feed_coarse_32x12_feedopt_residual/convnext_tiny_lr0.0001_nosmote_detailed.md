### convnext_tiny_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Med | Med | Med | N |
| run17 | Med | Hi | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Med | Hi | Hi | Hi | Y |
| run25 | Low | Med | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Med | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Med | Med | Med | Med | N |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Hi | Med | Med | Med | N |
| run7 | Low | Low | Med | Low | Low | Low | Y |
| run9 | Med | Med | Med | Low | Med | Med | Y |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **66.7%** (8/12)