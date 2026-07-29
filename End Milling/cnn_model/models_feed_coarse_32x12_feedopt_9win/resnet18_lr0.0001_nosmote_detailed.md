### resnet18_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run17 | Med | Low | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Med | Med | Low | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run25 | Low | Low | Low | Med | Med | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Hi | Hi | Hi | Hi | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Med | Low | Hi | Hi | Low | Low | Low | Hi | Low | Hi | ~ |
| run37 | Low | Low | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Low | Med | Low | Med | Med | Med | Low | Low | Med | Med | Med | Y |
| run5 | Hi | Med | Low | Low | Low | Hi | Hi | Low | Hi | Hi | Low | Low | N |
| run7 | Low | Low | Low | Med | Low | Med | Med | Med | Med | Med | Med | Low | ~ |
| run9 | Med | Low | Low | Low | Hi | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **31.5%** (34/108)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **50.0%** (6/12)