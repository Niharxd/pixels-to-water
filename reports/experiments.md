# Experiment Log

This file records reproducible experiments for Pixels to Water.

All fields must be filled from actual runs. Do not enter estimated or
fabricated values.

---

## Experiment Template

- Experiment ID:
- Date:
- Model:
- Dataset:
- Dataset version:
- Number of images:
- Number of classes:
- Train/Validation/Test split:
- Image size:
- Augmentation:
- Optimizer:
- Learning rate:
- Batch size:
- Epochs:
- Random seed:
- Validation accuracy:
- Test accuracy:
- Top-5 accuracy:
- Precision:
- Recall:
- Macro F1:
- Training time:
- Inference time:
- Number of parameters:
- Model size:
- Observations:

---

## Dataset Exploration - August 14, 2026

### Files examined

- `train_cultivar_mapping.csv`
- `germplasm.csv`
- `season_6_aboveground_fresh_biomass_manual.csv`
- All PNG images in `Dataset/`

### Dataset layout discovery

The dataset is **flat**: images and CSVs are directly inside `Dataset/`, not under a `Sorghum/` subfolder as originally assumed. There is no `genotype.csv`; the third metadata file is `season_6_aboveground_fresh_biomass_manual.csv`.

### Mapping CSV columns

| Column | Content |
|---|---|
| `image` | PNG filename (e.g. `2017-06-26__11-18-57-106.png`) |
| `cultivar` | Cultivar identifier (e.g. `PI_257599`) |

### Dataset statistics

All values below come from actual inspection of the files on August 14, 2026. Fill in the blanks after running `01_data_exploration.ipynb`.

- PNG images on disk: _run notebook_
- Rows in mapping CSV: _run notebook_
- Unique cultivar labels: _run notebook_
- Min images / class: _run notebook_
- Max images / class: _run notebook_
- Mean images / class: _run notebook_
- Median images / class: _run notebook_

### Mapping quality

- One row has filename `.DS_Store` with an empty cultivar label - must be excluded before training.
- Duplicate image filenames: _run notebook_
- Mapped files missing on disk: _run notebook_
- Files on disk not in CSV: _run notebook_

### Image properties

- Format: PNG
- Color mode: _run notebook_
- Dimensions: _run notebook_ (may not be uniform)

### Metadata files

- `germplasm.csv`: germplasm registry with `germplasmName`, `germplasmPUI`, `season_4`, `season_6` columns. Relationship to image mapping requires further investigation.
- `season_6_aboveground_fresh_biomass_manual.csv`: manual aboveground fresh biomass measurements from MAC Field Scanner Season 6. Contains `plot`, `genotype`, `mean` (biomass in grams), and other agronomic columns. **Not used for cultivar classification.** Potential future use for biomass prediction.

### Issues to resolve before dataset creation

1. Remove the `.DS_Store` row from the mapping before any split.
2. Confirm whether duplicate image filenames (if any) are intentional.
3. Decide on image resolution for training (dimensions may vary).
4. Determine whether unmapped images on disk should be excluded.

---

## Dataset Mapping Validation - August 15, 2026

### Files used

- `Dataset/train_cultivar_mapping.csv` (primary)
- `Dataset/germplasm.csv` (cross-check only)
- All PNG images in `Dataset/` (existence check)

### Column names confirmed

- Image filename column: `image`
- Cultivar label column: `cultivar`

### Validation results (from actual data)

| Metric | Value |
|---|---|
| Total mapping rows | 22194 |
| Unique mapped images | 22194 |
| Duplicate image filenames | 0 |
| Images with conflicting labels | 0 |
| Missing cultivar labels | 1 |
| Mapped images physically present | 5000 |
| Mapped images physically missing | 17194 |
| Unmapped physical images | 0 |
| Valid image-cultivar pairs | 5000 |

### Key findings

