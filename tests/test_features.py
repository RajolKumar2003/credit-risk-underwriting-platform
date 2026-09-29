import numpy as np
import pandas as pd

from src.features import add_ratio_features


def make_applications():
    return pd.DataFrame(
        {
            "DAYS_BIRTH": [-10957.5, -18262.5],
            "DAYS_EMPLOYED": [-1826.25, np.nan],
            "AMT_INCOME_TOTAL": [100000.0, 50000.0],
            "AMT_CREDIT": [300000.0, 100000.0],
            "AMT_ANNUITY": [15000.0, 0.0],
            "CNT_FAM_MEMBERS": [2.0, 0.0],
        }
    )


def test_ratios_have_the_expected_values():
    result = add_ratio_features(make_applications())
    first = result.iloc[0]
    assert first["AGE_YEARS"] == 30
    assert first["CREDIT_INCOME_RATIO"] == 3
    assert first["ANNUITY_INCOME_RATIO"] == 0.15
    assert first["CREDIT_ANNUITY_RATIO"] == 20
    assert np.isclose(first["EMPLOYED_AGE_SHARE"], 1 / 6)
    assert first["INCOME_PER_FAMILY_MEMBER"] == 50000


def test_division_by_zero_becomes_missing_not_infinite():
    result = add_ratio_features(make_applications())
    assert np.isnan(result.loc[1, "CREDIT_ANNUITY_RATIO"])
    assert np.isnan(result.loc[1, "INCOME_PER_FAMILY_MEMBER"])
    assert not np.isinf(result.select_dtypes("number").to_numpy()).any()


def test_missing_employment_stays_missing():
    result = add_ratio_features(make_applications())
    assert np.isnan(result.loc[1, "EMPLOYED_AGE_SHARE"])
