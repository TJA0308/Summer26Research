### resnet50_lr0.0001_dropout03_ls01  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Low | Low | Low | Low | Y |
| run17 | Med | Low | Low | Low | Low | Low | N |
| run21 | Hi | Hi | Low | Low | Low | Low | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Low | Low | Low | N |
| run31 | Med | Hi | Low | Low | Low | Low | N |
| run36 | Hi | Hi | Low | Low | Low | Low | N |
| run37 | Low | Hi | Low | Low | Low | Low | Y |
| run45 | Med | Low | Low | Low | Low | Low | N |
| run5 | Hi | Hi | Low | Low | Low | Low | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)