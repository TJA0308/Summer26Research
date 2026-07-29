### resnet50_lr0.001_cond_gt  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Med | Med | Med | Med | Med | N |
| run3 | Hi | Med | Med | Hi | Med | Med | N |
| run31 | Med | Med | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Med | Med | Hi | Med | Med | N |
| run37 | Low | Med | Med | Med | Med | Med | N |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Med | Hi | Hi | Hi | Y |
| run7 | Low | Low | Med | Hi | Low | Med | Y |
| run9 | Med | Med | Med | Low | Med | Med | Y |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **33.3%** (4/12)