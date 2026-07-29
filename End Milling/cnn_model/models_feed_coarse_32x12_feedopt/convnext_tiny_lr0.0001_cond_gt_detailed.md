### convnext_tiny_lr0.0001_cond_gt  |  target=feed_coarse  |  scalogram=32x12_feedopt  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Low | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Med | Med | Low | Med | Med | N |
| run3 | Hi | Low | Med | Med | Med | Med | N |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Hi | Low | Med | Low | ~ |
| run45 | Med | Low | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Hi | Med | Hi | Med | Y |
| run7 | Low | Med | Med | Med | Med | Med | N |
| run9 | Med | Med | Low | Low | Low | Med | ~ |

Window accuracy: **30.6%** (11/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **41.7%** (5/12)