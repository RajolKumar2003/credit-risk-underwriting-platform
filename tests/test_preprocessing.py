import numpy as np
import pandas as pd

from src.preprocessing import clean_applications, split_features_target


def make_applications():
    return pd.DataFrame(
        {
            "SK_ID_CURR": [1, 2, 3],
            "TARGET": [0, 1, 0],
            "DAYS_EMPLOYED": [-1200, 365243, -30],
            "AMT_INCOME_TOTAL": [100000.0, 90000.0, 250000.0],
        }
    )


def test_placeholder_becomes_missing_and_is_flagged():
    cleaned = clean_applications(make_applications())
    assert cleaned["DAYS_EMPLOYED"].isna().tolist() == [False, True, False]
    assert cleaned["DAYS_EMPLOYED_ANOMALY"].tolist() == [0, 1, 0]


def test_real_values_are_untouched():
    cleaned = clean_applications(make_applications())
    assert cleaned.loc[0, "DAYS_EMPLOYED"] == -1200
    assert cleaned.loc[2, "DAYS_EMPLOYED"] == -30


def test_input_frame_is_not_modified():
    original = make_applications()
    clean_applications(original)
    assert original.loc[1, "DAYS_EMPLOYED"] == 365243


def test_features_exclude_id_and_target():
    X, y = split_features_target(clean_applications(make_applications()))
    assert "SK_ID_CURR" not in X.columns
    assert "TARGET" not in X.columns
    assert y.tolist() == [0, 1, 0]
    assert not np.isinf(X.select_dtypes("number").to_numpy()).any()
