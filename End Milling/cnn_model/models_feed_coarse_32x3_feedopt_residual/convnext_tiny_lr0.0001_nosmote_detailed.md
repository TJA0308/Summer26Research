### convnext_tiny_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run17 | Med | Hi | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Hi | Med | Hi | ~ |
| run31 | Med | Hi | Med | Med | Med | Hi | Y |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Low | Med | Hi | Med | N |
| run45 | Med | Med | Hi | Med | Med | Hi | Y |
| run5 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **61.1%** (22/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **58.3%** (7/12)