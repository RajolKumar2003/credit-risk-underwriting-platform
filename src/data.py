import pandas as pd
from sklearn.model_selection import train_test_split

from src import config


def load_applications():
    return pd.read_csv(config.RAW_DIR / "application_train.csv")


def load_column_descriptions():
    path = config.RAW_DIR / "HomeCredit_columns_description.csv"
    return pd.read_csv(path, index_col=0, encoding="cp1252")


def load_bureau():
    columns = [
        "SK_ID_CURR",
        "CREDIT_ACTIVE",
        "DAYS_CREDIT",
        "CREDIT_DAY_OVERDUE",
        "AMT_CREDIT_SUM",
        "AMT_CREDIT_SUM_DEBT",
    ]
    return pd.read_csv(config.RAW_DIR / "bureau.csv", usecols=columns)


def load_previous_applications():
    columns = ["SK_ID_CURR", "NAME_CONTRACT_STATUS", "DAYS_DECISION"]
    return pd.read_csv(config.RAW_DIR / "previous_application.csv", usecols=columns)


def load_installments():
    dtypes = {
        "SK_ID_CURR": "int32",
        "DAYS_INSTALMENT": "float32",
        "DAYS_ENTRY_PAYMENT": "float32",
        "AMT_INSTALMENT": "float32",
        "AMT_PAYMENT": "float32",
    }
    return pd.read_csv(
        config.RAW_DIR / "installments_payments.csv",
        usecols=list(dtypes),
        dtype=dtypes,
    )


def assign_split(target, seed=config.RANDOM_SEED, valid_share=0.2, test_share=0.2):
    train_valid, test = train_test_split(
        target.index, test_size=test_share, stratify=target, random_state=seed
    )
    train, valid = train_test_split(
        train_valid,
        test_size=valid_share / (1 - test_share),
        stratify=target.loc[train_valid],
        random_state=seed,
    )
    split = pd.Series("train", index=target.index)
    split.loc[valid] = "valid"
    split.loc[test] = "test"
    return split


def load_modelling_table():
    return pd.read_pickle(config.PROCESSED_DIR / "modelling_table.pkl")
