# Decision log

One entry per major decision. Status is **Confirmed** (backed by results in this repo)
or **Provisional** (backed only by reasoning so far, with the phase that will test it).

## D01. Use Home Credit Default Risk as the only dataset

| | |
|---|---|
| Status | Confirmed (choice); licence terms Provisional |
| Evidence | 307,511 applicants, 122 columns, about 8% positive class, plus bureau, previous-application, instalment, POS-cash and credit-card tables (sizes from public write-ups, to be re-counted in Phase 4) |
| Reason | It is the only accessible candidate with behavioural history tables, so the "does history add value?" question and a real relational SQL schema are both possible without fabricating data |
| Alternative | LendingClub, Freddie Mac SFLLD, L&T vehicle-loan data, Taiwan Credit Card, Give Me Some Credit, German Credit |
| Why rejected | LendingClub: leakage-heavy and unclear download terms. Freddie Mac: terms forbid distributing derived products. L&T: no history tables. Others: too small or too few features |
| Impact | No calendar dates, no real LGD, no stated currency; all handled as stated limitations |
| Interview explanation | "I picked the dataset that could support the most business questions honestly, and I listed what it cannot support before I started." |

## D02. Define the target as early repayment difficulty, not lifetime default

| | |
|---|---|
| Status | Confirmed (Phase 4) |
| Evidence | The data owner defines `TARGET = 1` as a late payment of more than X days on at least one of the first Y instalments, and does not disclose X or Y. 24,825 of 307,511 applicants (8.07%) are positive |
| Reason | Calling it lifetime default would overstate what PD means here |
| Alternative | Describe it simply as "default" |
| Why rejected | An interviewer who knows the dataset would catch it |
| Impact | Every PD, expected-loss and threshold statement uses the precise wording |
| Interview explanation | "The label is a proxy for default, so I say so and treat expected loss as illustrative." |

## D03. DuckDB as the SQL engine

| | |
|---|---|
| Status | Superseded for the feature build (Phase 5): pandas aggregated all 13.6M instalment rows in about 20 seconds using 7 GB of memory, so DuckDB is not needed there. Still an option for the Phase 9 SQL analytics, where the engine will be chosen again on reproducibility grounds |
| Evidence | The largest history tables have tens of millions of rows; the raw files total a few GB |
| Reason | It runs in-process with no server, reads CSV and parquet directly, and uses standard SQL, so the project stays reproducible with one `pip install` |
| Alternative | SQLite; PostgreSQL |
| Why rejected | SQLite is row-oriented and likely slow for these aggregations (to be measured). PostgreSQL needs a server, which hurts reproducibility |
| Impact | The deployed app does not need a database; it reads pre-computed files |
| Interview explanation | "I chose the engine for the data size and for reproducibility, and I measured it rather than assuming." |

## D04. No statsmodels

| | |
|---|---|
| Status | Confirmed for now |
| Evidence | Planned tests are proportion tests, chi-square, and non-parametric comparisons with effect sizes |
| Reason | SciPy covers these, including confidence intervals for proportions |
| Alternative | statsmodels |
| Why rejected | An extra dependency with no method it uniquely provides for this plan |
| Impact | Smaller install; revisit only if a Phase 5 test needs it |
| Interview explanation | "I avoid a dependency unless a method needs it." |

## D05. Candidate models: logistic regression, random forest, gradient boosting

| | |
|---|---|
| Status | Provisional (final choice by Phase 6 and 7 results and usefulness) |
| Evidence | None yet; this is the shortlist, not the result |
| Reason | One interpretable baseline, one bagged-tree model, one gradient-boosted model cover the useful range on tabular data with missing values |
| Alternative | XGBoost as well; neural networks |
| Why rejected | A second booster adds cost without adding a different idea; neural networks lack a justification on tabular data of this kind |
| Impact | Updated in Phase 6: sklearn `HistGradientBoostingClassifier` is used instead of LightGBM (not installable in the build environment, and the same algorithm family). `lightgbm` removed from requirements. The random forest was tested and dropped (D25) |
| Interview explanation | "Three models, each for a reason, and I chose on results and interpretability, not on one metric." |

## D06. No LangChain; a direct API call with a validated context object

