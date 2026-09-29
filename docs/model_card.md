# Model card: probability-of-default model

*Educational project. Not a lending policy. Thresholds and loss assumptions are project-defined.*

## Purpose
Rank Home Credit applicants by the probability of early repayment difficulty (`TARGET` = late payment beyond an undisclosed number of days on at least one of the first instalments) and support illustrative underwriting, risk-band and expected-loss analysis. It does not predict lifetime default.

## Model
scikit-learn `HistGradientBoostingClassifier` (max depth 4, learning rate 0.05, up to 500 trees with early stopping, min leaf 100, L2 1.0), no class weights, no calibrator. Inputs: 142 columns (application fields, six ratio features, 19 history features from bureau, previous-application and instalment tables), preprocessed by ordinal encoding of categories; missing values handled natively.

## Data
Home Credit Default Risk (Kaggle), 307,511 applicants, 8.07% positive. Split stratified random 60/20/20 (train 184,506, validation 61,502, test 61,503, seed 42) because the data has no calendar dates. The test split was scored once.

## Performance (test split)
| Metric | Gradient boosting | Logistic benchmark | Reference |
|---|---|---|---|
| ROC-AUC | 0.7749 (95% 0.7675 to 0.7816) | 0.7630 | 0.5 random |
| PR-AUC | 0.2700 | 0.2523 | 0.0807 random |
| KS | 0.415 | 0.395 | |
| Brier | 0.0665 | 0.0674 | 0.0742 constant rate |
| Mean predicted PD | 8.05% | 8.04% | 8.07% actual |

Calibrated in every risk decile on validation (Platt slope 0.994). Risk bands: actual default rate 1.7% / 4.3% / 8.0% / 13.2% / 25.5% (Low to Very high).

## What drives the model
External scores `EXT_SOURCE_1-3` (removing them costs 0.033 AUC), the credit-to-annuity ratio, goods price, and the share of earlier instalments paid late. History data adds about 0.009 AUC over application data plus ratios.

## Limitations
- **No time dimension.** One random split of one historical portfolio; nothing is known about performance after economic change or population drift.
- **Label.** Early repayment difficulty, not lifetime default; LGD and margin are illustrative assumptions.
- **External scores** are anonymised with unknown provenance; a lender would need equivalent inputs at decision time.
- **Age and gender** are model inputs. Removing them costs about 0.0025 AUC and narrows but does not close the approval-rate gap between women and men (D31). No fairness claim is made; a real use would exclude them or check the applicable regulation.
- **Weaker groups:** within-group AUC is lower for the oldest applicants (0.728, age 60-70) and some small groups (lower secondary education 0.697, n=757, noisy). Incomplete higher education is over-predicted by 1.7 points.
- **Explanations** use permutation importance and occlusion, not SHAP; they ignore interactions. Logistic coefficients for loan-size variables are unstable because those variables are correlated (D22).
- Data licence and public deployment rules of the Kaggle competition have not been checked; the app ships only aggregates and the trained model.

## Intended and out-of-scope use
Intended: portfolio and learning demonstration of a credit-risk analytics workflow. Out of scope: any real credit, pricing or eligibility decision.
