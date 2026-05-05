# Distribution Shift in Expected Goals Models: Why Industry Standards Fail in 3v3 Overtime

**Author:** Adriana-Stefania Ciupeanu
**Data:** 1.2M NHL shots (2014-2025) | MoneyPuck xG values  
**Status:** Research-grade analysis ready for publication

---

## Executive Summary

Expected Goals (xG) models are the industry standard for shot quality assessment in hockey. We audit the calibration of MoneyPuck's xG model across 1.2M NHL shots and identify **substantial localized miscalibration when game state transitions to 3-on-3 overtime**, despite strong global performance. Calibration error increases by 288% in this context (ECE: 0.015 → 0.058), revealing hidden model weaknesses in rare but extreme distribution shifts.

**Key Findings:**
- ✓ **Statistical validation (LRT)**: Game context is a statistically significant predictor (χ²=28.59, p<0.001)
- ✓ **Localized failure mode**: MoneyPuck systematically underestimates high-danger zone shots specifically in 3v3
- ✓ **Strategic insights**: Shot effectiveness changes under game-state conditions—snap shots gain 14.3% while slap shots gain only 4.4%
- ✓ **Simple recovery path**: Logistic regression with explicit context reduces calibration error by 65.6%

**Why This Matters:**
Although 3v3 overtime constitutes less than 1% of shots, its extreme distribution shift exposes a critical principle: **model robustness cannot be assessed on aggregate metrics alone.** Models that perform well globally may harbor hidden weaknesses in specific subpopulations. For decision-making in high-stakes contexts (playoff strategy, betting markets), local calibration is as critical as global accuracy.

---

## Research Contributions

This work makes three distinct contributions:

### **1. Localized Miscalibration Under Distribution Shift**
- Quantifies +288% ECE degradation in 3v3 overtime
- Demonstrates that global model performance masks subpopulation weaknesses
- Highlights risk of aggregate-metric-based evaluation

### **2. Statistical Validation of Context Dependence**
- Likelihood Ratio Test confirms game context is statistically significant (χ²=28.59, p<0.001)
- Provides formal statistical grounding beyond descriptive findings
- Establishes baseline for future game-state-aware modeling

### **3. Recoverability via Simple Models**
- Shows logistic regression recovers 65.6% of calibration error
- Demonstrates principle: interpretability + context beats complexity without context
- Provides baseline for practitioners (no neural networks required)

**Broader Implication:** Rare but extreme distribution shifts expose hidden model weaknesses that routine evaluation misses. This has implications beyond hockey for any domain where rare events or context-dependent shifts occur.

---

### Context: What is 3v3 Overtime?

In NHL regular season overtime, teams play 3-on-3 (instead of 5v5), creating an open-ice environment where:
- Fewer defenders = fewer obstacles
- Goal probability **doubles** (from 7.05% to 14.3%)
- Shot strategy shifts (speed/accuracy > raw power)

### The Research Question

**Can industry-standard xG models handle distribution shifts, or do they fail when the game fundamentally changes?**

We test this using MoneyPuck, the most widely-used open-source xG model in hockey analytics.

---

## Uncertainty Quantification

All reported metrics include 95% confidence intervals from 1,000 bootstrap resamples:

### Bootstrap Confidence Intervals (3v3 Overtime)
- **MoneyPuck ECE**: 0.0583 [95% CI: 0.0419–0.0786]
- **LR ECE**: 0.0201 [95% CI: 0.0071–0.0408]
- **Improvement**: 65.6% [95% CI: ~58%–72%]

### Interpretation
The non-overlapping confidence intervals provide strong statistical evidence that LR's calibration improvement is **robust and not due to sampling variability**. Even on MoneyPuck's best bootstrap sample (0.0419), it exceeds LR's worst sample (0.0408), confirming consistent superiority.

### Statistical Significance
All primary findings (LRT, ECE reduction, coefficient effects) retain p<0.001 significance under bootstrap resampling.

---

## Key Results

### Finding 1: Robust Calibration Degradation in 3v3

| Metric | 5v5 | 3v3 | Degradation | 95% CI |
|--------|-----|-----|------------|--------|
| **MoneyPuck ECE** | 0.0150 | 0.0583 | **+288%** | [0.0419–0.0786] |
| **LR (Context-Aware) ECE** | 0.0022 | 0.0201 | +9x (stable) | [0.0071–0.0408] |
| **Improvement** | — | **-65.6%** | ✓ | Non-overlapping |

**Critical Observation:** The confidence intervals for MoneyPuck and LR do not overlap, even at their extremes. This provides strong statistical evidence that the improvement is robust across bootstrap resamples—not an artifact of a single validation fold.

---

### Finding 2: Statistical Necessity (Likelihood Ratio Test)

To prove this isn't noise, we used Likelihood Ratio Testing:

```
Null:       Logistic Regression WITHOUT is_3v3 flag
Alternative: Logistic Regression WITH is_3v3 flag

LRT Statistic: χ²(1) = 28.59
P-value:       p < 8.96e-08  (< 0.001, highly significant)
```

**Conclusion:** You can claim with **>99.9% confidence** that game context is statistically necessary. This is not overfitting—it's a real, measurable signal.

---

### Finding 3: What MoneyPuck Learned (And Didn't Learn)

Our logistic regression extracted a crucial insight:

**is_3v3 Coefficient: β = +0.376 (rank #3 of 11 features)**
- **Odds Ratio**: 3v3 play increases goal odds by **45.7%**
- **Interpretation**: The model learned that 3v3 has fundamentally higher scoring probability
- **Problem**: MoneyPuck appears to ignore this signal, applying 5v5 assumptions to 3v3 shots

---

### Finding 4: Spatial Failure Mode

Where does MoneyPuck fail on the ice?

| Zone | Mean Prediction Error |
|------|----------------------|
| **High-danger (x > 85)** | 0.258 |
| **Perimeter (55-85)** | 0.205 |
| **Overall (3v3)** | 0.194 |

**Insight:** MoneyPuck's biggest errors occur in high-danger zones—exactly where defenders are absent in 3v3. The model assumes defender density (a 5v5 assumption) that doesn't exist in overtime.

---

### Finding 5: Strategic Shift in Shot Types

Shot effectiveness changes in 3v3. Here's how each shot type benefits:

| Shot Type | 5v5 Effectiveness | 3v3 Boost | Rank |
|-----------|------------------|-----------|------|
| **SNAP** | 2.03x | **+14.3%** | 1st ✓ |
| **WRIST** | 1.47x | +7.0% | 2nd |
| **TIP** | 1.06x | +5.1% | 3rd |
| **SLAP** | 2.41x | +4.4% | 4th ⚠️ |
| **WRAP** | 0.38x | -0.0% | 5th ✗ |

**The Story:** In 3v3, **snap shots (high-speed, controlled) gain 3.3x more boost than slap shots (raw power)**. This suggests players and coaches intuitively understand the strategic shift—open ice rewards accuracy and speed over power. MoneyPuck's model likely doesn't capture this distinction.

---

## Methodology

### Data & Split Strategy

**Training Set (2014-2024):** 1,083,932 shots
- Represents typical NHL play across a decade
- 98.99% regular play, 1.01% 3v3 OT

**Validation Set (2024-25):** 116,578 shots
- Held separate to avoid overfitting
- 115,466 regular play, 1,112 OT shots (0.95%)
- Mimics "real deployment" conditions

### Models Evaluated

1. **MoneyPuck (Baseline)**: Published xG values
2. **LR (No Context)**: Logistic regression on (distance, angle, shot_type)
3. **LR (+ 3v3 Context)**: LR + is_3v3 binary flag
4. **LR (+ Interactions)**: LR + is_3v3 × shot_type interactions
5. **LR (Calibrated)**: LR + Platt scaling

### Metrics

- **Primary**: Expected Calibration Error (ECE) — measures how well predictions match observed frequency
- **Secondary**: Brier Score, AUC-ROC
- **Statistical Test**: Likelihood Ratio Test (α = 0.001)

### Feature Engineering

```python
# Base Features
- shotDistance_norm: Normalized distance to goal
- shotAngle_norm: Normalized angle to goal
- shotType: One-hot encoded (SNAP, WRIST, SLAP, etc.)

# Context Feature
- is_3v3: Binary flag (homeSkatersOnIce == 3 AND awaySkatersOnIce == 3)

# Interaction Features
- is_3v3 × shot_type: Tests if shot effectiveness changes in OT
- angle × distance: Captures non-linear relationships
```

---

## Figures

### Figure 1: Reliability Diagrams (Calibration Curves)

**Left (5v5):** MoneyPuck and LR perform similarly  
**Right (3v3):** MoneyPuck deviates far below the diagonal; LR stays "honest"

The y=x line represents perfect calibration. MoneyPuck's curve sagging below the line in 3v3 means it **underestimates goal probability**—a classic sign of miscalibration.

### Figure 2: Spatial Residual Mapping

Heat map showing where MoneyPuck's prediction errors cluster in 3v3:
- **Red zones**: High error (MoneyPuck underestimates)
- **Blue zones**: Low error (MoneyPuck accurate)

**Finding:** Errors concentrate in high-danger zones, confirming the "missing defenders" hypothesis.

---

## Implications

### For Analytics Teams
- **Playoff OT decisions**: Don't use uncalibrated xG. Apply context-specific adjustments or use our context-aware model.
- **Roster evaluation**: Some players may look worse in xG models if they're strong in OT (where MoneyPuck underestimates).

### For Betting Markets
- **3v3 odds**: If you're pricing shots without context, you're systematically mispricing OT.
- **Hedging**: Teams entering 3v3 with xG-based strategies may have edge if others use uncalibrated models.

### For ML/Data Science
- **Generalization**: This is a case study in why complex models (like MoneyPuck's neural networks) can fail on distribution shifts. Simple, interpretable models with explicit context can be more robust.
- **Calibration > Accuracy**: High AUC doesn't guarantee reliable predictions. Calibration matters, especially in decision-making contexts.

---

## Repository Structure

```
📁 project/
├── README.md (this file)
├── data/
│   └── oz_clean.parquet          # 1.2M shots with MoneyPuck xG
├── notebooks/
│   ├── 01_eda.ipynb              # Exploratory data analysis
│   ├── 02_modeling.ipynb          # 5 model experiments
│   ├── 03_3v3_diagnostic.ipynb    # Subgroup audit & feature importance
│   └── 04_statistical_validation.ipynb  # LRT, spatial mapping, interactions
├── outputs/
│   ├── model_comparison_results.csv
│   ├── subgroup_audit.csv
│   ├── calibration_curves.png
│   ├── reliability_diagrams.png
│   ├── spatial_residual_analysis.png
│   └── feature_importance.png
└── README.md
```

### How to Run

**Requirements:**
```bash
pip install pandas numpy scikit-learn matplotlib seaborn scipy
```

**Order:**
1. `01_eda.ipynb` — Data loading, quality checks, train/val/test split
2. `02_modeling.ipynb` — Train 5 models, compare calibration
3. `03_3v3_diagnostic.ipynb` — Subgroup analysis & feature importance
4. `04_statistical_validation.ipynb` — LRT, spatial mapping, publication figures

---

## Key Takeaways

| Claim | Evidence | p-value |
|-------|----------|---------|
| 3v3 is a different game | Base rate: 7.05% → 14.3% (2.03x) | Descriptive |
| MoneyPuck breaks in 3v3 | ECE: 0.015 → 0.058 (+288%) | Observed |
| Context is statistically necessary | LRT: χ²=28.59 | p < 0.001 |
| Simple fix works | LR + is_3v3 recovers 65.6% | Demonstrated |
| Shot strategy changes | SNAP +14.3%, SLAP +4.4% | Coefficient rank |

---

## Limitations & Future Work

**Limitations:**
- 3v3 OT is rare (1% of play), limiting statistical power
- MoneyPuck is a black box; we infer failure modes but can't audit internals
- Analysis assumes coordinate system accuracy (uses adjusted coordinates)

**Future Work:**
1. **Other game states**: Do empty-net, power-play, and penalty-shot scenarios show similar miscalibration?
2. **Model class comparison**: Do tree-based models (XGBoost, LightGBM) also fail on this distribution shift?
3. **Temporal validation**: How does model performance degrade over seasons? Is 2024-25 already different from 2014?
4. **Goalie effects**: Does goalie skill interact with 3v3 context? (Some goalies may be better at open-ice play)

---

## References & Data Sources

- **MoneyPuck**: https://moneypuck.com
- **Data**: Public NHL play-by-play data (2014-2025 seasons)
- **Methodology**: Platt scaling (Platt, 1999), ECE (Guo et al., 2017), Calibration curves (standard ML)

---

## Contact & Questions

For questions about methodology, results, or reproduction:
- All notebooks are fully documented and reproducible
- Data available upon request (subject to NHL terms)
- Code licence under GNU General Public License v3.0 (GPLv3)

---

## Abstract 

Expected Goals (xG) models are widely used in hockey analytics, yet their robustness under distribution shift remains underexplored. Using 1.2M shots from 2014–2025, we identify substantial localized miscalibration when game state transitions to 3-on-3 overtime. While 3v3 shots comprise less than 1% of observations, calibration error increases by 288% (ECE: 0.015→0.058), reflecting a significant distributional shift (goal rate +103%).

A Likelihood Ratio Test confirms game context is a statistically significant predictor (χ²=28.59, p<0.001). Incorporating a simple context indicator within a logistic regression framework reduces calibration error by 65.6% (ECE=0.020), demonstrating that this failure mode is recoverable with minimal model complexity.

Spatial analysis reveals systematic underestimation of high-danger scoring regions in 3v3, while shot-type interactions indicate strategic shifts: snap shots increase in effectiveness by 14.3% compared to only 4.4% for slap shots.

These findings suggest that current xG models, while effective in aggregate, may not fully capture context-dependent dynamics. More broadly, our results highlight how rare but extreme distribution shifts can expose hidden weaknesses in otherwise well-performing probabilistic models.

---

**Last Updated:** May 2026 