- The mapping CSV contains 22194 rows but only 5000 images are physically present on disk. The remaining 17194 rows reference images that do not exist locally. This is expected - the local dataset is a 5000-image subset of the full Sorghum-100 dataset.
- The `.DS_Store` row (1 row, missing cultivar) was excluded as planned.
- No duplicate image filenames exist.
- No conflicting labels exist. Every image maps to exactly one cultivar.
- All 5000 physical images are present in the mapping CSV (0 unmapped physical images).
- The validated clean mapping contains exactly 5000 image-cultivar pairs.

### Validated cultivar distribution

- Unique cultivars: 100
- Min images per cultivar: 50
- Max images per cultivar: 50
- Mean images per cultivar: 50.0
- Median images per cultivar: 50.0

The local subset is perfectly balanced: exactly 50 images per cultivar across all 100 cultivars.

### Germplasm cross-check

- Identifier columns used: `cultivar` (mapping, e.g. `PI_257599`) vs `germplasmName` (germplasm, e.g. `PI257599`)
- Normalization applied: remove underscore before comparison
- Cultivars matched: 100 / 100
- Cultivars unmatched: 0

All 100 cultivar identifiers in the validated mapping correspond to entries in `germplasm.csv`.

### Output files

- `results/validated_image_cultivar_mapping.csv` - 5000 clean image-cultivar pairs
- `results/mapping_validation_report.csv` - validation metric counts
- `results/validated_cultivar_distribution.csv` - per-cultivar image counts
- `results/validated_cultivar_distribution.png` - distribution chart
- `results/validated_mapping_sample.csv` - 30-row manual verification sample

### Ready for August 16

The validated mapping (`results/validated_image_cultivar_mapping.csv`) is clean and ready for balanced subset creation. Since the local dataset is already perfectly balanced at 50 images per cultivar, August 16 will focus on creating the train/validation/test split from this validated mapping.

---

## Balanced Dataset Creation — August 16, 2026

### Source mapping

- `results/validated_image_cultivar_mapping.csv` (5000 clean image-cultivar pairs from August 15)

### Validated image count

- Total validated images: 5000
- All 5000 images confirmed present on disk before sampling.

### Cultivar statistics

| Metric | Value |
|---|---|
| Number of cultivars | 100 |
| Min images per cultivar | 50 |
| Max images per cultivar | 50 |
| Median images per cultivar | 50.0 |

The local dataset is already perfectly balanced: exactly 50 images per cultivar across all 100 cultivars.

### Sampling decision

Because every cultivar already has exactly 50 images, the maximum feasible balanced sample size is 50 per class. No cultivar was excluded. The chosen sample size equals the minimum (and only) class size.

- Chosen images per cultivar: 50
- Final subset size: 5000 (100 cultivars × 50 images)
- Random seed: 42
- Sampling strategy: stratified random sample with fixed seed (pandas `groupby.sample`, `random_state=42`)
- No images were duplicated; no images were copied or moved.

### Why this subset size

The target of ~5000 images is met exactly. With 100 cultivars and 50 images each, 100 × 50 = 5000 is both the maximum feasible balanced count and the target. No cultivars were dropped.

### Dataset version

`balanced_subset_v1`

Reproducible from:
- `results/validated_image_cultivar_mapping.csv`
- `../Dataset/` (original image directory, untouched)
- Random seed: 42
- Sampling rule: 50 images per cultivar, stratified random sample

### Output files

- `results/balanced_subset.csv` — 5000-row manifest (image, cultivar, source_path)
- `results/balanced_subset_distribution.csv` — per-cultivar selected image counts
- `results/balanced_subset_summary.csv` — summary metrics
- `results/balanced_subset_distribution.png` — distribution chart
- `src/create_balanced_subset.py` — reproducible sampling script

### Limitations

- The local dataset is a 5000-image subset of the full Sorghum-100 dataset (22194 rows in the original mapping CSV). The full dataset would allow larger per-class samples.
- Because the local subset is already perfectly balanced, the balanced manifest is identical to the validated mapping in terms of image count. The manifest adds `source_path` and is produced by a deterministic, seeded procedure.

---

## Dataset Split

### Source dataset

