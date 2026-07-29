### convnext_tiny_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Low | Med | Hi | Low | Med | ~ |
| run21 | Hi | Med | Med | Hi | Med | Med | N |
| run25 | Low | Med | Low | Med | Med | Med | N |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Hi | Med | Med | Y |
| run36 | Hi | Low | Low | Hi | Low | Low | N |
| run37 | Low | Med | Low | Hi | Med | Med | N |
| run45 | Med | Low | Med | Med | Med | Med | Y |
| run5 | Hi | Low | Low | Med | Low | Low | N |
| run7 | Low | Med | Low | Med | Med | Med | N |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **27.8%** (10/36)
Run hard-vote accuracy: **16.7%** (2/12)
Run soft-vote accuracy: **25.0%** (3/12)