### convnext_tiny_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw9w  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Hi | Hi | Hi | Hi | Med | Hi | Med | Hi | Hi | N |
| run17 | Med | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Low | Hi | Med | Med | Med | Med | Hi | Hi | Med | Med | N |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | Med | Med | Med | Hi | Hi | Hi | N |
| run36 | Hi | Med | Med | Med | Med | Hi | Med | Hi | Hi | Hi | Med | Med | N |
| run37 | Low | Hi | Med | Med | Hi | Med | Low | Hi | Hi | Med | Hi | Hi | N |
| run45 | Med | Hi | Hi | Med | Med | Hi | Hi | Hi | Med | Med | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Med | Low | Med | Med | Med | Med | Low | Low | Med | Med | N |
| run9 | Med | Med | Med | Med | Med | Med | Med | Med | Low | Med | Med | Med | Y |

Window accuracy: **49.1%** (53/108)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)