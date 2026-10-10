# SWAP Project Input Sources

## 1. Selected Reference Scenario

The selected scenario is the winter lettuce cropping system in Southern Italy near the Metaponto area, associated with Ventrella et al. (2009), *Adaptations of irrigated cropping systems of Southern Italy as affected by climate change at field/farm scale*. The accessible primary record identifies the Southern Italy study and its SWAP context, but the chapter's numerical SWAP inputs are not available in the accessible record.

This is a documented scenario anchor, not yet a complete executable lettuce case. The Mendeley RGB-LAI dataset is an indoor/outdoor aquaponic experiment and is not the same physical experiment.

## 2. Why This Scenario Was Selected

Ventrella et al. (2009) is the requested Southern Italy source associated with a winter lettuce cropping system and SWAP's simple crop module. It is a Nova Science book chapter; no DOI or accessible full text was located. The accessible authoritative record is the Google Scholar bibliographic record.

A related open Ventrella et al. (2010) paper, DOI `10.4081/ija.2010.193`, documents Southern Italy soil-water-balance methodology and cites SWAP, van Genuchten, and Wosten parameterization methods. It does not provide verified lettuce-specific values for this scenario, so those methodology references are not substituted for missing field inputs.

The earlier Lockyer Valley study remains a secondary lead only. Its sandy-loam, shallow-root, irrigation, and Gatton-weather details are not mixed into this Southern Italy scenario.

## 3. Weather Inputs

| parameter | value/source | unit | source | status |
|---|---|---|---|---|
| Site | Metaponto area, Basilicata, Southern Italy | location | Ventrella et al. (2009) primary record | VERIFIED |
| Exact coordinates | Pending recovery from chapter or cited experimental documentation | decimal degrees | Ventrella et al. (2009) | PENDING |
| Simulation period | Pending recovery from primary source | dates | Ventrella et al. (2009) | PENDING |
| Daily precipitation | Pending acquisition | mm/day | ECMWF AgERA5 | PENDING |
| Minimum and maximum temperature | Pending acquisition | deg C | ECMWF AgERA5 | PENDING |
| Solar radiation | Pending acquisition | SWAP-compatible radiation unit | ECMWF AgERA5 | PENDING |
| Humidity or dew point | Pending acquisition | SWAP-compatible unit | ECMWF AgERA5 | PENDING |
| Wind speed | Pending acquisition | m/s | ECMWF AgERA5 | PENDING |
| Reference ET | Optional alternative input if configured | mm/day | ECMWF AgERA5 FAO56 reference ET | PENDING |

AgERA5 provides daily precipitation, temperature, solar radiation, humidity/dew point, wind speed, and reference evapotranspiration time series. The exact Metaponto point, historical period, variable names, units, and download request must be recorded when acquired. No weather values are fabricated here.

## 4. Soil Inputs

| parameter | value/source | unit | source | status |
|---|---|---|---|---|
| Soil texture | Not recovered from accessible Ventrella record | - | Ventrella et al. (2009) | MISSING |
| Soil layer boundaries | Not recovered | cm | Ventrella et al. (2009) | MISSING |
| Residual water content, theta-r | Not recovered | cm3/cm3 | Ventrella et al. (2009); Wosten methodology cited by Ventrella et al. (2010) | MISSING |
| Saturated water content, theta-s | Not recovered | cm3/cm3 | Ventrella et al. (2009) | MISSING |
| Alpha | Not recovered | 1/cm | Ventrella et al. (2009) | MISSING |
| n | Not recovered | - | Ventrella et al. (2009) | MISSING |
| L or pore-connectivity exponent | Not recovered | - | Ventrella et al. (2009); Mualem/van Genuchten methodology | MISSING |
| Ks | Not recovered as the lettuce SWAP profile | cm/day in current SWAP convention | Ventrella et al. (2009); related Ventrella hydraulic study | MISSING |
| Initial water content or pressure head | Not recovered | cm3/cm3 or cm | Ventrella et al. (2009) | MISSING |
| Groundwater level | Fixed and shallow/fluctuating cases are discussed, but selected case is unresolved | cm | Ventrella et al. (2009) | MISSING |
| Lateral drainage | Not recovered | configuration and parameters | Ventrella et al. (2009) | MISSING |

The existing baseline contains two Dutch sandy reference layers and a drainage file, but those values belong to Hupselbrook and are not transferred to Metaponto. Reported soil statistics from another study must not be treated as the final SWAP profile unless the original source states that they were used in the lettuce simulation.

No unit conversion has been performed. Original values will be preserved alongside any later converted SWAP values and the conversion formula.

## 5. Lettuce Crop Inputs

| parameter | value/source | unit | source | status |
|---|---|---|---|---|
| Crop | Winter lettuce | - | Ventrella et al. (2009) primary record | VERIFIED |
| Crop module | Ventrella source is reported as using SWAP simple crop; actual crop-file values unavailable | - | Ventrella et al. (2009) | PENDING |
| Kcb initial | 0.15 | - | FAO 56 Table 17 | VERIFIED |
| Kcb mid-season | 0.90 | - | FAO 56 Table 17 | VERIFIED |
| Kcb end-season | 0.90 | - | FAO 56 Table 17 | VERIFIED |
| Development-stage lengths | Pending local field documentation | days | Ventrella et al. (2009) and FAO 56 | PENDING |
| LAI trajectory | Pending primary field/reference source | m2/m2 | Ventrella et al. (2009) | PENDING |
| Crop height trajectory | Not recovered | cm | Ventrella et al. (2009) | MISSING |
| Rooting-depth trajectory | Not recovered | cm | Ventrella et al. (2009) | MISSING |
| Root-water-extraction stress parameters | Not recovered | SWAP units | SWAP crop documentation and lettuce source | MISSING |

