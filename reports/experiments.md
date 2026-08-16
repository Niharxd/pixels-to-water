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
