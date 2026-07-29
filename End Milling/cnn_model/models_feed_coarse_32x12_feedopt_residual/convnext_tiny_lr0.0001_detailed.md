### convnext_tiny_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Med | Hi | Med | Med | Hi | Y |
| run21 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Hi | Med | Med | N |
| run31 | Med | Hi | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Low | Med | Med | Low | ~ |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Med | Med | Low | Med | Med | N |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **58.3%** (21/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)