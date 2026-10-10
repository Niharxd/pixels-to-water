# Additional workspace artifacts

This directory contains a copy of the lettuce LAI decision-engine notebook, MATLAB helper scripts, and the trained Random Forest model `DatasetLAI/lai_rf_model.joblib`.

The copied notebook expects `weather_eto.csv` and an input lettuce image in its working directory; neither is included here. The original lettuce workbook and RGB images are also external data. See the root [README](../README.md#data-required-to-reproduce-the-work) for source-data locations and reproduction notes.

The model estimates LAI from nine RGB summary features. The notebook combines that estimate with reference ET₀ and rainfall to assign a relative `LOW`, `MODERATE`, or `HIGH` demand class. This is an exploratory rule-based prototype; it does not calculate irrigation depth and has not been validated against field irrigation outcomes.
