import numpy as np
import pandas as pd

from src import sql_runner
from src.risk import BAND_LABELS


def tiny_frame():
    rng = np.random.default_rng(1)
    n = 600
    pd_score = rng.uniform(0.01, 0.4, n)
    frame = pd.DataFrame(
        {
            "applicant_id": range(n),
            "split": "valid",
            "target": (rng.uniform(size=n) < pd_score).astype(int),
            "pd": pd_score,
            "band": "Low",
            "contract_type": "Cash loans",
            "income_type": "Working",
            "age_band": "[30, 40)",
            "credit": 1000.0,
            "expected_loss": pd_score * 450,
            "bureau_credit_count": 1,
            "inst_late_share": 0.0,
            "band_order": 0,
        }
    )
    return frame


def test_queries_run_and_totals_match(tmp_path):
    frame = tiny_frame()
    path = sql_runner.build_database(frame, tmp_path / "t.db")
    summary = sql_runner.run_query("01_portfolio_summary.sql", path)
    assert summary["applicants"].sum() == len(frame)
    cutoff = sql_runner.run_query("05_cutoff_policy.sql", path)
    everyone = cutoff[cutoff["cutoff"] == 1.0].iloc[0]
    expected = (frame["credit"] * np.where(frame["target"] == 0, 0.08, -0.45)).sum() / 1e6
    assert abs(everyone["net_value_millions"] - round(expected, 1)) < 1e-9
    deciles = sql_runner.run_query("04_loss_concentration.sql", path)
    assert abs(deciles["cumulative_pct"].iloc[-1] - 100) < 0.11
    assert set(BAND_LABELS) >= set(sql_runner.run_query("02_default_by_band.sql", path)["band"])
