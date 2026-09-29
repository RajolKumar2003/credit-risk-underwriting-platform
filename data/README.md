# Data

Source: Home Credit Default Risk (Kaggle competition). Accepting the competition
rules on Kaggle is required to download it.

The raw files are not in this repository and must not be committed or
redistributed. Place them in `data/raw/`:

- application_train.csv
- bureau.csv
- bureau_balance.csv
- previous_application.csv
- installments_payments.csv
- POS_CASH_balance.csv
- credit_card_balance.csv
- HomeCredit_columns_description.csv (Windows-1252 encoded, not UTF-8)

Used so far: application_train, bureau, previous_application, installments_payments and the
column descriptions. `credit_card_balance.csv`, `POS_CASH_balance.csv` and
`bureau_balance.csv` are not used yet. `application_test.csv` has no labels and is not used.

Open item: the Kaggle rules have not yet been read for what may be shown in a
public deployment. Until then the deployed app must use only model outputs and
aggregates, not applicant-level rows.
