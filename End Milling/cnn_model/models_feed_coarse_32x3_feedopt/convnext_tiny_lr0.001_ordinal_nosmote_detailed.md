### convnext_tiny_lr0.001_ordinal_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Low | Med | Med | N |
| run17 | Med | Med | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Med | Low | Low | Med | Y |
| run3 | Hi | Med | Med | Low | Med | Low | N |
| run31 | Med | Med | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Med | Med | Hi | Med | Med | N |
| run37 | Low | Med | Med | Med | Med | Med | N |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Low | Med | Med | Med | Med | N |
| run7 | Low | Low | Low | Med | Low | Low | Y |
| run9 | Med | Low | Med | Med | Med | Med | Y |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **33.3%** (4/12)