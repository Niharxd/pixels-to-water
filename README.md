# Pixels to Water
### Deep Learning-Based Crop Monitoring and Intelligent Irrigation Control

This project investigates deep-learning-based crop image analysis and will
progressively integrate environmental information to support intelligent
irrigation decision-making.

---

## Overview

The core idea is to extract meaningful visual features from crop field images
using deep learning, then combine those features with environmental data
(weather, soil conditions) to build a crop monitoring and irrigation system.

**Planned high-level pipeline:**

```
Crop Image
     ↓
Deep Learning Model
     ↓
Crop Visual Features
     ↓
Environmental Information
     ↓
Crop Monitoring
     ↓
Intelligent Irrigation
```

---

## Current Experimental Milestone

The first milestone is a controlled comparison of two CNN architectures:

| Model           | Source      |
|-----------------|-------------|
| ResNet-18       | torchvision |
| EfficientNet-B0 | torchvision |

Both models will be trained and evaluated on the
**Sorghum-100 Cultivar Identification – FGVC 9** dataset.

The dataset contains field RGB images of sorghum plants labelled by cultivar.
It does **not** contain biomass measurements, irrigation labels, soil data,
or weather data. It is used here for cultivar classification as the first
step toward a broader crop monitoring pipeline.

Detailed dataset statistics will be documented after the data exploration
stage — no numbers are assumed here.

Both models will be trained under **identical conditions** (same subset,
split, resolution, augmentation, optimizer, learning rate, batch size,
epochs, and random seed) to ensure a fair comparison.

---

## Project Status

```
[✓] Repository initialization
[✓] Dataset exploration
[ ] Dataset validation
[ ] Balanced dataset creation
[ ] Train/validation/test split
[ ] Image preprocessing
[ ] ResNet-18 training
[ ] EfficientNet-B0 training
[ ] Model comparison
[ ] Error analysis
[ ] Best model selection
[ ] Crop monitoring integration
[ ] Irrigation module
[ ] Final application
```

---

## Repository Structure

```
pixels-to-water/
├── configs/          # Experiment configuration files (future)
├── data/             # Data README only — raw files are external
├── models/           # Saved model checkpoints (git-ignored)
├── notebooks/        # Jupyter notebooks for exploration and analysis
├── reports/          # Experiment logs and findings
├── results/          # Evaluation outputs, plots (result images not ignored)
├── src/              # Source code
│   ├── dataset.py
│   ├── preprocessing.py
│   ├── models.py
│   ├── train.py
│   └── evaluate.py
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Dataset

**Sorghum-100 Cultivar Identification – FGVC 9**
Source: Kaggle / FGVC Workshop 2022

The raw dataset is stored **outside** this repository and is never committed
to GitHub. See `data/README.md` for details.

---

## Reproducibility

All experiments will be logged in `reports/experiments.md` with full
hyperparameter records. No results are reported until they are produced
by an actual experiment.
