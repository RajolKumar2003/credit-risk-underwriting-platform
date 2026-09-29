import numpy as np
import pandas as pd

from src.history import bureau_features, installment_features, previous_application_features


def test_bureau_counts_and_overdue_flags():
    bureau = pd.DataFrame(
        {
            "SK_ID_CURR": [1, 1, 1, 2],
            "CREDIT_ACTIVE": ["Active", "Closed", "Active", "Closed"],
            "DAYS_CREDIT": [-100, -800, -30, -400],
            "CREDIT_DAY_OVERDUE": [0, 0, 15, 0],
            "AMT_CREDIT_SUM": [1000.0, 2000.0, 1000.0, 500.0],
            "AMT_CREDIT_SUM_DEBT": [400.0, 0.0, 100.0, np.nan],
        }
    )
    features = bureau_features(bureau)
    first = features.loc[1]
    assert first["BUREAU_CREDIT_COUNT"] == 3
    assert first["BUREAU_ACTIVE_COUNT"] == 2
    assert first["BUREAU_OVERDUE_COUNT"] == 1
    assert first["BUREAU_MAX_DAYS_OVERDUE"] == 15
    assert first["BUREAU_HISTORY_DAYS"] == 800
    assert first["BUREAU_DEBT_TO_CREDIT"] == 0.125
    assert np.isnan(features.loc[2, "BUREAU_DEBT_TO_CREDIT"])


def test_previous_application_refusal_share():
    previous = pd.DataFrame(
        {
            "SK_ID_CURR": [1, 1, 1, 1],
            "NAME_CONTRACT_STATUS": ["Approved", "Refused", "Refused", "Canceled"],
            "DAYS_DECISION": [-500, -200, -50, -900],
        }
    )
    row = previous_application_features(previous).loc[1]
    assert row["PREV_APP_COUNT"] == 4
    assert row["PREV_REFUSED_SHARE"] == 0.5
    assert row["PREV_DAYS_SINCE_LAST"] == 50


def test_installments_late_underpaid_and_unpaid():
    installments = pd.DataFrame(
        {
            "SK_ID_CURR": [1, 1, 1, 1],
            "DAYS_INSTALMENT": [-300.0, -270.0, -240.0, -210.0],
            "DAYS_ENTRY_PAYMENT": [-305.0, -260.0, -240.0, np.nan],
            "AMT_INSTALMENT": [100.0, 100.0, 100.0, 100.0],
            "AMT_PAYMENT": [100.0, 60.0, 100.0, np.nan],
        }
    )
    row = installment_features(installments).loc[1]
    assert row["INST_PAID_COUNT"] == 3
    assert np.isclose(row["INST_LATE_SHARE"], 1 / 3)
    assert row["INST_MAX_DAYS_LATE"] == 10
    assert np.isclose(row["INST_UNDERPAID_SHARE"], 1 / 3)
    assert row["INST_UNPAID_COUNT"] == 1


def test_zero_amount_due_gives_missing_ratio_not_infinity():
    installments = pd.DataFrame(
        {
            "SK_ID_CURR": [7],
            "DAYS_INSTALMENT": [-100.0],
            "DAYS_ENTRY_PAYMENT": [-100.0],
            "AMT_INSTALMENT": [0.0],
            "AMT_PAYMENT": [0.0],
        }
    )
    features = installment_features(installments)
    assert np.isnan(features.loc[7, "INST_PAID_TO_DUE"])
