### convnext_tiny_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Med | Med | Med | Hi | Hi | Hi | Med | Hi | Med | Med | N |
| run17 | Med | Low | Hi | Hi | Med | Hi | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Hi | Med | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Med | Med | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Low | Low | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Low | Low | Low | Low | Med | Hi | Hi | Hi | Hi | Low | Hi | ~ |
| run37 | Low | Low | Low | Low | Low | Hi | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Low | Med | Med | Med | Med | Med | Med | Med | Low | Med | Med | Y |
| run5 | Hi | Hi | Low | Med | Med | Med | Med | Med | Med | Hi | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Med | Med | Med | Med | Med | Med | Med | N |
| run9 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **42.6%** (46/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **50.0%** (6/12)