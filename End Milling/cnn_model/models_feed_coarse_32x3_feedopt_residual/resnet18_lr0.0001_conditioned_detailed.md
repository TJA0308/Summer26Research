### resnet18_lr0.0001_conditioned  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run17 | Med | Med | Hi | Hi | Hi | Med | ~ |
| run21 | Hi | Med | Med | Med | Med | Med | N |
| run25 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run3 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Low | Med | Med | Med | N |
| run45 | Med | Hi | Hi | Med | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Hi | Med | Low | Med | Y |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)