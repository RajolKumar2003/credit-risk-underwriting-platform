import numpy as np

from src.risk import assign_band, band_summary, expected_loss


def test_bands_follow_edges():
    bands = assign_band([0.01, 0.03, 0.05, 0.12, 0.30])
    assert list(bands) == ["Low", "Moderate", "Moderate", "High", "Very high"]


def test_expected_loss_is_pd_times_lgd_times_exposure():
    assert abs(expected_loss(0.1, 1000, lgd=0.5) - 50) < 1e-9


def test_band_summary_totals_match():
    pd_score = np.array([0.01, 0.02, 0.2, 0.3])
    summary = band_summary([0, 0, 1, 0], pd_score, [100, 100, 100, 100], lgd=0.5)
    assert summary["applicants"].sum() == 4
    assert abs(summary["expected_loss"].sum() - 0.5 * 100 * pd_score.sum()) < 1e-9