| | |
|---|---|
| Status | Provisional (Phase 11) |
| Evidence | The task is one call: structured model outputs in, a short explanation out |
| Reason | A single call needs no orchestration framework, and a Pydantic object makes the inputs auditable |
| Alternative | LangChain |
| Why rejected | It would add a dependency and indirection with nothing to orchestrate |
| Impact | The LLM is only handed numbers the model produced, and its reply is checked against them |
| Interview explanation | "The LLM explains numbers; it never produces them." |

## D07. Currency shown as "currency units"

| | |
|---|---|
| Status | Confirmed |
| Evidence | Home Credit documents no currency |
| Reason | Showing ₹ would invent a fact |
| Alternative | Assume rupees, or convert with an assumed rate |
| Why rejected | Unsupported by the data |
| Impact | One constant, `CURRENCY_LABEL`, controls all amount labels |
| Interview explanation | "The data does not say, so I do not claim." |

## D08. Exclude the applicant ID from features

| | |
|---|---|
| Status | Confirmed (notebook 01) |
| Evidence | One row per `SK_ID_CURR`, no duplicates; Spearman correlation with `TARGET` is -0.0021 |
| Reason | It identifies a record and has no meaning for a new applicant; the correlation check shows row order carries no hidden signal |
| Alternative | Keep it as a feature |
| Why rejected | It could only help by exploiting how the file was ordered, which would not exist at prediction time |
| Impact | Used only as a join key for the history tables |
| Interview explanation | "I checked that the ID had no relationship with the outcome, then excluded it because a new applicant would have no comparable ID." |

## D09. Treat `DAYS_EMPLOYED = 365243` as missing and add a flag

| | |
|---|---|
| Status | Confirmed (notebook 01) |
| Evidence | 55,374 rows (18.01%) share the value, about 1,000 years. 55,352 are pensioners and 22 unemployed; the same rows have `ORGANIZATION_TYPE = XNA`. Their default rate is 5.40% versus 8.66% elsewhere |
| Reason | The value is a code for "not applicable", not a measurement. As a number it would distort any model that uses the size of the value, while the group itself has a distinct risk level worth keeping |
| Alternative | Leave as is; drop the rows; replace with the median |
| Why rejected | Leaving it puts a fake number in the feature. Dropping removes 18% of applicants and the pensioner group. Median-filling invents an employment length for people who have none |
| Impact | `DAYS_EMPLOYED` is missing for those rows and `DAYS_EMPLOYED_ANOMALY` = 1 |
| Interview explanation | "The summary statistics looked wrong, so I investigated. It was a placeholder for pensioners. I kept the information as a flag instead of a fake number." |

## D10. No blanket imputation; missingness is treated case by case

| | |
|---|---|
| Status | Provisional (tested in Phases 5 and 6) |
| Evidence | 67 of 122 columns have missing values; 41 are missing in over half the rows. `OWN_CAR_AGE` is missing exactly when there is no car; `OCCUPATION_TYPE` is missing for every pensioner. Missing `EXT_SOURCE_1` goes with 8.52% default versus 7.50%, and missing `AMT_REQ_CREDIT_BUREAU_YEAR` with 10.34% versus 7.72% |
| Reason | Many gaps are structural or informative, and a median fill would erase that |
| Alternative | Fill all numeric columns with the median |
| Why rejected | It hides the pattern above and treats "no car" as an average-aged car |
| Impact | Tree models use missing values directly. For logistic regression, median fill plus missing-indicators is tried on informative columns, fitted on training data only, and compared |
| Interview explanation | "Before choosing an imputation method I asked why the values were missing. Several were missing for a reason that itself predicts risk." |

## D11. Keep income outliers; log transform only where a linear model needs it

| | |
|---|---|
| Status | Provisional (before/after comparison in Phase 5) |
| Evidence | Median income 147,150, maximum 117,000,000 (about 795 times the median). Skewness is 391.6 raw and 0.17 after log. No income is zero or negative. 278 applicants are above the 99.9th percentile of 900,000 |
| Reason | The values are extreme but not impossible, and the skew is large enough to matter for a linear model. Tree models use only the order of values, so the transform does not affect them |
| Alternative | Remove outliers; cap at a percentile; transform everything |
| Why rejected | Removal deletes real applicants and makes the model blind to that region. Capping and transforming everything add steps with no measured benefit yet |
| Impact | All rows kept; log applied inside the logistic pipeline only, and its effect measured |
| Interview explanation | "I measured the skew before deciding, kept every row, and applied the transform only where the model type is sensitive to it." |

