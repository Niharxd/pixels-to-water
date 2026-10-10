# Data

This directory contains documentation for data used by the project. Source datasets and generated LAI split CSVs are kept out of GitHub. A fresh clone therefore does not contain the images or LAI tables required to rerun data-dependent notebooks.

## Sorghum

The training workflow expects the original Sorghum image collection and its mapping/metadata CSVs in a `Dataset/` folder beside the repository. See the root [README](../README.md#data-required-to-reproduce-the-work) for the expected layout and reproduction notes. Obtain source data from its provider and follow its terms.

## Lettuce LAI

Notebook 16 reads the original `DatasetLAI/Numerical Data/` workbook and `DatasetLAI/Raw Images/` tree, validates the references, and generates the dataset and train/validation/test CSVs in this folder. Those generated files are local working data and are not tracked. Keep the source images and workbook outside GitHub as well.

The root `.gitignore` excludes the generated `lai_*.csv` files. Tracked project results, such as metrics and experiment manifests, are kept under `results/`.
