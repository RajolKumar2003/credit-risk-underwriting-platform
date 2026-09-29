import numpy as np

from src.config import ID_COLUMN, TARGET

EMPLOYED_PLACEHOLDER = 365243


def fix_days_employed(df):
    df = df.copy()
    is_placeholder = df["DAYS_EMPLOYED"] == EMPLOYED_PLACEHOLDER
    df["DAYS_EMPLOYED_ANOMALY"] = is_placeholder.astype(int)
    df["DAYS_EMPLOYED"] = df["DAYS_EMPLOYED"].mask(is_placeholder, np.nan)
    return df


def clean_applications(df):
    return fix_days_employed(df)


def split_features_target(df):
    y = df[TARGET]
    X = df.drop(columns=[TARGET, ID_COLUMN])
    return X, y
