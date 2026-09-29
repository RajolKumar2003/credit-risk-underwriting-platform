import sqlite3
from pathlib import Path

import joblib
import pandas as pd

from src import config
from src.risk import BAND_LABELS, assign_band, expected_loss

SQL_DIR = config.ROOT / "sql"
DB_FILE = config.PROCESSED_DIR / "portfolio.db"


def scored_applicants(table, bundle):
    scored = table[table["split"].isin(["valid", "test"])].copy()
    scored["pd"] = bundle["model"].predict_proba(scored[bundle["columns"]])[:, 1]
    frame = pd.DataFrame(
        {
            "applicant_id": scored[config.ID_COLUMN] if config.ID_COLUMN in scored else scored.index,
            "split": scored["split"],
            "target": scored[config.TARGET],
            "pd": scored["pd"],
            "band": assign_band(scored["pd"]).astype(str),
            "contract_type": scored["NAME_CONTRACT_TYPE"],
            "income_type": scored["NAME_INCOME_TYPE"],
            "age_band": pd.cut(scored["AGE_YEARS"], [20, 30, 40, 50, 60, 70], right=False).astype(str),
            "credit": scored["AMT_CREDIT"],
            "expected_loss": expected_loss(scored["pd"], scored["AMT_CREDIT"]),
            "bureau_credit_count": scored["BUREAU_CREDIT_COUNT"],
            "inst_late_share": scored["INST_LATE_SHARE"],
        }
    )
    frame["band_order"] = frame["band"].map({label: i for i, label in enumerate(BAND_LABELS)})
    return frame


def build_database(frame, path=DB_FILE):
    path = Path(path)
    if path.exists():
        path.unlink()
    with sqlite3.connect(path) as connection:
        frame.to_sql("applicants", connection, index=False)
        connection.execute("CREATE INDEX idx_split ON applicants(split)")
    return path


def run_query(name, path=DB_FILE):
    text = (SQL_DIR / name).read_text()
    with sqlite3.connect(path) as connection:
        return pd.read_sql_query(text, connection)
