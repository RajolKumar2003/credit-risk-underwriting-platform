import pandas as pd

COUNT_COLUMNS = [
    "BUREAU_CREDIT_COUNT",
    "BUREAU_ACTIVE_COUNT",
    "BUREAU_OVERDUE_COUNT",
    "PREV_APP_COUNT",
    "PREV_APPROVED_COUNT",
    "PREV_REFUSED_COUNT",
    "INST_PAID_COUNT",
    "INST_UNPAID_COUNT",
]

HISTORY_FEATURES = [
    "BUREAU_CREDIT_COUNT",
    "BUREAU_ACTIVE_COUNT",
    "BUREAU_OVERDUE_COUNT",
    "BUREAU_MAX_DAYS_OVERDUE",
    "BUREAU_DEBT_SUM",
    "BUREAU_CREDIT_SUM",
    "BUREAU_HISTORY_DAYS",
    "BUREAU_DEBT_TO_CREDIT",
    "PREV_APP_COUNT",
    "PREV_APPROVED_COUNT",
    "PREV_REFUSED_COUNT",
    "PREV_DAYS_SINCE_LAST",
    "PREV_REFUSED_SHARE",
    "INST_PAID_COUNT",
    "INST_LATE_SHARE",
    "INST_MAX_DAYS_LATE",
    "INST_UNDERPAID_SHARE",
    "INST_PAID_TO_DUE",
    "INST_UNPAID_COUNT",
]


def bureau_features(bureau):
    frame = bureau.assign(
        is_active=bureau["CREDIT_ACTIVE"] == "Active",
        is_overdue=bureau["CREDIT_DAY_OVERDUE"] > 0,
    )
    grouped = frame.groupby("SK_ID_CURR")
    features = pd.DataFrame(
        {
            "BUREAU_CREDIT_COUNT": grouped.size(),
            "BUREAU_ACTIVE_COUNT": grouped["is_active"].sum(),
            "BUREAU_OVERDUE_COUNT": grouped["is_overdue"].sum(),
            "BUREAU_MAX_DAYS_OVERDUE": grouped["CREDIT_DAY_OVERDUE"].max(),
            "BUREAU_DEBT_SUM": grouped["AMT_CREDIT_SUM_DEBT"].sum(min_count=1),
            "BUREAU_CREDIT_SUM": grouped["AMT_CREDIT_SUM"].sum(min_count=1),
            "BUREAU_HISTORY_DAYS": -grouped["DAYS_CREDIT"].min(),
        }
    )
    credit_sum = features["BUREAU_CREDIT_SUM"]
    features["BUREAU_DEBT_TO_CREDIT"] = features["BUREAU_DEBT_SUM"] / credit_sum.where(
        credit_sum > 0
    )
    return features


def previous_application_features(previous):
    frame = previous.assign(
        is_approved=previous["NAME_CONTRACT_STATUS"] == "Approved",
        is_refused=previous["NAME_CONTRACT_STATUS"] == "Refused",
    )
    grouped = frame.groupby("SK_ID_CURR")
    features = pd.DataFrame(
        {
            "PREV_APP_COUNT": grouped.size(),
            "PREV_APPROVED_COUNT": grouped["is_approved"].sum(),
            "PREV_REFUSED_COUNT": grouped["is_refused"].sum(),
            "PREV_DAYS_SINCE_LAST": -grouped["DAYS_DECISION"].max(),
        }
    )
    features["PREV_REFUSED_SHARE"] = (
        features["PREV_REFUSED_COUNT"] / features["PREV_APP_COUNT"]
    )
    return features


def installment_features(installments):
    is_paid = installments["DAYS_ENTRY_PAYMENT"].notna() & installments["AMT_PAYMENT"].notna()
    paid = installments[is_paid]
    days_late = (paid["DAYS_ENTRY_PAYMENT"] - paid["DAYS_INSTALMENT"]).clip(lower=0)
    frame = paid.assign(
        days_late=days_late,
        is_late=days_late > 0,
        is_underpaid=paid["AMT_PAYMENT"] < paid["AMT_INSTALMENT"] - 0.01,
    )
    grouped = frame.groupby("SK_ID_CURR")
    amount_due = grouped["AMT_INSTALMENT"].sum()
    features = pd.DataFrame(
        {
            "INST_PAID_COUNT": grouped.size(),
            "INST_LATE_SHARE": grouped["is_late"].mean(),
            "INST_MAX_DAYS_LATE": grouped["days_late"].max(),
            "INST_UNDERPAID_SHARE": grouped["is_underpaid"].mean(),
            "INST_PAID_TO_DUE": grouped["AMT_PAYMENT"].sum() / amount_due.where(amount_due > 0),
        }
    )
    unpaid_counts = installments[~is_paid].groupby("SK_ID_CURR").size()
    return features.join(unpaid_counts.rename("INST_UNPAID_COUNT"), how="outer")
