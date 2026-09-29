import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
INTERIM_DIR = ROOT / "data" / "interim"
PROCESSED_DIR = ROOT / "data" / "processed"
MODELS_DIR = ROOT / "models"
REPORTS_DIR = ROOT / "reports"
DB_PATH = INTERIM_DIR / "home_credit.duckdb"

RANDOM_SEED = int(os.getenv("RANDOM_SEED", "42"))
TARGET = "TARGET"
ID_COLUMN = "SK_ID_CURR"

# Home Credit does not state a currency, so the app labels amounts with this.
CURRENCY_LABEL = "currency units"
