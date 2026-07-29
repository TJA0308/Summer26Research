### convnext_tiny_lr0.0001_conditioned  |  target=feed_coarse  |  scalogram=32x12_feedopt  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Hi | Med | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Low | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Low | Low | Med | Low | Med | N |
| run7 | Low | Low | Low | Med | Low | Med | Y |
| run9 | Med | Low | Med | Med | Med | Low | Y |

Window accuracy: **52.8%** (19/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **41.7%** (5/12)