## D12. Do not use accuracy; leakage review and open item

| | |
|---|---|
| Status | Confirmed for accuracy; the social-circle check is Provisional (Phase 5) |
| Evidence | 91.9% of applicants are negative, so predicting "no difficulty" for everyone scores about 92%. All application columns are application-time by the owner's descriptions; the timing of `DEF_*_CNT_SOCIAL_CIRCLE` is not stated |
| Reason | Accuracy cannot separate a useful model from a useless one at this base rate |
| Alternative | Accuracy as the headline metric |
| Why rejected | See above |
| Impact | Ranking (ROC-AUC, PR-AUC, KS) and probability (Brier, calibration) metrics are used; the social-circle columns are tested by removal in Phase 5 |
| Interview explanation | "A model that never predicts a problem would look 92% accurate, so I judged it on ranking and on probability quality." |

## D13. Stratified random 60/20/20 split, fixed seed, test set locked

| | |
|---|---|
| Status | Confirmed (Phase 5) |
| Evidence | The data has no calendar dates (only days relative to each application), one row per applicant, and 8.07% positives. The split gives train 184,506, validation 61,502 and test 61,503, each with a 8.07% default rate |
| Reason | With no dates a time-based split is impossible, and one row per applicant means no applicant appears twice. Stratification keeps the rare class equally represented; validation is large enough (about 5,000 defaults) for model comparison and tuning |
| Alternative | Time-based split; k-fold cross-validation |
| Why rejected | Time-based: no dates exist. Cross-validation: more cost with no benefit at this sample size |
| Impact | All EDA, tests and feature checks use the training split only. The test split is opened once, for the final model. The lack of a temporal check is a stated limitation |
| Interview explanation | "There were no dates, so I could not split by time. I used a stratified holdout with a fixed seed and did all exploration on the training part only, so the test set stayed clean." |

## D14. Report effect sizes with every significance test

| | |
|---|---|
| Status | Confirmed |
| Evidence | With 184,506 training rows, ten tests gave p-values from 1e-15 to below 1e-250, yet Cramér's V was only 0.03 to 0.06 for the categorical variables |
| Reason | At this sample size almost any difference is "significant"; only the effect size says whether it matters |
| Alternative | Report p-values alone |
| Why rejected | It would suggest importance where the effect is small |
| Impact | Every test reports Cramér's V or the AUC form of Mann-Whitney. A Bonferroni check (threshold 0.005 across ten tests) changes no conclusion |
| Interview explanation | "The p-values were tiny for everything, so I judged the differences by effect size." |

## D15. Never drop a feature on a single-variable rank statistic alone

| | |
|---|---|
| Status | Confirmed |
| Evidence | `CREDIT_INCOME_RATIO` has Mann-Whitney AUC 0.497 (p = 0.28), yet its default rate by quintile is 7.25%, 8.78%, 8.92%, 8.18%, 7.25%: an inverted U. Rare features such as a currently overdue bureau credit have power near 0.506 but default at 15.48% against 7.99% |
| Reason | A rank statistic detects consistent direction and common events; it misses hump-shaped and rare-event relationships |
| Alternative | Screen features by univariate AUC |
| Why rejected | It would have discarded two useful kinds of feature |
| Impact | Feature decisions wait for model-level comparison in Phase 6; logistic regression will test binning or splines for the debt ratios |
| Interview explanation | "I looked at the quintile chart and not just the test, and found a pattern the test could not see." |

## D16. History features built per applicant, no-record handled by feature type

| | |
|---|---|
| Status | Confirmed (construction); logistic indicator Provisional (Phase 6) |
| Evidence | Coverage is 85.7% (bureau), 94.6% (earlier applications), 94.8% (instalments). No bureau record: 10.12% default against 7.73%. No earlier application: 6.31% against 8.17% |
| Reason | "No record" is different from "clean record", and the direction differs by table |
| Alternative | Fill every gap with 0; drop applicants without history |
| Why rejected | Filling with 0 would call a missing share a perfect one; dropping applicants removes up to 14% of the data and the model would not work for new customers |
| Impact | Counts are 0 without records; shares and ratios stay missing. Zero-amount instalments would have produced infinite ratios; they are set to missing (found by a check, fixed, tested) |
| Interview explanation | "I checked what a missing history means before choosing how to encode it, and it meant opposite things in different tables." |

