### resnet50_lr0.001_dropout03_ls01_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Hi | Hi | Hi | Hi | N |
| run17 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Hi | Med | Low | Hi | Low | ~ |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Med | Hi | Hi | Hi | N |
| run45 | Med | Med | Hi | Hi | Hi | Hi | N |
| run5 | Hi | Med | Med | Hi | Med | Med | N |
| run7 | Low | Hi | Hi | Med | Hi | Hi | N |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **33.3%** (12/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **33.3%** (4/12)