- `results/balanced_subset.csv` — 5000 images, 100 cultivars, 50 images per cultivar

### Split ratio

- Training   : 80%
- Validation : 10%
- Test       : 10%

### Stratification method

Scikit-learn `train_test_split` with `stratify=cultivar` applied in two passes:
1. 80% train / 20% temp (seed 42)
2. 50% of temp → validation / 50% → test (seed 42)

This guarantees every cultivar is represented proportionally in all three splits.

### Random seed

42 (fixed for all future experiments using this split)

### Split counts

| Split      | Images | Cultivars | % of Total |
|------------|--------|-----------|------------|
| Training   | 4000   | 100       | 80.00%     |
| Validation | 500    | 100       | 10.00%     |
| Test       | 500    | 100       | 10.00%     |
| **Total**  | **5000** | **100** | **100%**   |

### Per-cultivar distribution

Because the balanced subset has exactly 50 images per cultivar and 50 is evenly divisible by 10:

- Training   : 40 images per cultivar (all 100 cultivars)
- Validation : 5 images per cultivar (all 100 cultivars)
- Test       : 5 images per cultivar (all 100 cultivars)

The split is perfectly uniform across all cultivars. No class has a different count.

### Leakage checks

- train ∩ validation = empty ✓
- train ∩ test = empty ✓
- validation ∩ test = empty ✓
- train + validation + test = balanced subset (5000 images) ✓
- No duplicate images within any split ✓
- Every image has exactly one cultivar ✓
- All 100 cultivars represented in every split ✓

### Output files

- `results/train.csv` — 4000 rows (image, cultivar, split)
- `results/validation.csv` — 500 rows (image, cultivar, split)
- `results/test.csv` — 500 rows (image, cultivar, split)
- `results/dataset_split.csv` — 5000 rows, canonical master split file
- `results/split_class_distribution.csv` — per-cultivar counts across splits
- `results/split_summary.csv` — aggregate metrics
- `results/split_distribution.png` — visualization
- `src/create_dataset_split.py` — reproducible split script

### Limitations

- Each split references the original image files via filename only; images are not copied.
- With only 5 images per cultivar in validation and test, per-class evaluation metrics will have high variance. This is a consequence of the 5000-image local subset size, not a flaw in the split procedure.
- The split is fixed. All future models (ResNet-18, EfficientNet-B0) must use this exact split without modification.

---

## Image Preprocessing and Augmentation

### Input resolution

- 224 × 224 pixels
- Applied to both ResNet-18 and EfficientNet-B0 to enable a fair comparison

### Color format

- RGB (converted from PIL on load via `.convert("RGB")`)

### Normalization

- Standard ImageNet normalization
- mean = [0.485, 0.456, 0.406]
- std  = [0.229, 0.224, 0.225]
- Applied after tensor conversion, dynamically during loading
- Raw images on disk are never modified
- Rationale: both ResNet-18 and EfficientNet-B0 will be initialized from ImageNet-pretrained weights

### Training augmentation pipeline

| Step | Parameters | Rationale |
|---|---|---|
| RandomResizedCrop(224, scale=(0.8, 1.0)) | 80–100% of image area | Simulates varying camera distance and framing |
| RandomRotation(degrees=10) | ±10° | Accounts for slight camera tilt; conservative to preserve plant structure |
| RandomHorizontalFlip() | p=0.5 | Sorghum plants are bilaterally symmetric in the horizontal axis |
| ColorJitter(brightness=0.2, contrast=0.2, saturation=0.1, hue=0.05) | Mild | Accounts for lighting variation across field sessions |
| ToTensor() | — | Converts PIL image to float32 tensor in [0, 1] |
| Normalize(ImageNet) | — | Shifts to ImageNet distribution |

Vertical flip is omitted because field images have a consistent ground-up orientation; flipping vertically would produce unrealistic images.

Augmentation is conservative. No extreme rotations, heavy distortion, random erasing, or unrealistic color transformations are used.

### Validation preprocessing (deterministic)

