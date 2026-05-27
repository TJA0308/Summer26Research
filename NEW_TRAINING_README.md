# New Training Runs — ResNet18 & ConvNeXt-Tiny

Two pipelines, two backbones, four targets. All runs use the same base settings:
`--lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine`

`--weighted_loss` only for `feed_coarse` (class imbalance requires it).  
SMOTE is loaded automatically in Pipeline A (CSVs in scalogram dir).  
SMOTE requires `--smote` flag in Pipeline B.

Epochs: speed=30, doc=31, roughness=31, feed_coarse=33

---

## Pipeline A — Standard CWT (`scalograms_10w`, `cnn_train.py`)

### ResNet18

```powershell
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone resnet18 --epochs 30 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save nonhilbert_speed_rn18.pt

python cnn_model/cnn_train.py --img_dir scalograms_10w --target doc --backbone resnet18 --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save nonhilbert_doc_rn18.pt

python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness --backbone resnet18 --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save nonhilbert_roughness_rn18.pt

python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone resnet18 --epochs 33 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --weighted_loss --save nonhilbert_feed_coarse_rn18.pt
```

### ConvNeXt-Tiny

```powershell
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone convnext_tiny --epochs 30 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save nonhilbert_speed_cnxt.pt

python cnn_model/cnn_train.py --img_dir scalograms_10w --target doc --backbone convnext_tiny --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save nonhilbert_doc_cnxt.pt

python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness --backbone convnext_tiny --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save nonhilbert_roughness_cnxt.pt

python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone convnext_tiny --epochs 33 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --weighted_loss --save nonhilbert_feed_coarse_cnxt.pt
```

---

## Pipeline B — SES 4-Channel (`scalograms_ses_10w`, `cnn_train_hilbert.py`)

### ResNet18

```powershell
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed --backbone resnet18 --epochs 30 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save hilbert_speed_resnet18.pt

python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target doc --backbone resnet18 --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save hilbert_doc_resnet18.pt

python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target roughness --backbone resnet18 --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save hilbert_roughness_resnet18.pt

python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target feed_coarse --backbone resnet18 --epochs 33 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --weighted_loss --smote --save hilbert_feed_coarse_resnet18.pt
```

### ConvNeXt-Tiny

```powershell
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed --backbone convnext_tiny --epochs 30 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save hilbert_speed_convnext.pt

python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target doc --backbone convnext_tiny --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save hilbert_doc_convnext.pt

python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target roughness --backbone convnext_tiny --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save hilbert_roughness_convnext.pt

python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target feed_coarse --backbone convnext_tiny --epochs 33 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --weighted_loss --smote --save hilbert_feed_coarse_convnext.pt
```

---

## Results

Fill in after training. Window accuracy = per scalogram; Run MV = majority vote over 10 windows.

### Pipeline A — Standard CWT

| Target | Epochs | Backbone | Window Acc | Run MV Acc | Model File |
|--------|--------|----------|-----------|-----------|-----------|
| Speed | 30 | ResNet18 | | | `nonhilbert_speed_rn18.pt` |
| Speed | 30 | ConvNeXt-Tiny | | | `nonhilbert_speed_cnxt.pt` |
| DOC | 31 | ResNet18 | | | `nonhilbert_doc_rn18.pt` |
| DOC | 31 | ConvNeXt-Tiny | | | `nonhilbert_doc_cnxt.pt` |
| Roughness | 31 | ResNet18 | | | `nonhilbert_roughness_rn18.pt` |
| Roughness | 31 | ConvNeXt-Tiny | | | `nonhilbert_roughness_cnxt.pt` |
| Feed Coarse | 33 | ResNet18 | | | `nonhilbert_feed_coarse_rn18.pt` |
| Feed Coarse | 33 | ConvNeXt-Tiny | | | `nonhilbert_feed_coarse_cnxt.pt` |

### Pipeline B — SES 4-Channel

| Target | Epochs | Backbone | Window Acc | Model File |
|--------|--------|----------|-----------|-----------|
| Speed | 30 | ResNet18 | | `hilbert_speed_resnet18.pt` |
| Speed | 30 | ConvNeXt-Tiny | | `hilbert_speed_convnext.pt` |
| DOC | 31 | ResNet18 | | `hilbert_doc_resnet18.pt` |
| DOC | 31 | ConvNeXt-Tiny | | `hilbert_doc_convnext.pt` |
| Roughness | 31 | ResNet18 | | `hilbert_roughness_resnet18.pt` |
| Roughness | 31 | ConvNeXt-Tiny | | `hilbert_roughness_convnext.pt` |
| Feed Coarse | 33 | ResNet18 | | `hilbert_feed_coarse_resnet18.pt` |
| Feed Coarse | 33 | ConvNeXt-Tiny | | `hilbert_feed_coarse_convnext.pt` |
