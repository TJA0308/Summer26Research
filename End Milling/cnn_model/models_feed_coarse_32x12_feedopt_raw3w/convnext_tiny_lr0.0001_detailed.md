### convnext_tiny_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Low | Med | Med | Med | N |
| run17 | Med | Med | Low | Hi | Med | Med | Y |
| run21 | Hi | Hi | Hi | Low | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Med | Med | Med | Med | N |
| run31 | Med | Low | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Hi | Hi | Med | Hi | Hi | N |
| run5 | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Med | Low | Low | Y |
| run9 | Med | Med | Med | Low | Med | Med | Y |

Window accuracy: **61.1%** (22/36)
Run hard-vote accuracy: **75.0%** (9/12)
Run soft-vote accuracy: **75.0%** (9/12)