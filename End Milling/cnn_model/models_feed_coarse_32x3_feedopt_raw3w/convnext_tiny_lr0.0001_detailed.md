### convnext_tiny_lr0.0001  |  target=feed_coarse  |  scalogram=32x3_feedopt_raw3w  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run17 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Low | Low | Hi | Low | Low | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Med | Hi | Med | N |
| run45 | Med | Hi | Med | Hi | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Med | Med | Med | Med | Med | N |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **52.8%** (19/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)