### efficientnet_b0_lr0.0001_nosmote  |  target=feed  |  scalogram=32x12_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run1 | 5mm | 6mm | 7mm | 4mm | 6mm | 4mm | N |
| run17 | 6mm | 6mm | 7mm | 4mm | 6mm | 4mm | Y |
| run28 | 4mm | 6mm | 7mm | 4mm | 6mm | 4mm | ~ |
| run35 | 7mm | 6mm | 7mm | 4mm | 6mm | 4mm | N |
| run40 | 3mm | 6mm | 7mm | 3mm | 6mm | 3mm | ~ |
| run6 | 8mm | 6mm | 7mm | 3mm | 6mm | 3mm | N |

Window accuracy: **22.2%** (4/18)
Run hard-vote accuracy: **16.7%** (1/6)
Run soft-vote accuracy: **33.3%** (2/6)