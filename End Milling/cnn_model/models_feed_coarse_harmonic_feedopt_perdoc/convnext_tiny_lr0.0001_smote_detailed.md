### convnext_tiny_lr0.0001_smote  |  target=feed_coarse  |  scalogram=harmonic_feedopt_perdoc  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Low | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Med | Med | Med | Med | N |
| run25 | Low | Low | Low | Hi | Low | Low | Y |
| run3 | Hi | Med | Low | Med | Med | Med | N |
| run31 | Med | Hi | Med | Med | Med | Med | Y |
| run36 | Hi | Low | Low | Med | Low | Low | N |
| run37 | Low | Med | Med | Hi | Med | Med | N |
| run45 | Med | Low | Low | Med | Low | Med | ~ |
| run5 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Med | Hi | Hi | Hi | Hi | N |
| run9 | Med | Hi | Hi | Hi | Hi | Hi | N |

Window accuracy: **25.0%** (9/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **41.7%** (5/12)