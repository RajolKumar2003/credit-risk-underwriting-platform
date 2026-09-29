import numpy as np

from src.policy import approval_table, best_threshold


def sample():
    return np.array([0, 0, 1, 0]), np.array([0.05, 0.1, 0.5, 0.2]), np.array([100, 100, 100, 100])


def test_net_value_counts_margin_on_good_and_loss_on_bad():
    y, p, e = sample()
    table = approval_table(y, p, e, [0.15, 1.0], lgd=0.45, margin=0.08)
    assert abs(table["net_value"][0] - 16) < 1e-9
    assert abs(table["net_value"][1] - (24 - 45)) < 1e-9


def test_shares_are_consistent():
    y, p, e = sample()
    row = approval_table(y, p, e, [0.15]).iloc[0]
    assert row["approval_rate"] == 0.5
    assert row["defaulters_declined_share"] == 1.0


def test_best_threshold_picks_highest_value():
    y, p, e = sample()
    table = approval_table(y, p, e, [0.15, 1.0])
    assert best_threshold(table)["threshold"] == 0.15
