# Architecture (Phase 3 design)

Status: implemented through Phase 11. Boosting uses sklearn HistGradientBoosting (D05). Open problems 1 and 3 resolved in D34 and D13; problem 2 still open.
**Provisional** are confirmed or changed by evidence in the named phase.

## Data flow

```
Kaggle CSVs (data/raw, not committed)
        |
        v   src/build_dataset.py: clean, add features, aggregate history, split
Modelling table (data/processed, pickle)
        |
        v   src/train.py: split -> baseline -> candidates -> tune -> calibrate
models/ (joblib)   +   reports/ (metrics json, figures, scored aggregates)
        |
        v   inference only, no training
Streamlit app (app/)  <--  llm/risk_analyst.py (structured context in, text out)
```

Training and inference are separate: the app loads `models/` and `reports/` and never
fits anything.

## Modules

| File | Single responsibility |
|---|---|
| `src/config.py` | Paths, seed, target and ID column names, currency label |
| `src/data.py` | Load raw files, assign the train/valid/test split, read the modelling table |
| `src/preprocessing.py` | Cleaning rules found in the audit (each documented in the decision log) |
| `src/history.py` | Per-applicant aggregates from the bureau, previous-application and instalment tables |
| `src/build_dataset.py` | Builds the modelling table (cleaning, features, history, split): `python -m src.build_dataset` |
| `src/analysis.py`, `src/plots.py` | Default-rate tables, chi-square and Mann-Whitney helpers; notebook chart style |
| `src/features.py` | Ratio features and the feature-set definitions |
| `src/train.py` | Split, fit, save. Command-line entry point |
| `src/evaluate.py` | Metrics: ROC-AUC, PR-AUC, KS, Brier, threshold table |
| `src/calibration.py` | Calibration curve and the calibrator, only if validation supports it |
| `src/explainability.py` | SHAP values and the risk-driver / protective-factor lists |
| `src/risk.py` | Risk bands, risk score, expected loss = PD x LGD x EAD |
| `llm/risk_analyst.py` | Builds a validated context object, calls the LLM, checks the output |
| `app/` | Multipage Streamlit app |

## App pages

Overview, Portfolio Analytics, Customer Risk Assessment, Risk Explorer, Model
Performance, Explainability, Expected Loss, AI Risk Analyst, About. Page-level
design happens in Phase 10, once the real features and metrics exist.

Note (Phase 5): the history aggregation ran in pandas in about 20 seconds for 13.6M
instalment rows, so DuckDB (decision D03) is not needed for the feature build. SQL remains
planned for the analytics queries in Phase 9.

## Open design problems

1. **Simulator inputs (Provisional, Phase 6).** The strongest features are likely the
   anonymised external scores and bureau aggregates, which a user cannot type in. Two
   options: (a) a simulator model on human-enterable features only, reporting the
   AUC cost; (b) a few aggregate inputs such as number of previous loans and past late
   instalments. The feature-set definitions in `features.py` are kept separate so
   either can be built.
2. **Deployed data (Provisional, needs the Kaggle rules).** Until read, the app ships
   only aggregates and model outputs.
3. **No dates.** Home Credit has only relative day counts. The split will be stratified
   random, and the loss of a time-based check is stated as a limitation.

## Explicit non-goals

No Docker, microservices, MLOps platform, LangChain, deep learning, or a second
gradient-boosting library. Each would need evidence from a later phase to enter.
