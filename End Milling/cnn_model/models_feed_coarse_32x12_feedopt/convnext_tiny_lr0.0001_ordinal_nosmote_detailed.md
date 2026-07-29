### convnext_tiny_lr0.0001_ordinal_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Low | Med | Med | N |
| run17 | Med | Med | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Med | Med | Med | Hi | ~ |
| run25 | Low | Med | Med | Med | Med | Med | N |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Hi | Med | Med | Y |
| run36 | Hi | Hi | Low | Med | Hi | Low | Y |
| run37 | Low | Hi | Low | Hi | Hi | Hi | N |
| run45 | Med | Med | Med | Low | Med | Med | Y |
| run5 | Hi | Med | Low | Med | Med | Med | N |
| run7 | Low | Med | Med | Med | Med | Med | N |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **25.0%** (9/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **25.0%** (3/12)