| Step | Parameters |
|---|---|
| Resize(256) | Resize shorter edge to 256 |
| CenterCrop(224) | Crop center 224×224 |
| ToTensor() | — |
| Normalize(ImageNet) | — |

### Test preprocessing (deterministic)

Identical to validation preprocessing. No random operations.

### Batch size

- Default: 32
- Configurable via `make_loader(batch_size=...)`
- This is a practical baseline. Optimality is not claimed.

### Class mapping strategy

- Cultivar strings are sorted alphabetically and assigned integer indices 0–99
- Mapping is derived from the training manifest only
- Saved to `results/class_to_index.json` for reproducibility
- Identical mapping is used for training, validation, test, ResNet-18, and EfficientNet-B0

### Data leakage precautions

- train ∩ validation = empty (verified)
- train ∩ test = empty (verified)
- validation ∩ test = empty (verified)
- Class mapping is derived from training data only
- Augmentation is applied only to training data
- Validation and test transforms are deterministic
- No images were copied, moved, or modified on disk
- No new split was created; the canonical split from the previous stage is used unchanged

### Output files

- `src/preprocessing.py` — transform pipelines (train, val, test)
- `src/dataset.py` — SorghumDataset class and DataLoader factory
- `configs/preprocessing.yaml` — preprocessing configuration
- `results/class_to_index.json` — deterministic cultivar → index mapping (100 classes)
- `results/augmentation_examples.png` — original vs preprocessed vs augmented visualization
- `notebooks/04_preprocessing_and_augmentation.ipynb` — demonstration and verification notebook

### Verified

- Training batch shape: [32, 3, 224, 224], dtype=float32
- Validation batch shape: [32, 3, 224, 224], dtype=float32
- Test batch shape: [32, 3, 224, 224], dtype=float32
- All labels are valid integers in [0, 99]
- val_transform is deterministic (identical tensors on repeated calls)
- test_transform is deterministic (identical tensors on repeated calls)

---

- Training augmentation is applied only to training data
- No raw images were modified

# ResNet-18 Training

- Number of classes: 100
- Training samples: 4000
- Validation samples: 500
- Input size: [3, 224, 224]
- Pretrained weights: ResNet18_Weights.IMAGENET1K_V1
- Optimizer: AdamW
- Learning rate: 0.0001
- Batch size: 32
- Epochs completed: 20
- Best validation accuracy: 0.7180
- Best validation loss: 1.078231
- Best epoch: 20
- Training observations: Training completed for the configured maximum of 20 epochs. The selected checkpoint is from epoch 20 based on highest validation accuracy; validation loss was used as the tie-breaker.

# ResNet-18 Test Evaluation

- Number of classes: 100
- Test images: 500
- Test accuracy: 0.686000
- Precision: 0.725493
- Recall: 0.686000
- F1-score: 0.679440
- Top-5 accuracy: 0.904000

---

## EfficientNet-B0 Implementation

- Pretrained weights: `EfficientNet_B0_Weights.IMAGENET1K_V1`
- Input size: 224 × 224 pixels with the existing ImageNet preprocessing pipeline
- Number of classes: 100
- Total parameters: 4,135,648
- Trainable parameters: 4,135,648
- Forward-pass verification: successful; output shape was `[32, 100]`

# EfficientNet-B0 Training

- Number of classes: 100
- Training images: 4000
- Validation images: 500
- Batch size: 32
- Learning rate: 0.0001
- Optimizer: AdamW
- Epochs completed: 20
- Best validation accuracy: 0.7720
- Best validation loss: 0.837706
- Best epoch: 20

# EfficientNet-B0 Evaluation