The FAO coefficients are reference evapotranspiration coefficients, not a complete SWAP crop file. No daily LAI curve is fabricated. The AI model's predicted LAI and Mendeley measured LAI are excluded from this reference-crop audit.

## 6. Boundary and Initial Conditions

| parameter | value/source | unit | source | status |
|---|---|---|---|---|
| Initial soil condition | Not recovered | SWAP units | Ventrella et al. (2009) | MISSING |
| Bottom boundary type | Fixed or shallow/fluctuating water-table scenarios are discussed, but selected lettuce case is unresolved | SWAP option | Ventrella et al. (2009) | MISSING |
| Groundwater or deep-aquifer forcing | Not recovered | cm or cm/day | Ventrella et al. (2009) | MISSING |
| Drainage condition | Not recovered | SWAP drainage inputs | Ventrella et al. (2009) | MISSING |
| Surface runoff/ponding assumptions | Pending site-specific documentation | SWAP units | SWAP official manual | MISSING |

The source discussion of alternative water-table scenarios does not establish which option belongs to the selected lettuce case. No initial pressure head or groundwater value is invented.

## 7. Irrigation Inputs

SWAP supports fixed applications and scheduled irrigation. The existing baseline's fixed 24 mm event on 2002-01-05 is a Hupselbrook test value and is not evidence for Southern Italy lettuce management. The accessible Ventrella record does not expose the actual lettuce irrigation method, dates, depths, supply rate, or trigger.

| parameter | value/source | unit | source | status |
|---|---|---|---|---|
| Irrigation method | Not recovered | sprinkling, surface, or subsurface | Ventrella et al. (2009) | MISSING |
| Irrigation dates | Not recovered | dates | Ventrella et al. (2009) | MISSING |
| Irrigation depths | Not recovered | mm | Ventrella et al. (2009) | MISSING |
| Supply rate | Not recovered | mm/hour | Ventrella et al. (2009) | MISSING |
| Scheduling rule | Not recovered; SWAP supports fixed or scheduled regimes | SWAP scheduling option | Ventrella et al. (2009) and SWAP irrigation manual | MISSING |
| Water salinity/concentration | Not recovered; not needed unless salinity is simulated | SWAP concentration unit | Ventrella et al. (2009) | PENDING |

## 8. Unresolved Parameters

- Exact Metaponto field coordinates and the primary-study simulation period.
- Downloaded daily weather records for the selected point and period.
- Soil texture, layer depths, theta-r, theta-s, alpha, n, L, and Ks for the lettuce SWAP profile.
- Initial soil water profile, selected bottom boundary, groundwater forcing, and lateral drainage.
- Lettuce development-stage lengths, LAI, crop height, rooting depth, and root-water-extraction stress parameters.
- Irrigation method, dates, depths, supply rate, and scheduling rule.
- The accessible Ventrella chapter or cited experimental documentation needed to verify the original simple-crop file values.

## 9. Assumptions

- The Ventrella Southern Italy winter-lettuce study is the reference scenario, not the physical setting of the Mendeley dataset.
- AgERA5 is the intended weather source, subject to exact point and period confirmation.
- A future prescribed-development configuration remains possible, but the source is reported as using SWAP's simple crop module and no crop-file values have been assumed.
- No numerical value is invented for missing soil, weather, crop, initial-condition, boundary, or irrigation data.

## 10. Source Links

- SWAP official site: https://swap.wur.nl/
- SWAP official manual: https://swap.wur.nl/manual/index.html
- SWAP description and required-input summary: https://swap.wur.nl/description.html
- SWAP irrigation documentation: https://www.swap.wur.nl/manual/11_irrigation.html
- SWAP verification and validation: https://www.swap.wur.nl/manual/13_verification_validation.html
- SWAP FAQ: https://swap.wur.nl/faq.html
- Ventrella et al. (2009) primary record: https://scholar.google.com/scholar?q=%22Adaptations+of+irrigated+cropping+systems+of+Southern+Italy%22
- Ventrella et al. (2010), *Soil Water Balance and Irrigation Strategies in an Agricultural District of Southern Italy*: https://doi.org/10.4081/ija.2010.193
- Ventrella et al. (2005), related hydraulic-conductivity study: https://doi.org/10.1016/j.geoderma.2004.05.005
- ECMWF AgERA5 daily agrometeorological time series: https://www.ecmwf.int/en/forecasts/datasets/agrometeorological-indicators-time-series-1979-present-derived-reanalysis
- Copernicus Climate Data Store AgERA5 access: https://cds.climate.copernicus.eu/datasets/sis-agrometeorological-indicators-timeseries
- FAO 56 crop coefficients: https://www.fao.org/4/X0490E/x0490e0c.htm
- Mendeley Data landing page: https://data.mendeley.com/

## 11. Relationship to Mendeley RGB-LAI Dataset

Mendeley dataset:

```text
RGB image -> actual measured LAI -> AI model
```

Reference SWAP scenario:

```text
documented Southern Italy lettuce field conditions -> SWAP
```

The two are connected later through the LAI variable, but they are not the same physical experiment. The aquaponic indoor/outdoor dataset must not be represented as field soil or field-weather ground truth. This audit does not implement AI-LAI integration or irrigation recommendation logic.

## Current Baseline Audit Result

The existing `project_baseline` case remains a successful SWAP 4.3.0 Hupselbrook reference execution. It uses Hupsel KNMI weather, Dutch reference soil parameters, a maize/potato/grass rotation, WOFOST/simple growth modes, fixed irrigation, lateral drainage, and zero bottom flux. It produces `result.bal`, `result.blc`, `result_output.csv`, `swap.log`, `swap.ok`, and `swap.wrn`.

It is executable, but it is not yet a scientifically meaningful Southern Italy lettuce simulation.