## D17. History features use only pre-application records; placeholder columns excluded

| | |
|---|---|
| Status | Confirmed |
| Evidence | Checked on the raw tables: zero rows with a positive day value in `DAYS_CREDIT`, `DAYS_DECISION`, `DAYS_INSTALMENT` and `DAYS_ENTRY_PAYMENT`. `DAYS_FIRST_DRAWING`, `DAYS_LAST_DUE` and `DAYS_TERMINATION` hold 365,243 placeholders on 934,444, 211,221 and 225,913 rows |
| Reason | Only information available at the decision may be used. Termination and last-due dates could also describe events after the decision |
| Alternative | Load every column and aggregate |
| Why rejected | It would bring in placeholders and possible post-decision information |
| Impact | Only the columns listed in `src/data.py` are read; rows for applicants outside the labelled file are dropped |
| Interview explanation | "I tested for future-dated records instead of assuming there were none, and excluded columns whose timing I could not defend." |

## D18. Ratio features stay candidates until the model-level comparison

| | |
|---|---|
| Status | Provisional (Phase 6) |
| Evidence | `AGE_YEARS` power 0.584 equals `DAYS_BIRTH` (a rescale). `EMPLOYED_AGE_SHARE` 0.569 is below `DAYS_EMPLOYED` 0.582. `INCOME_PER_FAMILY_MEMBER` 0.517 is no better than raw income at 0.521. `BUREAU_DEBT_TO_CREDIT` 0.596 is the strongest single feature |
| Reason | A derived feature earns a place only if it helps the model, and one-variable evidence cannot show that |
| Alternative | Keep all; or drop those without single-variable gain now |
| Why rejected | Keeping all is unjustified; dropping now repeats the mistake in D15 |
| Impact | Phase 6 compares three sets on the validation split: application only, plus ratios, plus history. That difference answers the alternate-data question |
| Interview explanation | "I treated engineered features as hypotheses and tested them against the raw columns they came from." |

## D19. Sensitive attributes: describe now, decide use later

| | |
|---|---|
| Status | Provisional (Phases 6 and 8) |
| Evidence | Age has a strong monotonic relationship with default (11.54% at 20-29 to 4.93% at 60-69); gender is in the data; education and income type also correlate with age and with each other |
| Reason | Using age or gender in a credit model is a policy and fairness question, not only a statistical one, and the tables cannot separate their effects from correlated variables |
| Alternative | Include everything by default; exclude by default |
| Why rejected | Both skip the question |
| Impact | The model will be compared with and without them; segment analysis reports performance by age and gender group without fairness claims |
| Interview explanation | "I noted that age predicts default strongly, and I treated whether to use it as a decision to make and justify, not as a default." |

## D20. No class weights

| | |
|---|---|
| Status | Confirmed (Phase 6) |
| Evidence | Logistic, application columns, validation: ROC-AUC 0.7459 unweighted vs 0.7458 balanced; mean predicted probability 0.081 vs 0.421 (true 0.0807); Brier 0.0687 vs 0.2039. Boosting on the full set: AUC 0.7690 vs 0.7682, mean prediction 0.383, Brier 0.0675 vs 0.1789 |
| Reason | Ranking did not improve, and probabilities became unusable for expected loss |
| Alternative | Balanced class weights; SMOTE |
| Why rejected | Weights shift predicted probabilities to about 40-50% for an 8% event; resampling has the same effect and no ranking evidence |
| Impact | Models train on natural rates. The decision threshold is chosen in Phase 7 from costs |
| Interview explanation | "I tested class weights and showed they gave no ranking gain while inflating the average predicted probability from 8% to 42%, which breaks expected-loss calculations." |

## D21. Log amounts yes, splines no, in the logistic baseline

| | |
|---|---|
| Status | Confirmed (Phase 6) |
| Evidence | Log amounts: AUC 0.7467 vs 0.7459 (noise is about 0.004). Splines on credit-income and annuity-income ratios: 0.7484 vs 0.7483 |
| Reason | The inverted U from notebook 02 exists in bins but does not change ranking once other variables are in the model |
| Alternative | Splines on all ratios; dropping the ratios |
| Why rejected | No measurable gain, and harder to explain |
| Impact | Log amounts kept (harmless, addresses skew); splines not used. Tree models handle non-linearity |
| Interview explanation | "The rank test missed the inverted U, so I tested it directly with splines. It did not move the model, so I kept the simpler form." |

