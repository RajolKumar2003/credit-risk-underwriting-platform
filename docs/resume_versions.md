# Resume versions

Every number is from this repository's notebooks. Do not add figures that are not here. Replace the GitHub link with the real one.

## Version 1: Data / business analyst
**Credit Risk & Loan Underwriting Analytics Platform** | Python, SQL, Streamlit
- Built an end-to-end lending analytics workflow on 307,511 Home Credit applicants (8.07% early-repayment difficulty): audited data quality, ran statistical tests with effect sizes, and engineered 25 features from four linked tables.
- Wrote six SQL analyses (CTEs, window functions, NTILE) showing that the riskiest 20% of applicants hold 50.5% of expected loss and that the Very-high band is 13% of applicants but 42% of defaulters; cross-checked policy figures against pandas to the decimal.
- Showed that the best approval cutoff moves from 6% to 30% of default probability across plausible loss and margin assumptions, and built a Streamlit dashboard where users change those assumptions.

## Version 2: Data scientist / ML
**Credit Risk PD Model with Explainability and Calibration** | scikit-learn, pandas, permutation importance, Streamlit
- Compared logistic regression, random forest and gradient boosting on three feature sets with paired-bootstrap intervals; the chosen gradient-boosting model reached test ROC-AUC 0.775 (logistic benchmark 0.763; 95% interval on the gap 0.009 to 0.015) with the test set opened once.
- Quantified the value of alternate data (bureau, previous-application, instalment history): +0.009 AUC with an interval excluding zero; showed that removing three external scores costs 0.033 AUC.
- Rejected class weighting after showing it inflated mean predicted risk from 8% to 42% with no ranking gain; verified calibration by decile (Platt slope 0.994) so the probabilities feed PD x LGD x EAD expected loss (expected/realised 0.99).
- Documented 36 decisions with evidence and rejected alternatives; segment analysis and an age/gender ablation flagged limitations openly.

## Version 3: FinTech / risk analytics
**AI-Powered Credit Risk & Underwriting Analytics Platform** | Python, SQL, Streamlit, LLM API
- Built a probability-of-default, risk-band and expected-loss platform: five risk bands with actual default rates of 1.7% to 25.5%, and portfolio expected loss within 2% of the label-implied loss under stated LGD and EAD assumptions.
- Designed an "AI Risk Analyst" that explains model outputs in plain language with a validated input schema and a number-grounding check that falls back to a template if the LLM cites any figure not in the model output.
- Framed thresholds and loss as assumptions instead of facts, and documented model limitations (no time dimension, age and gender as inputs, label is early difficulty) in a model card.
