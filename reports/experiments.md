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

## Dataset Exploration — August 14, 2026

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

- One row has filename `.DS_Store` with an empty cultivar label — must be excluded before training.
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
