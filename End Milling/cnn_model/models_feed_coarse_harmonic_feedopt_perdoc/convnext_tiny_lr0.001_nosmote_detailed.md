### convnext_tiny_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=harmonic_feedopt_perdoc  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Hi | Low | Med | Med | N |
| run17 | Med | Med | Hi | Med | Med | Hi | Y |
| run21 | Hi | Hi | Hi | Low | Hi | Med | Y |
| run25 | Low | Low | Med | Low | Low | Low | Y |
| run3 | Hi | Low | Med | Low | Low | Low | N |
| run31 | Med | Med | Med | Low | Med | Med | Y |
| run36 | Hi | Med | Med | Low | Med | Med | N |
| run37 | Low | Med | Med | Low | Med | Low | ~ |
| run45 | Med | Med | Med | Low | Med | Med | Y |
| run5 | Hi | Low | Low | Med | Low | Low | N |
| run7 | Low | Low | Low | Med | Low | Low | Y |
| run9 | Med | Low | Low | Med | Low | Low | N |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **41.7%** (5/12)