## D22. Coefficients are read in groups, not one by one

| | |
|---|---|
| Status | Confirmed (Phase 6) |
| Evidence | In the logistic model AMT_CREDIT has +2.01, AMT_GOODS_PRICE -1.05, AMT_ANNUITY -0.64 and CREDIT_ANNUITY_RATIO -0.52 |
| Reason | Credit, goods price and annuity are strongly correlated, so their coefficients offset each other |
| Alternative | Report coefficients as risk drivers |
| Why rejected | Would tell a false story that bigger loans are 2.0 times riskier |
| Impact | Explanations in the app use per-prediction attributions (Phase 8), and the loan-size cluster is discussed as a group |
| Interview explanation | "I noticed the coefficient signs flipped across correlated loan-size variables and did not present them as individual effects." |

## D23. Alternate data (history) helps modestly but reliably

| | |
|---|---|
| Status | Confirmed (Phase 6) |
| Evidence | Boosting AUC 0.7528 (application), 0.7601 (+ratios), 0.7690 (+history). Paired bootstrap: ratios +0.0072 (0.0054 to 0.0093), history +0.0089 (0.0062 to 0.0114); logistic history +0.0094 (0.0073 to 0.0118) |
| Reason | Gains exclude zero in both model families but are small in size |
| Alternative | Skip history features; use history only |
| Why rejected | The gains are real, so skipping loses ranking power |
| Impact | History features stay. Full ladder gain is about 0.016 AUC |
| Interview explanation | "Bureau, previous-application and instalment data added about one point of AUC in both models, with bootstrap intervals that exclude zero." |

## D24. External scores are essential; social-circle columns are dropped

| | |
|---|---|
| Status | Confirmed (Phase 6) |
| Evidence | Boosting without EXT_SOURCE_1-3: AUC 0.7362 vs 0.7690 (PR-AUC 0.2076 vs 0.2488). Without social-circle columns: 0.7691 |
| Reason | External scores are the largest single source of signal and cannot be typed by an app user. Social-circle columns add nothing measurable and their timing is unclear (D12) |
| Alternative | Keep social circle for completeness |
| Why rejected | No benefit, unresolved leakage doubt |
| Impact | EXT scores kept; SOCIAL_CIRCLE removed from the final feature list. The app simulator must state which inputs a user can and cannot supply (decision still open) |
| Interview explanation | "I removed the external scores as a test: performance fell by 0.033 AUC. I dropped the social-circle columns because they added nothing and I could not defend their timing." |

## D25. Model choice: gradient boosting; random forest dropped; logistic kept as benchmark

| | |
|---|---|
| Status | Confirmed (Phase 7): test AUC 0.7749 vs logistic 0.7630 |
| Evidence | Validation AUC on +history: boosting 0.7690, logistic 0.7577, forest 0.7490. Boosting minus logistic +0.0113 (0.0081 to 0.0145). Forest is lowest at every feature set |
| Reason | Best ranking with mean prediction near the true rate; the forest is worse and costs more |
| Alternative | Logistic only; forest |
| Why rejected | Logistic is 0.011 behind; forest is worse than both |
| Impact | Phase 7 tunes boosting lightly, checks calibration shape, and opens the test split once |
| Interview explanation | "I chose boosting because it beat the logistic baseline by about one AUC point with an interval that excludes zero, and kept the logistic model as the interpretable comparison." |

## D26. Light tuning only: depth 4, learning rate 0.05

| | |
|---|---|
| Status | Confirmed (Phase 7) |
| Evidence | Eight settings, validation AUC 0.7664 to 0.7705; defaults 0.7691; six within 0.0005 of defaults. Chosen setting used all 500 trees (cap reached) |
| Reason | Best result, simplest tree shape; the gain is inside noise so the choice is low-risk |
| Alternative | Larger random or Bayesian search |
| Why rejected | More search would overfit the validation split for gains below noise |
| Impact | models use max_depth=4, learning_rate=0.05 |
| Interview explanation | "I ran a small grid, saw that the effect was below noise, and stopped instead of searching until validation looked good." |

## D27. No probability calibrator

