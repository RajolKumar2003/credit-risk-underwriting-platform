# Interview questions and answers

*Educational project. Every number below is from the notebooks in this repository.*

## Business framing

**1. What problem does the project solve?**

It ranks loan applicants by probability of early repayment difficulty, explains why an applicant scores high, converts probabilities into expected loss (PD x LGD x EAD), and shows how approval cutoffs trade volume against loss. It simulates the analytics workflow of an underwriting team.

**2. What exactly is the target, and why does that matter?**

TARGET=1 means a late payment beyond an undisclosed number of days on at least one of the first instalments. It is early repayment difficulty, not lifetime default, so expected-loss figures are illustrations, and I say that everywhere.

**3. Why credit risk as a project domain?**

It has a natural chain from prediction to money: PD, exposure, loss and a decision cutoff. Each step needs a defensible assumption, which makes it a good test of reasoning, not only modelling.

**4. Who would use the outputs?**

Underwriters (PD, band, drivers), portfolio managers (band and loss concentration), finance (expected loss under stated assumptions). The app has a page for each.

**5. Is this a lending policy?**

No. Thresholds, LGD and margin are project-defined, the data is one historical portfolio, and the project says so in the README, app and model card.

**6. What would you change to deploy this for real?**

Time-based validation on dated data, exclude or legally review age and gender, real recovery data for LGD, monitoring for drift, and an approval process on top of the cutoff. Those are the gaps I list in the model card.

## Data and leakage

**7. Why Home Credit and not a simpler dataset?**

It has an application table plus three history tables (bureau, previous applications, instalments), which allowed a real test of whether alternate data helps.

**8. How did you check for leakage?**

I tested the history tables for records dated after the application (there were none: no positive DAYS values), excluded three columns with placeholder values and unclear timing (DAYS_FIRST_DRAWING, DAYS_LAST_DUE, DAYS_TERMINATION), and tested the social-circle columns, which added nothing and which I then dropped.

**9. What is the DAYS_EMPLOYED anomaly?**

365243 is a placeholder for people with no employment date (mostly pensioners). I turned it into missing and added a flag column, since the flag itself carries information.

**10. How did you handle missing values?**

Column by column. Some missingness is structural (OWN_CAR_AGE when there is no car), some informative (missing external score raised risk). Median imputation with missing indicators for logistic regression, native handling for boosting. Counts of history records fill with 0 when there is no record; shares and ratios stay missing.

**11. Why a random split?**

The data has no calendar dates, only relative day counts, so a time split is impossible. I state the loss of a time-based check as a limitation.

**12. How did you keep the test set clean?**

fit_and_score raises an error if asked to evaluate on test; only a separate final function touches it, called once with the model and cutoff frozen.

**13. Why did you exclude SK_ID_CURR?**

It is an identifier; using it would let a tree model memorise row order or ID structure.

**14. Did you drop outliers in income?**

No. Extreme incomes are plausible, and trees are robust. Log transform was tested only in the logistic model and made no measurable difference.

## Statistics and EDA

**15. Why report effect sizes with p-values?**

With 300,000 rows almost any difference is significant. Cramér's V and the AUC-form effect size say whether it matters.

**16. What did EDA find that a simple test would miss?**

Credit-to-income has an inverted U with default (7.25%, 8.78%, 8.92%, 8.18%, 7.25% by quintile) that a rank test rated as weak. So I never dropped features on univariate AUC alone.

**17. Why Wilson intervals?**

Default rates in small groups are near 0 or 1 where the normal approximation is poor; Wilson intervals behave correctly there.

**18. What does 'no history' mean?**

It differs by table. No bureau record: 10.12% default vs 7.73% with one. No earlier application or instalments: 6.31% vs 8.17%. Treating them the same would be wrong.

**19. How does age relate to default?**

Strongly and monotonically: about 11.5% at 20-29 down to 4.9% at 60-69. That is why using age is a policy question (D19, D31).

**20. Did you use statsmodels?**

No (D04). The tests I needed are in scipy, and I wanted every statistic to be something I can derive.

## Modelling

**21. Why start with logistic regression?**

It is the interpretable benchmark. Any complex model has to justify its extra complexity against it: here boosting beat it by 0.012 AUC with an interval excluding zero.

**22. Why gradient boosting?**

It handles missing values and non-linearity natively and was the best of three families on every feature set. I used scikit-learn's HistGradientBoosting because LightGBM was not installable in my environment.

**23. Why was the random forest dropped?**

It was the weakest at every feature set (0.749 vs 0.769 for boosting on the full set) and slower.

**24. Did class weights help?**

No. Ranking did not change (AUC 0.7458 vs 0.7459) and the average predicted probability rose from 8% to 42%, breaking expected loss.

**25. Why not SMOTE?**

It does what class weights do to probabilities, and I had shown that reweighting brought no ranking benefit. No evidence, no technique.

**26. Did you use PCA or deep learning?**

No. Features are interpretable and few carry the signal; nothing in the evidence called for them.

**27. How much did tuning help?**

At most 0.0014 AUC over defaults, below the roughly 0.004 noise, so I stopped after eight settings instead of searching until validation looked good.

**28. What is the value of alternate data?**

History features added about 0.009 AUC (interval 0.006 to 0.011) for boosting and 0.009 for logistic. Real but modest.

**29. What is the most important input?**

The three external scores: removing them costs 0.033 AUC, twice the whole gain from ratios plus history.

