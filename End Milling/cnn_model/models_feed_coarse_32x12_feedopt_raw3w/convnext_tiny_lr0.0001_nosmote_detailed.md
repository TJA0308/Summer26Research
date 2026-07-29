### convnext_tiny_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Med | Low | Low | Y |
| run17 | Med | Med | Low | Med | Med | Low | Y |
| run21 | Hi | Med | Med | Med | Med | Med | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Med | Low | Low | N |
| run31 | Med | Low | Med | Low | Low | Low | N |
| run36 | Hi | Med | Hi | Med | Med | Med | N |
| run37 | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Low | Med | Low | Low | Low | N |
| run5 | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run7 | Low | Med | Med | Med | Med | Med | N |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **41.7%** (5/12)