| | |
|---|---|
| Status | Confirmed (Phase 7) |
| Evidence | Decile table: predicted 1.11% vs actual 1.09% (lowest) to 29.1% vs 28.1% (highest). Held-out half: Brier raw 0.06760, isotonic 0.06756, Platt 0.06759. Platt slope 0.994, intercept -0.018 |
| Reason | The model is already calibrated (natural rate, log-loss training, no class weights) |
| Alternative | Isotonic or Platt calibration |
| Why rejected | No improvement, extra component |
| Impact | Raw model output is the PD used for expected loss (Phase 8) |
| Interview explanation | "I checked calibration by decile and with two calibrators; neither helped, so I did not add one." |

## D28. Approval threshold is an assumption-dependent business choice

| | |
|---|---|
| Status | Confirmed (Phase 7) as illustrative |
| Evidence | Under LGD 45%, margin 8%: best cutoff 0.16 (validation), net value 1,692m vs 1,464m approving all. Across LGD 30-60% and margin 4-12%, best cutoff ranges 0.06 to 0.30. Near the top, 0.12-0.20 are within 1.3% in value |
| Reason | Cost and margin are project-defined numbers, not from the dataset |
| Alternative | Report a single 'optimal' threshold; maximise F1 |
| Why rejected | A single optimum hides the assumption dependence; F1 has no financial meaning here |
| Impact | Cutoff 0.16 stored with the model as illustrative; the app must expose LGD and margin as inputs |
| Interview explanation | "The optimal cutoff moved from 6% to 30% across plausible loss assumptions, so I presented the cutoff as a function of the assumptions and never as a fact about the model." |

## D29. Final test result, opened once

| | |
|---|---|
| Status | Confirmed (Phase 7) |
| Evidence | Test: boosting AUC 0.7749 (0.7675 to 0.7816), PR-AUC 0.2700, KS 0.415, Brier 0.0665; logistic 0.7630; gap 0.0121 (0.0091 to 0.0150); mean predicted 8.05% vs 8.07% actual |
| Reason | One evaluation with everything frozen beforehand |
| Alternative | Re-tune after looking at the test |
| Why rejected | Would make the test a second validation set |
| Impact | Reported as the final performance. Test is not used again for any choice |
| Interview explanation | "I froze the model and the cutoff before opening the test split and reported the number I got, including that it was slightly higher than validation by an amount within noise." |

## D30. Permutation importance and occlusion instead of SHAP

| | |
|---|---|
| Status | Confirmed (Phase 8); replaceable |
| Evidence | SHAP is not installable in the build environment. Top permutation importances: EXT_SOURCE_2 0.037, EXT_SOURCE_3 0.032, EXT_SOURCE_1 0.016 AUC drop; 102 of 142 columns at or below 0.0002 |
| Reason | Permutation importance measures what the model actually uses for ranking; occlusion gives a per-applicant answer in the same units the model outputs |
| Alternative | Wait for SHAP; hand-code Shapley values |
| Why rejected | SHAP was unavailable and a hand-coded version would be slower and harder to trust |
| Impact | Explanations are labelled 'occlusion, not SHAP' everywhere; they ignore interactions and correlation. SHAP can be dropped in later without touching the rest |
| Interview explanation | "I could not install SHAP, so I used two simpler methods, stated their weaknesses, and tested that the local method points to the feature that drives a synthetic model." |

## D31. Age and gender stay in the evaluated model; flagged for review

| | |
|---|---|
| Status | Provisional (needs a policy decision outside this project) |
| Evidence | Refit without CODE_GENDER, DAYS_BIRTH, AGE_YEARS: validation AUC 0.7680 vs 0.7705. Approval gap women vs men at cutoff 0.16 narrows from 8.7 to 6.3 points but remains; default rates differ (7.0% vs 10.1%). CODE_GENDER is 7th in permutation importance |
| Reason | The cost of exclusion is tiny, but the model tested on the test split included them, and reopening the test to swap models would spoil it |
| Alternative | Exclude both now and re-test; include silently |
| Why rejected | Re-testing breaks the single-use rule; silent inclusion hides a policy issue |
| Impact | Documented as a limitation in the model card. The app never asks for gender. A real deployment should exclude them or check regulation. Removing a column does not remove correlated information, so no fairness claim is made |
| Interview explanation | "I measured what removing age and gender costs, found it small, and kept the tested model but documented it as a limitation instead of claiming the model is fair." |