- Test set size: 500 images
- Test accuracy: 0.744000
- Top-5 accuracy: 0.928000
- Precision: 0.781190
- Recall: 0.744000
- F1-score: 0.739890
- Important observations:
  - The model was evaluated on the existing held-out test split using the deterministic test preprocessing pipeline only.
  - The top-5 accuracy exceeds the top-1 accuracy, indicating that the correct cultivar is frequently among the model's five highest-confidence predictions.
  - The results are based on the checkpoint saved from the trained EfficientNet-B0 run and the actual computed metrics from the complete test set.

  # ResNet-18 vs EfficientNet-B0 Comparison

  The comparison below uses the existing test metric files only. No model was retrained or reevaluated for this comparison.

  | Metric | ResNet-18 | EfficientNet-B0 |
  |---|---:|---:|
  | Test Accuracy | 0.686000 | 0.742000 |
  | Precision | 0.725493 | 0.779000 |
  | Recall | 0.686000 | 0.742000 |
  | F1-score | 0.679440 | 0.737577 |
  | Top-5 Accuracy | 0.904000 | 0.928000 |

  | Model | Total Parameters | Trainable Parameters |
  |---|---:|---:|
  | ResNet-18 | 11,227,812 | 11,227,812 |
  | EfficientNet-B0 | 4,135,648 | 4,135,648 |

  EfficientNet-B0 achieved the higher test accuracy, precision, recall, F1-score, and top-5 accuracy. Under the experimental conditions used in this project, EfficientNet-B0 achieved the stronger overall classification performance. This conclusion is limited to these experiments and does not claim that the architecture is universally better.

## Model Comparison Visualizations

The visualization notebook displays separate percentage-formatted charts for Test Accuracy, Precision, Recall, F1-score, and Top-5 Accuracy, plus a total-parameter comparison for both models. The combined summary chart provides the main report-ready view of the five performance metrics, while the parameter chart shows that EfficientNet-B0 uses fewer total parameters than ResNet-18. All charts use the existing comparison results without retraining or reevaluation.

---

## Random Forest LAI Baseline — Official Clean Leakage-Free Split — September 5, 2026

This is the canonical and final Random Forest LAI baseline. The earlier RF evaluation used a split containing identical image contents across splits and therefore was not used as the final benchmark. Its notebook and derived prediction/plot artifacts are obsolete and are not part of the official experiment. The legacy metrics JSON remains only because the clean notebook uses it for a recorded comparison.

### Dataset and inputs

- Dataset: `data/lai_train_clean.csv`, `data/lai_val_clean.csv`, `data/lai_test_clean.csv`
- Train/Validation/Test split: 234 / 51 / 51
- Model: `RandomForestRegressor` with default settings and `random_state=42`
- Features: 9 RGB-derived features recomputed directly from each raw image
- Features used: `mean_red`, `mean_green`, `mean_blue`, `std_red`, `std_green`, `std_blue`, `mean_brightness`, `green_to_red_ratio`, `green_to_blue_ratio`
- Metadata and ground-truth measurements were not used as input features.
- Validation was used only as a diagnostic; no extensive hyperparameter tuning was performed.

### Clean split verification

| Check | Value |
|---|---:|
| Missing required raw RGB images | 0 |
| Cross-split identical image hashes | 0 |
| Cross-split duplicate paths | 0 |

### Evaluation metrics

- MAE: 0.006192920455
- RMSE: 0.009753515015
- R²: 0.865564843

### Output artifacts

- `notebooks/lai_baseline.ipynb`
- `results/lai_rf_clean_metrics.json`
- `results/lai_rf_clean_predictions.csv`
- `results/lai_rf_clean_actual_vs_predicted.png`
- `results/lai_rf_clean_error_distribution.png`

### Conclusion

The Random Forest LAI baseline was retrained using the leakage-free dataset split. These results are the official RF benchmark and replace the earlier contaminated-split RF evaluation for model comparison.

---

## EfficientNet-B0 LAI Regression — Clean Leakage-Free Split — September 6, 2026

This is a new EfficientNet-B0 regression experiment and is clearly distinguished from the older EfficientNet-B0 classification and LAI regression results above. The older EfficientNet-B0 notebook and its artifacts were not modified.

### Dataset and preprocessing

