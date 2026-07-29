### convnext_tiny_lr0.0001_cascade_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Low | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Med | Med | Hi | Med | Med | N |
| run25 | Low | Med | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Hi | Hi | Hi | Hi | N |
| run45 | Med | Low | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Med | Med | Med | Med | N |
| run7 | Low | Med | Med | Med | Med | Med | N |
| run9 | Med | Med | Low | Med | Med | Med | Y |

Window accuracy: **30.6%** (11/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)