## D32. Five risk bands with edges at 3%, 6%, 10%, 16%

| | |
|---|---|
| Status | Confirmed (Phase 8) |
| Evidence | Actual default rate by band: Low 1.7%, Moderate 4.3%, Elevated 8.0%, High 13.2%, Very high 25.5%; two top bands hold 25% of applicants and 46% of expected loss |
| Reason | Edges are ordered by predicted PD; the top edge is the approval cutoff (D28) |
| Alternative | Equal-size quintiles; a score scaled to 300-850 |
| Why rejected | Quintiles hide the tail; a scaled score adds an invented scale that means nothing without a calibration to a lender's own scorecard |
| Impact | Bands are used in the app and SQL. Edges are project-defined |
| Interview explanation | "I checked that default rates rise at every band and that predicted matches actual within each band." |

## D33. Expected loss is validated on calibration, not on amount

| | |
|---|---|
| Status | Confirmed (Phase 8) |
| Evidence | Expected 1,242m vs realised 1,258m under the same LGD 45% and EAD = credit: ratio 0.99 (0.958 to 1.019) |
| Reason | PD is well calibrated in aggregate; the loss amount depends on assumptions |
| Alternative | Claim the loss figure as accurate |
| Why rejected | LGD and EAD are assumptions and the label is only early difficulty |
| Impact | App exposes LGD as an input and labels the result illustrative |
| Interview explanation | "Expected loss matched the loss implied by the labels within 2%, which validates the probabilities, not the loss amount." |

## D34. Streamlit simulator: optional outside inputs, no gender, missing passed as missing

| | |
|---|---|
| Status | Confirmed (Phase 10); resolves the architecture open problem 1 |
| Evidence | Removing external scores costs 0.033 AUC; a missing external score raises the estimate, which the app warns about |
| Reason | Users cannot type anonymised outside scores; the model treats missing values natively |
| Alternative | Only human-enterable fields (large AUC cost); ask for all 142 fields |
| Why rejected | The first ignores the strongest signal; the second is unusable |
| Impact | Loan, income, employment fields required; external scores, instalment record and bureau counts optional; other fields left missing |
| Interview explanation | "I designed the simulator around what a person could actually type and told the user what that costs." |

## D35. AI Risk Analyst: direct API call, validated context, grounding check, template fallback

| | |
|---|---|
| Status | Confirmed (Phase 11) |
| Evidence | Tests: a grounded reply passes; a reply with an invented income figure is replaced by the template; an out-of-range PD is rejected |
| Reason | The LLM only rewrites structured model outputs; it does not decide anything |
| Alternative | LangChain or agent frameworks (D06); free-form prompting |
| Why rejected | A framework adds nothing for one call; free-form output can invent numbers |
| Impact | llm/risk_analyst.py: pydantic RiskContext, system prompt forbidding invented figures and mention of age or gender, regex check that every number in the reply is in the context, else the template note |
| Interview explanation | "The model never scores; the LLM only explains numbers the model produced, and I check every number in its reply." |

## D36. Extra features tested on validation and not adopted

| | |
|---|---|
| Status | Confirmed (post-Phase 13 experiment) |
| Evidence | Same boosting settings, validation ROC-AUC: current 0.7705; plus EXT_MEAN/MIN/PRODUCT 0.7703 (gap -0.0002, interval -0.0014 to 0.0012); plus recent-history features (last-12-month late share, max lateness, mean lateness, paid-to-due, recent bureau count, active share) 0.7723 (gap +0.0018, interval 0.0006 to 0.0033); all together 0.7721 (interval -0.0000 to 0.0031) |
| Reason | The recent-history gain is statistically detectable but tiny; combining external scores adds nothing because trees already learn the combinations |
| Alternative | Adopt the recent-history features |
| Why rejected | Adoption would mean a second look at the test split and re-running notebooks 07-08 for 0.002 AUC |
| Impact | Model, test result and all reported numbers are unchanged. `src/features_v2.py` stays as a documented, tested experiment |
| Interview explanation | "I tried the obvious next features to push AUC up; combining the external scores added nothing and recent-payment features added 0.002, so I concluded the data, not the feature list, sets the ceiling, and I did not reopen the test set for that." |
