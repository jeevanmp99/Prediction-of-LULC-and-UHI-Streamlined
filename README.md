# Spatiotemporal Dynamics and Predictive Modeling of LULC, LST, SUHI, and UTFVI: Greater Kovai Region (2020–2028)

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CRS: EPSG-32643](https://img.shields.io/badge/CRS-EPSG%3A32643-brightgreen.svg)](https://epsg.io/32643)

## Abstract
This repository provides a streamlined implementation of the predictive thermal modeling framework developed for the Greater Kovai Region (Coimbatore, Tamil Nadu), covering a spatial extent of **1,197.06 km²** at **30 m spatial resolution**.

The workflow evaluates Land Use/Land Cover (LULC) transitions between 2020 and 2024 (Sentinel-2 MSI) and simulated LULC for 2028 (CA-ANN / MOLUSCE). Historical Land Surface Temperature (LST) is derived using the **Split-Window Algorithm (SWA)** on Landsat-8/9 TIRS (Bands 10 & 11). Predictive modeling for **2028 Land Surface Temperature** is driven by an ensemble **Random Forest (RF) Regression** architecture ($R^2 = 0.774$), dynamic NDVI transitions, and spatial covariates. Further ecological vulnerability is quantified using the **Surface Urban Heat Island (SUHI)** intensity and the **Urban Thermal Field Variance Index (UTFVI)**.

> **Note on Prior Work:** This repository is a focused, refined continuation of the master's thesis work originally hosted at [jeevanmp99/Prediction-of-LULC-and-UHI](https://github.com/jeevanmp99/Prediction-of-LULC-and-UHI).

---

## Key Quantitative Findings

1. **Impervious Footprint Expansion:**
   - Built-up area expanded by **+71.10 km²** between 2020 and 2024, and is projected to expand by an additional **+28.70 km²** by 2028, yielding a net 8-year expansion of **+99.80 km² (+21.7%)**.
   - **Cropland loss accounted for over 89%** of all urban expansion transitions (76.62 km² converted from 2020–2024; 30.92 km² converted from 2024–2028).

2. **Thermal Baseline & Synoptic Shift:**
   - The scene spatial mean LST dropped from **35.85°C (2020)** to **33.98°C (2024)**, and stabilized at **33.97°C (2028)**.
   - The ~1.87°C drop between 2020 and 2024 is uniformly reflected across all land-cover classes, confirming synoptic overpass meteorological variance rather than regional cooling.

3. **SUHI Footprint Volume Over Peak Intensity:**
   - Tree Canopy-referenced SUHI ($SUHI_{Canopy}$) remained persistent at **>+5.0°C** across all periods (+5.99°C in 2020, +5.01°C in 2024, +5.17°C in 2028).
   - While class-level peak temperature remained steady, the physical footprint experiencing >5.0°C surface heat excess expanded by **99.80 km²**.
   - Area-weighted Composite Rural SUHI ($SUHI_{Rural}$) steadily widened from **+0.56°C -> +0.64°C -> +0.76°C**.

4. **Ecological Stress Escalation (UTFVI):**
   - Natural thermal comfort sinks (Class 1, None/Excellent) contracted by **-74.89 km²** between 2020 and 2028.
   - Transitional-to-severe stress zones (Classes 2 to 5) expanded by **+179.11 km² (+168%)**, driven by peri-urban canopy clearing and construction corridors.

---

## Methodological Summary

### 1. Spatial Domain & CRS
- **Region:** Greater Kovai Region (Coimbatore, TN, India)
- **Bounding Box / Extent:** Universal Transverse Mercator (UTM) Zone 43N (EPSG: 32643)
- **Grid Resolution:** 30 m x 30 m (1,316 columns x 1,308 rows; 1 pixel = 0.0009 km²)

### 2. Analytical Formulations
- **Surface Urban Heat Island Intensity (SUHI):**
  $$SUHI_{Canopy} = \overline{T}_{Built Area} - \overline{T}_{Tree Canopy}$$
  $$SUHI_{Rural} = \overline{T}_{Built Area} - \overline{T}_{Composite Rural Baseline}$$

- **Urban Thermal Field Variance Index (UTFVI):**
  $$UTFVI = \frac{T_s - T_{mean}}{T_s}$$
  *Thresholds:* Class 1 (<0.000, None), Class 2 (0.000-0.005, Weak), Class 3 (0.005-0.010, Moderate), Class 4 (0.010-0.015, Strong), Class 5 (0.015-0.020, Stronger), Class 6 (>0.020, Strongest).

---

## Data Tables

### Table 1: Multi-Temporal LULC Dynamics (2020–2028)
| Class ID | Land Cover Class | 2020 (km²) | 2024 (km²) | 2028 (km²) | Net Change 2020–2028 (Δkm²) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| 1 | Water | 9.70 | 8.59 | 8.51 | -1.19 |
| 2 | Trees | 127.88 | 148.65 | 148.20 | +20.32 |
| 4 | Flooded Veg | 0.17 | 0.07 | 0.06 | -0.11 |
| 5 | Crops | 520.47 | 422.37 | 398.89 | **-121.58** |
| 7 | Built Area | 458.88 | 529.98 | 558.68 | **+99.80** |
| 8 | Bare Ground | 0.53 | 0.39 | 0.37 | -0.16 |
| 11 | Rangeland | 79.44 | 86.99 | 82.35 | +2.91 |
| **Total** | | **1197.07** | **1197.04** | **1197.06** | — |

### Table 2: Multi-Temporal Zonal LST Dynamics (°C)

| Class ID | Class Name | Mean 2020 (°C) | Mean 2024 (°C) | Mean 2028 (°C) | ΔLST 20–24 | ΔLST 24–28 |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | Water | 28.46 | 27.79 | 27.63 | -0.67 | -0.16 |
| 2 | Trees | 30.27 | 29.38 | 29.25 | -0.89 | -0.13 |
| 4 | Flooded Veg | 27.21 | 28.34 | 30.90 | +1.13 | +2.56 |
| 5 | Crops | 37.20 | 35.38 | 35.44 | -1.82 | +0.06 |
| 7 | Built Area | 36.26 | 34.39 | 34.42 | -1.87 | +0.03 |
| 8 | Bare Ground | 36.14 | 35.20 | 35.12 | -0.94 | -0.08 |
| 11 | Rangeland | 34.61 | 33.31 | 33.02 | -1.30 | -0.29 |
| **Scene** | **Landscape Mean** | **35.85** | **33.98** | **33.97** | **-1.87** | **-0.01** |

### Table 3: Multi-Temporal UTFVI Ecological Dynamics

| Value | Category | Grade | 2020 (km²) | 2024 (km²) | 2028 (km²) | Net Change (Δkm²) |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| 1 | None (<0.000) | Excellent | 568.72 | 590.61 | 493.83 | **-74.89** |
| 2 | Weak (0.000–0.005) | Good | 27.48 | 31.30 | 53.03 | **+25.55** |
| 3 | Moderate (0.005–0.010) | Normal | 26.76 | 30.41 | 85.58 | **+58.82** |
| 4 | Strong (0.010–0.015) | Bad | 26.21 | 29.11 | 84.82 | **+58.61** |
| 5 | Stronger (0.015–0.020) | Worse | 25.90 | 27.77 | 62.03 | **+36.13** |
| 6 | Strongest (>0.020) | Worst | 521.98 | 487.85 | 417.77 | **-104.21** |

---

## Visualizations

| Figure | Description |
| :--- | :--- |
| ![Figure 1](figures/fig1_lulc_dynamics.png) | **LULC Class Dynamics (2020–2028):** Visualizes the continuous expansion of built infrastructure at the direct expense of cropland. |
| ![Figure 2](figures/fig2_zonal_lst.png) | **Zonal Mean LST Stability:** Validates consistent class thermal signatures and highlights the synoptic drop between 2020 and 2024. |
| ![Figure 3](figures/fig3_suhi_dynamics.png) | **SUHI vs. Sprawl Footprint:** Highlights the steady >5.0°C canopy excess coupled with a +21.7% growth in spatial extent. |
| ![Figure 4](figures/fig4_utfvi_dynamics.png) | **UTFVI Stress Shift:** Demonstrates the severe contraction of comfortable sinks and the +166.9 km² surge across Classes 2–5. |

---

## Cartographic Layouts
Multi-panel QGIS print layouts are located in `figures/maps/`:
- `lulc_tripanel_2020_2028.png` (Sentinel-2 & CA-ANN simulation)
- `lst_tripanel_2020_2028.png` (SWA retrieval & RF regression)
- `utfvi_tripanel_2020_2028.png` (Ecological comfort classification)

---

## Usage

### 1. Installation
```bash
git clone [https://github.com/jeevanmp99/Prediction-of-LULC-and-UHI-Streamlined.git](https://github.com/jeevanmp99/Prediction-of-LULC-and-UHI-Streamlined.git)
cd Prediction-of-LULC-and-UHI-Streamlined
pip install -r requirements.txt
```

### 2. Predict 2028 LST
```bash
python scripts/predict_lst_2028.py --data_dir ./data/raw --output_dir ./data
```

### 3. Generate Analytical Figures
```bash
python scripts/generate_figures.py
```

---

## References & Attribution
- Original Research Repository: [jeevanmp99/Prediction-of-LULC-and-UHI](https://github.com/jeevanmp99/Prediction-of-LULC-and-UHI)
- Software Tools: QGIS 3.x, Python (GeoPandas, Rasterio, Scikit-Learn, Matplotlib)