**30. Why are logistic coefficients unreliable here?**

AMT_CREDIT, AMT_GOODS_PRICE and AMT_ANNUITY are strongly correlated; their coefficients (+2.0, -1.05, -0.64) offset each other. The group is meaningful, the individual signs are not.

## Evaluation, calibration and thresholds

**31. Why not accuracy?**

A model that approves everyone is 92% accurate. I used ROC-AUC, PR-AUC, KS and Brier.

**32. What is PR-AUC good for here?**

With 8% positives, PR-AUC is read against the random baseline of 0.081. The model reaches 0.270, over three times that.

**33. How did you test calibration?**

Ten equal-size groups by predicted PD compare predicted and actual rates; then isotonic and Platt calibrators on half the validation set were compared on the other half. Neither helped; Platt slope was 0.994.

**34. Why is the model already calibrated?**

It is trained with log-loss on the natural default rate with no reweighting. Calibration would matter if I had used class weights.

**35. How did you choose the approval cutoff?**

I did not, in the sense of finding a true optimum. Under LGD 45% and margin 8% the best cutoff is 16%, but it moves from 6% to 30% across plausible assumptions. I present it as a function of the assumptions.

**36. How do you know differences between models are real?**

Paired bootstrap on the same resampled rows gives an interval per difference. For example boosting minus logistic was +0.0113 (0.0081 to 0.0145) on validation.

**37. Your test AUC is higher than validation. Is that suspicious?**

0.775 vs 0.7705 is about one bootstrap standard error, so it is noise. I claim validation-level performance, not better.

**38. How did you validate expected loss?**

Expected loss under PD x 45% x credit was 1,242m vs 1,258m for the same formula applied to the labels: ratio 0.99 (0.958 to 1.019). It validates the calibration of PD, not the loss amount.

## Explainability and fairness

**39. Why not SHAP?**

It could not be installed. I used permutation importance globally and occlusion per applicant, stated their weaknesses, and unit-tested occlusion on a synthetic model.

**40. What are the weaknesses of your explanations?**

They ignore interactions and correlation: correlated columns share importance and occlusion effects do not add up to the total.

**41. Explain one applicant's score.**

The highest-risk applicant had PD 76.5%: external scores 0.14 and 0.10 vs typical 0.54 and 0.57, missing external score 1, a 67% refusal share on earlier applications, and a bureau debt ratio of 0.65.

**42. Did you use age and gender?**

The tested model does; removing them costs 0.0025 AUC and narrows the women/men approval gap from 8.7 to 6.3 points, not to zero. I kept the frozen model, documented the issue, and never ask for gender in the app.

**43. Is your model fair?**

I make no fairness claim. Segment analysis shows calibration holds across major groups, but removing a column does not remove correlated information, and fairness needs a policy definition.

**44. Where does the model perform worst?**

Ranking is weaker for applicants aged 60-70 (AUC 0.728) and some small groups; incomplete-higher-education applicants are over-predicted by 1.7 points.

## SQL

**45. What did you do in SQL?**

Six query files on the scored portfolio: summary by product, default by band with window-function shares, ranked segments, loss concentration with NTILE, cutoff economics with a CTE and CROSS JOIN, and history groups.

**46. How did you know the SQL was right?**

Net value at cutoff 0.16 and for approving everyone matched the pandas results exactly (1,691.8m and 1,463.8m), and a unit test checks totals on a small database.

**47. Why SQLite?**

It ships with Python and the queries are standard SQL. DuckDB was planned but unnecessary; pandas built the features in 20 seconds.

## App and AI analyst

**48. What does the app show?**

Overview metrics, portfolio analytics by band and segment, a single-applicant assessment, model performance and calibration, explainability, an expected-loss and cutoff simulator, an AI risk analyst note, and an About page with limits.

**49. How does the assessment page handle inputs a user cannot know?**

External scores, instalment record and bureau counts are optional; other fields go in as missing. The app warns that unknown external scores raise the estimate.

**50. How does the LLM avoid hallucinating?**

It never scores. It gets a validated structured object and may only rewrite it. A regex check compares every number in the reply against the numbers in the context; failures are replaced by a template note.

**51. Why no LangChain?**

One API call with a schema does not need a framework (D06, D35).

**52. Is the app tested?**

The scoring path, explanation, SQL, risk and analyst modules have unit tests and I ran the scoring path headlessly. The Streamlit UI itself could not be run in my build environment, and I say so in the report.

## Limitations and reflection

**53. What is the weakest part of the project?**

No time dimension: one random split cannot show drift. And loss figures are assumptions.

**54. What surprised you?**

How little tuning and model choice mattered compared with the data: the whole ladder from application form to the best model is about 0.016 AUC, while three external scores account for 0.033.

**55. What mistake did you catch?**

A zero-amount-due instalment produced infinity in a ratio; I fixed it and added a test. Also a logistic coefficient story that looked meaningful but was collinearity.

**56. What would you test next?**

A top-40-feature model (102 of 142 columns have near-zero importance), a refit without age and gender on a fresh holdout, and SHAP.

**57. How would you monitor this in production?**

Track PD distribution and default rate by band monthly, population stability of the top inputs, and calibration by decile once outcomes mature.

**58. Which decision are you proudest of?**

Refusing to present one 'optimal' cutoff, and instead showing that it moves from 6% to 30% with the assumptions.