- Dataset: `data/lai_train_clean.csv`, `data/lai_val_clean.csv`, `data/lai_test_clean.csv`
- Train/Validation/Test split: 234 / 51 / 51
- Target: actual measured `LAI` column only
- Image paths: resolved exactly from the clean manifest values
- Color/input: RGB, resize/crop to 224 x 224
- Normalization: ImageNet mean/std
- Training augmentation only: random resized crop, horizontal flip, conservative rotation, and mild color jitter
- Validation and test preprocessing: deterministic resize and center crop

### Clean split verification

| Check | Value |
|---|---:|
| Missing image paths | 0 |
| Invalid LAI targets | 0 |
| Cross-split identical image hashes | 0 |
| Cross-split duplicate paths | 0 |

### Model and training

- Model: ImageNet-pretrained EfficientNet-B0 with a single-output regression layer
- Loss: `SmoothL1Loss`
- Optimizer: `Adam`, learning rate `0.0001`
- Batch size: 32
- Maximum epochs: 25
- Early stopping patience: 6 epochs
- Random seed: 42
- Best checkpoint: epoch 13, selected by lowest validation loss
- Epochs completed: 19

### Final clean test metrics

- MAE: 0.0741037178
- RMSE: 0.0879353799
- R²: -9.9274252305

The metrics above are from the final/best validation-loss model evaluated once on the 51-image clean test set. No extensive hyperparameter tuning was performed, and no legacy LAI split was used.

### Output artifacts

- `notebooks/lai_efficientnet_b0_clean_split.ipynb`
- `results/lai_efficientnet_b0_clean_metrics.json`
- `results/lai_efficientnet_b0_clean_predictions.csv`
- `results/lai_efficientnet_b0_clean_training_curve.png`
- `results/lai_efficientnet_b0_clean_actual_vs_predicted.png`
- `results/lai_efficientnet_b0_clean_error_distribution.png`
- `models/lai_efficientnet_b0_clean_best.pth`

### Conclusion

This clean EfficientNet-B0 result is a leakage-free re-evaluation and should be compared with the clean Random Forest and clean ResNet-18 experiments, not with the older EfficientNet-B0 result.

---

## Final LAI Model Comparison — Clean Leakage-Free Test Split — September 6, 2026

This section is the final reporting comparison of the three LAI estimation models. It uses only the verified clean-split metrics and predictions; historical experiments above remain available for context but are not used as the final benchmark.

### Clean split and verification

- Train/Validation/Test: 234 / 51 / 51
- Missing image paths: 0
- Invalid targets: 0
- Cross-split identical image hashes: 0
- Cross-split duplicate paths: 0

### Final clean test metrics

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Random Forest | 0.006192920455 | 0.009753515015 | 0.865564843 |
| ResNet-18 | 0.096753565622 | 0.120569789972 | -19.543174905 |
| EfficientNet-B0 | 0.074103717822 | 0.087935379925 | -9.927425230 |

Random Forest performed best among the three evaluated models on this dataset and experimental setup. It had the lowest MAE, lowest RMSE, and highest R², with R² = 0.865565. Both CNN models produced negative R² values on the clean test set. This conclusion is limited to this dataset and experimental setup and does not claim that Random Forest is universally superior to deep learning.

### Interpretation

Random Forest used nine simple RGB-derived statistical features, while ResNet-18 and EfficientNet-B0 performed direct image-based regression. For this dataset and available sample size, the engineered RGB statistical representation was substantially more effective for LAI estimation than the evaluated end-to-end CNN regression approaches. Dataset size, dataset characteristics, target distribution, and model configuration can affect deep-learning performance; CNNs are not inherently unsuitable for LAI estimation.

### Leakage-control note

An earlier Random Forest evaluation used a split containing identical image contents across different splits and was rejected as the final benchmark. The leakage-free split was subsequently verified with zero cross-split identical image hashes and zero cross-split duplicate paths. All final model comparisons use this clean split. The official Random Forest result is R² = 0.865565; the earlier R² = 0.912224 result is not used.

The final comparison artifacts are saved in `results/lai_model_comparison.csv`, `results/lai_model_comparison_mae.png`, `results/lai_model_comparison_rmse.png`, `results/lai_model_comparison_r2.png`, and `results/lai_model_prediction_comparison.png`.

