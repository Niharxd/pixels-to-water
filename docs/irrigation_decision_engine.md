# Irrigation Decision Engine

## Purpose

This document describes the rule-based irrigation decision-support engine
developed as part of the project:

**"From Pixels to Water: An Autonomous Imaging System for Daily Crop
Monitoring and Irrigation Decision Support"**

The engine combines image-derived Leaf Area Index (LAI) predictions with
reference weather data to produce a daily irrigation demand classification:
**LOW**, **MODERATE**, or **HIGH**.

This is a decision-support prototype. It does not produce a physically
calibrated irrigation depth. It is designed to be transparent, reproducible,
and explainable.

---

## Inputs

### RGB Image

A lettuce crop image captured under either Indoor or Outdoor conditions.
The image is used to extract nine RGB-based features that are fed into the
trained Random Forest model to predict LAI.

**Image feature extraction:**

| Feature              | Description                                      |
|----------------------|--------------------------------------------------|
| mean_red             | Mean pixel value of the red channel              |
| mean_green           | Mean pixel value of the green channel            |
| mean_blue            | Mean pixel value of the blue channel             |
| std_red              | Standard deviation of the red channel            |
| std_green            | Standard deviation of the green channel          |
| std_blue             | Standard deviation of the blue channel           |
| mean_brightness      | Mean of (R + G + B) / 3                          |
| green_to_red_ratio   | mean_green / (mean_red + epsilon)                |
| green_to_blue_ratio  | mean_green / (mean_blue + epsilon)               |

### Predicted LAI

Leaf Area Index predicted by the trained Random Forest Regressor using the
nine image-derived features above.

**Model:** Random Forest Regressor (`lai_rf_model.joblib`)

**Clean test metrics (do not modify):**

| Metric | Value    |
|--------|----------|
| MAE    | 0.006193 |
| RMSE   | 0.009754 |
| R²     | 0.865565 |

**Dataset source:** Mendeley lettuce RGB-LAI dataset
(Indoor and Outdoor lettuce growth stages: Vegetative, HeadDevelopment, Harvest)

### Weather

The weather dataset provides **reference environmental inputs** for ET₀
calculation and irrigation demand estimation.

**Important:** The weather data is NOT claimed to be the measured
environmental conditions at the Mendeley lettuce experiment location.
It is used as representative reference weather for demonstrating the
irrigation decision pipeline.

**Weather dataset metadata:**

| Field          | Value                                                        |
|----------------|--------------------------------------------------------------|
| Source         | NASA POWER (via CSV export)                                  |
| Location       | Latitude 36.5°N, Longitude 119.5°W (Central California, USA)|
| Elevation      | ~249.47 m                                                    |
| Date range     | 2018-01-01 to 2023-12-31                                     |
| Variables used | T2M (°C), RH2M (%), WS2M (m/s), ALLSKY_SFC_SW_DWN (MJ/m²/day), PRECTOTCORR (mm/day) |
| ET₀ units      | mm/day (computed via FAO-56 Penman-Monteith)                 |
| Rainfall units | mm/day                                                       |

### ET₀

Reference evapotranspiration computed using the **FAO-56 Penman-Monteith**
equation (Allen et al., 1998).

**ET₀ formula:**

```
ET₀ = (0.408 × Δ × Rn + γ × (900 / (T + 273)) × u₂ × VPD)
      / (Δ + γ × (1 + 0.34 × u₂))
```

Where:
- Δ = slope of saturation vapour pressure curve (kPa/°C)
- Rn = net radiation (MJ/m²/day)
- γ = psychrometric constant (kPa/°C), derived from elevation
- T = mean daily temperature (°C)
- u₂ = wind speed at 2 m height (m/s)
- VPD = vapour pressure deficit (kPa)

**Units verified:**
- Temperature: °C ✓
- Wind speed: m/s ✓
- Solar radiation: MJ/m²/day ✓
- Humidity: % (converted to vapour pressure internally) ✓
- Elevation: 249.47 m (used for psychrometric constant) ✓
- ET₀ output: mm/day ✓

### Rainfall

Daily precipitation from the reference weather dataset.

- Units: mm/day
- Time period: daily
- Source: NASA POWER PRECTOTCORR variable

---

## LAI Classification

LAI demand thresholds are derived empirically from the **33rd and 66th
percentiles** of the LAI distribution within the reference Mendeley dataset,
computed **separately for Indoor and Outdoor environments**.

**These are empirical dataset-based thresholds, not universal agronomic
thresholds.**

Indoor and Outdoor environments are kept separate because the LAI
distributions differ substantially between the two conditions. Merging them
would produce thresholds that are not representative of either environment.

**Threshold values:**

