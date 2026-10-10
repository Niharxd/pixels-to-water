# Pixels to Water

Pixels to Water explores how crop images and environmental data can support crop monitoring and irrigation decision support. The repository now contains two related research tracks: sorghum cultivar classification, and lettuce Leaf Area Index (LAI) estimation with a rule-based irrigation decision prototype.

The work is experimental. The models and thresholds have not been validated for field deployment, and the decision engine does not calculate a calibrated irrigation depth.

## Project status

### Sorghum cultivar classification

A balanced local subset of 5,000 sorghum field images was validated, with 50 images for each of 100 cultivar classes. The notebooks cover data checks, splitting, preprocessing, training, comparison, error analysis, and final model selection.

The evaluated ResNet-18 and EfficientNet-B0 classifiers achieved the following test results:

| Model | Test accuracy | Top-5 accuracy | Macro F1 |
| --- | ---: | ---: | ---: |
| ResNet-18 | 0.686 | 0.904 | 0.679 |
| EfficientNet-B0 | 0.742 | 0.928 | 0.738 |

EfficientNet-B0 is the current candidate based on these results. A paired significance test was not completed because aligned per-image predictions for both models are not available. See [`results/final_model_selection.json`](results/final_model_selection.json) and [`reports/experiments.md`](reports/experiments.md) for details and limitations.

### Lettuce LAI estimation

The LAI experiments use a clean 336-image split (234 training, 51 validation, 51 test samples). The current Random Forest baseline uses nine RGB summary features and achieved test MAE 0.0062, RMSE 0.0098, and R² 0.866. On the same split, the image-based ResNet-18 and EfficientNet-B0 regressors had negative test R², so they did not outperform the feature-based baseline in these experiments.

The trained Random Forest model and its decision-engine notebook are in [`workspace/DatasetLAI/`](workspace/DatasetLAI/). Clean-split metrics and prediction plots are in [`results/`](results/).

### Irrigation decision prototype

The prototype combines image-derived LAI with reference weather inputs. It calculates reference evapotranspiration (ET₀) using FAO-56 Penman-Monteith and classifies relative demand as LOW, MODERATE, or HIGH. The thresholds are empirical to the datasets used; they are not universal agronomic thresholds. The weather series is reference data and is not claimed to describe the lettuce experiments' actual location.

Read [`docs/irrigation_decision_engine.md`](docs/irrigation_decision_engine.md) for the inputs, feature extraction, thresholds, and rules. The decision engine is a transparent demonstration, not a field-validated irrigation controller.

## Repository contents

- [`notebooks/`](notebooks/) — ordered experiments for sorghum classification (01–15), LAI regression (16–21), the decision engine (22), and weather/ET₀ exploration.
- [`src/`](src/) — reusable project code.
- [`models/`](models/) — trained PyTorch checkpoints for the classification and LAI experiments.
- [`workspace/DatasetLAI/`](workspace/DatasetLAI/) — decision-engine notebook, MATLAB helper scripts, and Random Forest model copied from the surrounding workspace.
- [`results/`](results/) — metrics, summaries, plots, and prediction files.
- [`reports/experiments.md`](reports/experiments.md) — experiment log and dataset validation notes.
- [`docs/irrigation_decision_engine.md`](docs/irrigation_decision_engine.md) — decision-engine design and limitations.
- [`SWAP_4.3.0/`](SWAP_4.3.0/) — selected SWAP 4.3.0 documentation, license, tools, and bundled utilities.
- [`data/README.md`](data/README.md) — policy and notes for data kept outside Git.

## Data policy

The large image collections and dataset CSVs are intentionally not stored in this GitHub repository. This keeps the repository within GitHub's normal push limits and avoids redistributing source datasets. Obtain the source data through its original provider, follow its license and terms, and set the paths expected by the relevant notebooks before running them.

Trained model checkpoints, derived metrics, and selected analysis outputs are included. Dataset files remaining in a local workspace are not part of this repository unless they are explicitly added later.

## Getting started

Use Python and a virtual environment, then install the listed dependencies:

```bash
python -m venv .venv
# Activate the environment for your operating system, then:
pip install -r requirements.txt
jupyter lab
```

Open the notebooks in sequence for the experiment you want to reproduce. Before running data-dependent notebooks, provide the required source data and update any local paths. Model checkpoints and result files correspond to specific experiments; consult their notebook and JSON metadata before comparing results.

## Reproducibility and limitations

The notebooks and result metadata record the splits, seeds, metrics, and model settings available for each experiment. The datasets and split sizes differ between the sorghum classification and lettuce LAI tracks, so their scores should not be compared directly. The LAI test split is small, the decision thresholds are dataset-derived, and further validation with representative field data is needed before using the prototype for operational irrigation decisions.
