# Methodology

*Educational project. Not a lending policy.*

Each step below points to the notebook that shows the evidence and to the decision-log entry that records the choice.

1. **Dataset choice (D01).** Home Credit Default Risk chosen for size, the multi-table structure (bureau, previous applications, instalments) and public availability.
2. **Audit (notebook 01; D02, D08-D11).** Target is early repayment difficulty. `DAYS_EMPLOYED = 365243` is a placeholder (flagged and set to missing). Missingness is studied column by column; no blanket imputation. Income outliers kept.
3. **Split (D13).** Stratified random 60/20/20; test untouched until the final model. No dates exist, so no time-based split is possible.
4. **EDA and tests (notebook 02; D14, D15).** Wilson intervals, chi-square with Cramér's V, Mann-Whitney with AUC effect size. Effect sizes are reported with every p-value. Features are not dropped on univariate AUC alone (the credit-to-income relationship is an inverted U that a rank test misses).
5. **Features (notebook 03; D16-D18).** Six ratios; 19 history features from records dated before the application. "No history" is handled by table: counts fill with 0, shares stay missing.
6. **Baseline and candidates (notebooks 04-05; D20-D25).** Logistic regression, random forest and gradient boosting on three feature sets. Class weights rejected (probabilities destroyed, no ranking gain). Differences read with paired bootstrap intervals.
7. **Tuning and calibration (notebook 06; D26-D27).** Eight-setting grid; gains below noise. No calibrator needed.
8. **Thresholds and test (notebook 07; D28-D29).** Net value under stated LGD and margin; cutoff shown as dependent on assumptions; test scored once.
9. **Errors, explanation, bands, expected loss (notebook 08; D30-D33).**
10. **SQL analytics (notebook 09).** Same portfolio questions in SQL; net-value figures cross-checked against pandas.
11. **App and AI analyst (D34-D35).** The app only loads the trained model and aggregates. The LLM only rewrites structured outputs.

## Metrics used, and why
ROC-AUC and KS for ranking; PR-AUC because defaults are 8% of cases; Brier and calibration by decile because probabilities feed expected loss. Accuracy is not used (a model that approves everyone is 92% "accurate", D12).
12. **Extra features (D36).** External-score combinations and recent-payment features tested on validation; gains of 0 and 0.002 AUC, not adopted.
