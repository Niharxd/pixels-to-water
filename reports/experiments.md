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
