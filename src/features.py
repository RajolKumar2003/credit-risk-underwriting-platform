import numpy as np

RATIO_FEATURES = [
    "AGE_YEARS",
    "CREDIT_INCOME_RATIO",
    "ANNUITY_INCOME_RATIO",
    "CREDIT_ANNUITY_RATIO",
    "EMPLOYED_AGE_SHARE",
    "INCOME_PER_FAMILY_MEMBER",
]


def add_ratio_features(df):
    df = df.copy()
    df["AGE_YEARS"] = -df["DAYS_BIRTH"] / 365.25
    df["CREDIT_INCOME_RATIO"] = df["AMT_CREDIT"] / df["AMT_INCOME_TOTAL"]
    df["ANNUITY_INCOME_RATIO"] = df["AMT_ANNUITY"] / df["AMT_INCOME_TOTAL"]
    df["CREDIT_ANNUITY_RATIO"] = df["AMT_CREDIT"] / df["AMT_ANNUITY"]
    df["EMPLOYED_AGE_SHARE"] = df["DAYS_EMPLOYED"] / df["DAYS_BIRTH"]
    df["INCOME_PER_FAMILY_MEMBER"] = df["AMT_INCOME_TOTAL"] / df["CNT_FAM_MEMBERS"]
    df[RATIO_FEATURES] = df[RATIO_FEATURES].replace([np.inf, -np.inf], np.nan)
    return df
