# Data

## External Dataset Policy

The raw Sorghum dataset is stored **outside** this repository.
Large image files will never be committed to GitHub.

The `.gitignore` at the repository root excludes all image formats,
archive files, and the `Dataset/` directory.

## Expected External Structure

```
Dataset/
├── *.png                          # Raw field RGB images (flat layout)
├── train_cultivar_mapping.csv     # Image-to-cultivar label mapping
├── germplasm.csv
└── season_6_aboveground_fresh_biomass_manual.csv
```

## What Belongs Here

Only non-data artefacts belong inside this `data/` directory:

- Subset manifests (CSV files listing selected image paths) — future
- Split definitions (train / validation / test file lists) — future

Raw images and the original CSVs remain in the external `Dataset/` location.

## Dataset Statistics

Dataset statistics (class counts, image dimensions, missing files, etc.)
will be documented only after the data exploration notebook is executed.
No numbers are assumed or fabricated here.

## Preprocessing

Image preprocessing and augmentation will be implemented in
`src/preprocessing.py` during the preprocessing stage.