| Environment | Low → Moderate | Moderate → High |
|-------------|----------------|-----------------|
| Indoor      | 0.03198        | 0.05981         |
| Outdoor     | 0.00324        | 0.00722         |

**Interpretation:**

| Class    | Meaning                                                        |
|----------|----------------------------------------------------------------|
| LOW      | Relatively lower LAI within the reference dataset distribution |
| MODERATE | Intermediate LAI                                               |
| HIGH     | Relatively higher LAI within the reference dataset distribution|

These categories are decision-support classes. They reflect the crop's
relative canopy development within the observed dataset range.

---

## ET₀ Classification

ET₀ demand thresholds are derived empirically from the **33rd and 66th
percentiles** of the ET₀ distribution across the full reference weather
dataset (2018–2023).

**These are empirical reference-weather thresholds, not universal lettuce
water-requirement thresholds.**

**Threshold values:**

| Low → Moderate | Moderate → High |
|----------------|-----------------|
| 2.2311 mm/day  | 5.1584 mm/day   |

**Interpretation:**

| Class    | Meaning                                                              |
|----------|----------------------------------------------------------------------|
| LOW      | Relatively lower atmospheric evaporative demand on this day          |
| MODERATE | Intermediate atmospheric evaporative demand                          |
| HIGH     | Relatively higher atmospheric evaporative demand on this day         |

---

## Rainfall Adjustment

If daily rainfall meets or exceeds the rainfall threshold, the combined
demand is reduced by one level.

**Rainfall threshold:** 2.7575 mm/day

This threshold is the **75th percentile of non-zero rainfall days** in the
reference weather dataset. It is an empirical/heuristic threshold, not a
physically calibrated irrigation offset.

**Adjustment rule:**

| Combined Demand | Rainfall ≥ Threshold | Final Demand |
|-----------------|----------------------|--------------|
| HIGH            | Yes                  | MODERATE     |
| MODERATE        | Yes                  | LOW          |
| LOW             | Yes                  | LOW          |
| Any             | No                   | Unchanged    |

---

## Demand Fusion

The LAI demand and ET₀ demand are combined using a **max rule**:

```
combined_demand = max(LAI_demand_level, ET0_demand_level)
```

Where demand levels are mapped as: LOW=1, MODERATE=2, HIGH=3.

The combined demand is then adjusted for rainfall (see above).

**Rationale:** The max rule ensures that if either the crop canopy (LAI)
or the atmospheric conditions (ET₀) indicate high demand, the system
responds conservatively by recommending higher irrigation. This is a
rule-based heuristic, not an experimentally validated crop-water model.

---

## Final Output

The engine outputs one of three irrigation demand classes:

| Output   | Meaning                                                        |
|----------|----------------------------------------------------------------|
| LOW      | Lower relative irrigation demand indicated                     |
| MODERATE | Intermediate irrigation demand indicated                       |
| HIGH     | Higher relative irrigation demand indicated                    |

The output also includes a plain-language explanation of which rules
produced the final decision.

---

## Important Limitations

1. **Weather is reference environmental input.** The weather dataset is not
   claimed to be measured at the Mendeley lettuce experiment location. It
   provides representative reference conditions for demonstrating the pipeline.

2. **LAI thresholds are empirical dataset-based thresholds.** They reflect
   the distribution of LAI values in the Mendeley lettuce dataset and are not
   universal agronomic thresholds.

3. **ET₀ thresholds are empirical reference-weather thresholds.** They
   reflect the distribution of ET₀ values in the reference weather dataset
   and are not universal lettuce water-requirement thresholds.

4. **Rainfall threshold is heuristic.** The 75th percentile of non-zero
   rainfall days is used as a practical cutoff, not a physically calibrated
   irrigation offset.

5. **Final demand is rule-based.** The fusion logic (max rule + rainfall
   adjustment) is a practical heuristic, not an experimentally validated
   crop-water optimization model.

6. **No validated numerical irrigation depth is produced.** The system
   outputs LOW / MODERATE / HIGH demand classes only. A numerical
   irrigation-depth module would require a documented crop-water methodology
   and is not currently implemented.

7. **This is a decision-support prototype.** It is designed to be
   transparent and explainable, not to replace agronomic expertise or
   field-calibrated irrigation scheduling.

---

## References

- Allen, R.G., Pereira, L.S., Raes, D., Smith, M. (1998). *Crop
  evapotranspiration — Guidelines for computing crop water requirements.*
  FAO Irrigation and Drainage Paper 56. FAO, Rome.

- Mendeley lettuce RGB-LAI dataset (source of LAI ground truth and images).

- NASA POWER (https://power.larc.nasa.gov/) — source of reference weather
  data.