For plain-text compatibility, the official Random Forest R-squared is also recorded as `R2 = 0.865565`; the rejected historical value is `R2 = 0.912224`.

---

# Statistical Reliability

The requested paired comparison was checked against the existing saved results. The test manifest and aggregate metrics are available, but no saved per-image predictions for either model were found. The earlier evaluation notebooks hold predictions only in memory, and `results/error_analysis_summary.csv` contains aggregated directed error counts; neither can determine the paired 2x2 counts.

- Test set size: 500
- ResNet-18 correct predictions: 343
- ResNet-18 incorrect predictions: 157
- EfficientNet-B0 correct predictions: 371
- EfficientNet-B0 incorrect predictions: 129
- Paired comparison counts:

  |  | EfficientNet Correct | EfficientNet Wrong |
  |---|---:|---:|
  | ResNet Correct | unavailable | unavailable |
  | ResNet Wrong | unavailable | unavailable |

- McNemar test statistic: not calculated
- p-value: not calculated
- Significance level: alpha = 0.05
- Plain-English interpretation: There is not enough paired prediction information to perform McNemar's test. Therefore, no statistical evidence-based conclusion about a difference between the models is reported from this test.
- Missing information: one correctness result per test image for both ResNet-18 and EfficientNet-B0, aligned by image.

# Model Error Analysis

The existing ResNet-18 and EfficientNet-B0 checkpoints were evaluated on the existing 500-image test split using the saved class mapping and deterministic test preprocessing. No model, dataset, preprocessing, or split was changed.

## Error counts

| Model | Number of Errors |
|---|---:|
| ResNet-18 | 157 |
| EfficientNet-B0 | 129 |

EfficientNet-B0 made 28 fewer test-set misclassifications.

## Most frequent directed confusion pairs

| Model | True Cultivar | Predicted Cultivar | Number of Errors |
|---|---|---|---:|
| ResNet-18 | PI_329299 | PI_329301 | 3 |
| ResNet-18 | PI_152967 | PI_257599 | 2 |
| ResNet-18 | PI_154844 | PI_152860 | 2 |
| ResNet-18 | PI_154844 | PI_154944 | 2 |
| ResNet-18 | PI_156178 | PI_255239 | 2 |
| EfficientNet-B0 | PI_152730 | PI_146890 | 4 |
| EfficientNet-B0 | PI_152751 | PI_152733 | 2 |
| EfficientNet-B0 | PI_221651 | PI_157035 | 2 |
| EfficientNet-B0 | PI_276837 | PI_253986 | 2 |
| EfficientNet-B0 | PI_329300 | PI_329301 | 2 |

## Comparison observations

- The models shared 28 directed confusion pairs, but their complete error sets were not identical.
- ResNet-18 had fewer errors for 24 cultivars, EfficientNet-B0 had fewer errors for 37 cultivars, and the models were tied for 39 cultivars.
- The notebook displays eight actual misclassified images per model with true cultivar, predicted cultivar, and confidence.
- The images and predictions do not support a specific visual explanation for the errors, so no cause is claimed.

The complete observed directed confusion counts are saved in `results/error_analysis_summary.csv`.

---

# Final Model Selection

- Selected model: EfficientNet-B0
- Key results on the existing 500-image test set:

  | Metric | ResNet-18 | EfficientNet-B0 |
  |---|---:|---:|
  | Test accuracy | 0.686000 | 0.742000 |
  | Precision | 0.725493 | 0.779000 |
  | Recall | 0.686000 | 0.742000 |
  | F1-score | 0.679440 | 0.737577 |
  | Top-5 accuracy | 0.904000 | 0.928000 |

