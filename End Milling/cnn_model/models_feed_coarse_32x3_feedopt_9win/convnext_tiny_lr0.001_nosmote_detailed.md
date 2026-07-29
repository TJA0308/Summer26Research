### convnext_tiny_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Hi | Low | Low | Y |
| run17 | Med | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Hi | Low | Med | Low | Low | Hi | Low | Low | Hi | Low | Med | Y |
| run3 | Hi | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run31 | Med | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Med | Med | Hi | Low | Low | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Hi | Hi | Hi | Low | Low | Low | Low | Hi | Med | N |
| run45 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run5 | Hi | Hi | Low | Low | Low | Low | Low | Low | Low | Hi | Low | Low | N |
| run7 | Low | Low | Low | Low | Med | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **38.9%** (42/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **33.3%** (4/12)