### convnext_tiny_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | Med | Med | Low | Hi | Med | Med | N |
| run17 | Med | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Med | Med | Hi | Hi | Med | Med | Med | Hi | Med | Hi | ~ |
| run25 | Low | Med | Low | Hi | Med | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Low | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Low | Low | Low | Hi | Hi | Med | Med | Hi | Hi | Hi | Y |
| run37 | Low | Low | Med | Med | Med | Hi | Low | Med | Med | Low | Med | Med | N |
| run45 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Med | Low | Low | N |
| run5 | Hi | Hi | Med | Low | Low | Med | Med | Med | Med | Hi | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Med | Med | Med | Med | Med | Med | Med | N |
| run9 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **25.9%** (28/108)
Run hard-vote accuracy: **16.7%** (2/12)
Run soft-vote accuracy: **25.0%** (3/12)