- Statistical reliability finding: McNemar's test was not calculated because aligned per-image predictions for both models are not saved. The paired counts, test statistic, and p-value are therefore unavailable.
- Important error-analysis finding: EfficientNet-B0 had 129 recorded errors versus 157 for ResNet-18, 28 fewer errors overall. EfficientNet-B0 had fewer errors for 37 cultivars, ResNet-18 had fewer for 24, and 39 cultivars were tied.
- Reason: Based on the experiments conducted in this project, EfficientNet-B0 is selected as the final candidate because it demonstrated the strongest overall performance under the evaluated conditions. This selection does not claim that the architecture is universally better and is not supported by a claim of statistically significant difference.
- Output: `results/final_model_selection.json`

---

# Limitations

- The local dataset is a 5000-image subset of the full Sorghum-100 dataset.
- The test set contains 500 images, with 5 images per cultivar, so per-class evaluation metrics have high variance.
- McNemar's paired comparison was not calculated because aligned per-image predictions for both models are not saved.

# Final Conclusion

The project tested ResNet-18 and EfficientNet-B0 for 100-class sorghum cultivar classification using the same existing dataset split and preprocessing. EfficientNet-B0 was selected as the final candidate because it had higher accuracy, precision, recall, F1-score, and top-5 accuracy, and fewer recorded test errors. The models were compared using existing aggregate metrics and error-analysis results; a paired McNemar test could not be performed because aligned per-image predictions were unavailable. The main evaluation limitation is the 5-image-per-cultivar test set, which makes per-class metrics high variance. The next practical step is to carry the selected EfficientNet-B0 checkpoint into application integration, without claiming universal superiority.

---

# LAI Error Analysis - September 16, 2026

The final LAI error analysis used the existing clean test split and saved per-image predictions only. No model was retrained, tuned, or modified. The clean test set contains 51 images, and `environment` and `GrowthStage` metadata were available for all 51 rows.

## Clean test metrics

| Model | MAE | RMSE | R² | Mean error (predicted - actual) |
|---|---:|---:|---:|---:|
| Random Forest | 0.006192920 | 0.009753515 | 0.865565 | +0.003529709 |
| ResNet-18 | 0.096753566 | 0.120569790 | -19.543175 | -0.039741542 |
| EfficientNet-B0 | 0.074103718 | 0.087935380 | -9.927425 | -0.002105238 |

Random Forest is the current LAI candidate because it has the lowest clean-test MAE and RMSE and the only positive R² among the three evaluated models. This conclusion uses the existing results without artificially improving any model.

## Error behavior

- Random Forest overpredicted on average, with 35 overpredictions and 16 underpredictions. Its largest MAE by actual-LAI range was 0.010401987 for `0.03-0.06` LAI; the corresponding bias was positive (+0.010401987), indicating overprediction in that range.
- ResNet-18 underpredicted strongly overall. Its largest range MAE was 0.125610904 for `0.03-0.06` LAI, with bias -0.096064990. It also had the largest environment MAE on indoor images (0.115023891) and the largest growth-stage MAE during HeadDevelopment (0.106404496).
- EfficientNet-B0 was close to unbiased overall, but its errors remained much larger than Random Forest. Its largest range MAE was 0.086603207 for `>0.06` LAI. It was nearly equal across environments (indoor MAE 0.074055036; outdoor MAE 0.074154347).
- For Random Forest, indoor MAE was 0.008975665 versus 0.003298867 outdoors. By GrowthStage, its largest MAE was during HeadDevelopment (0.007780540), followed by Harvest (0.004632119) and Vegetative (0.002709518).

The main weak points are therefore the Random Forest `0.03-0.06` LAI range, indoor images, and HeadDevelopment samples. These subgroup findings are descriptive and should be interpreted cautiously because the clean test set is small.

## Outputs

The reproducible notebook is `notebooks/21_lai_error_analysis.ipynb`. It saves:

- `results/lai_error_analysis.png`
- `results/lai_error_by_range.png`
- `results/lai_error_by_environment.png`
- `results/lai_error_by_growth_stage.png`
- `results/lai_error_analysis_overall.csv`
- `results/lai_error_by_range.csv`
- `results/lai_error_by_environment.csv`
- `results/lai_error_by_growth_stage.csv`

The earlier classification model-selection conclusion in this report is separate from this LAI regression conclusion.

---
