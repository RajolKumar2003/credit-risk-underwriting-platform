import numpy as np
import pandas as pd

EXTERNAL = ["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]
V2_FEATURES = [
    "EXT_MEAN",
    "EXT_MIN",
    "EXT_PRODUCT",
    "INST_RECENT_LATE_SHARE",
    "INST_RECENT_MAX_DAYS_LATE",
    "INST_MEAN_DAYS_LATE",
    "INST_RECENT_PAID_TO_DUE",
    "BUREAU_RECENT_COUNT",
    "BUREAU_ACTIVE_SHARE",
]


def external_score_features(applications):
    scores = applications[EXTERNAL]
    return pd.DataFrame(
        {
            "EXT_MEAN": scores.mean(axis=1),
            "EXT_MIN": scores.min(axis=1),
            "EXT_PRODUCT": scores.prod(axis=1, min_count=1),
        },
        index=applications.index,
    )


def recent_installment_features(installments, window_days=365):
    paid = installments[installments["DAYS_ENTRY_PAYMENT"].notna() & installments["AMT_PAYMENT"].notna()]
    days_late = (paid["DAYS_ENTRY_PAYMENT"] - paid["DAYS_INSTALMENT"]).clip(lower=0)
    frame = paid.assign(days_late=days_late, is_late=days_late > 0)
    recent = frame[frame["DAYS_INSTALMENT"] >= -window_days]
    grouped = recent.groupby("SK_ID_CURR")
    due = grouped["AMT_INSTALMENT"].sum()
    features = pd.DataFrame(
        {
            "INST_RECENT_LATE_SHARE": grouped["is_late"].mean(),
            "INST_RECENT_MAX_DAYS_LATE": grouped["days_late"].max(),
            "INST_RECENT_PAID_TO_DUE": grouped["AMT_PAYMENT"].sum() / due.where(due > 0),
        }
    )
    features["INST_MEAN_DAYS_LATE"] = frame.groupby("SK_ID_CURR")["days_late"].mean()
    return features


def recent_bureau_features(bureau, window_days=365):
    frame = bureau.assign(is_active=bureau["CREDIT_ACTIVE"] == "Active")
    grouped = frame.groupby("SK_ID_CURR")
    features = pd.DataFrame(
        {
            "BUREAU_RECENT_COUNT": frame[frame["DAYS_CREDIT"] >= -window_days].groupby("SK_ID_CURR").size(),
            "BUREAU_ACTIVE_SHARE": grouped["is_active"].mean(),
        }
    )
    return features
