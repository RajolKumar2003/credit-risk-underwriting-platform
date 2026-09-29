# Final report: AI-Powered Credit Risk & Loan Underwriting Analytics Platform

*Educational project. Not a lending policy. Thresholds and financial assumptions are project-defined.*

## Question
How can customer and loan data identify credit risk, estimate the probability of default, explain why an applicant is risky, estimate financial exposure, and support underwriting decisions?

## Answer in numbers
- A gradient-boosting model ranks applicants with **ROC-AUC 0.775 on a test set opened once** (logistic benchmark 0.763; random 0.5). PR-AUC is 0.270 against 0.081 for a random ranking.
- Probabilities are **calibrated**: predicted and actual default rates agree in every decile (Platt slope 0.994), so they can feed expected loss.
- Five risk bands separate risk: actual default rate 1.7%, 4.3%, 8.0%, 13.2%, 25.5%. The top 20% of applicants by predicted risk hold half of the expected loss.
- Under illustrative assumptions (LGD 45%, margin 8%), declining applicants above a 16% default probability raises net value about 16% over approving everyone. Across plausible assumptions the best cutoff ranges from 6% to 30%, so the cutoff is a business decision.

## What the analysis found
1. Outside credit scores are the most valuable inputs: removing them costs 0.033 AUC. This has a design consequence: a user cannot type them in, so the app treats them as optional and warns.
2. History data (bureau, earlier applications, instalments) adds about 0.009 AUC beyond application data plus ratios, with a bootstrap interval excluding zero in two model families. The full climb from application data alone to the best model is 0.016 AUC.
3. Class weighting inflates the average predicted probability from 8% to about 42% without improving ranking; it was rejected for that reason.
4. Loan-size variables are highly correlated, so coefficient-style explanations mislead; the project explains predictions by permutation importance and occlusion.
5. Performance is uniform across major groups; weaker for the oldest applicants and a few small groups.

## Method and rigour
Thirty-six documented decisions (`docs/decision_log.md`), each with evidence, rejected alternatives and an interview explanation; a single-use test split enforced in code; effect sizes and intervals instead of bare p-values; SQL and pandas cross-checks; 24 unit tests.

## Limitations
No time dimension (random split); the label is early repayment difficulty, not lifetime default; loss and margin figures are assumptions; age and gender are model inputs and are flagged for review (D31); explanations are not SHAP; Kaggle terms for public deployment not checked; the Streamlit app and LLM analyst were written and unit-tested at module level but not run end to end in the build environment because Streamlit and the Anthropic SDK could not be installed there.

## What I would do next
Test a top-40-feature model (an attempt to add more features gained only 0.002 AUC, D36); exclude age and gender and re-test on a fresh holdout; add a time-based check if dates were available; replace occlusion with SHAP; connect LGD to real recovery data.
