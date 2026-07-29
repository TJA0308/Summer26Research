### convnext_tiny_lr0.0001_cascade_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Low | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Med | Low | Med | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Low | Med | Hi | Low | Hi | N |
| run36 | Hi | Low | Low | Hi | Low | Low | N |
| run37 | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Med | Med | N |
| run7 | Low | Med | Low | Med | Med | Med | N |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **25.0%** (3/12)