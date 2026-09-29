import numpy as np
import pandas as pd

ASSUMED_LGD = 0.45
ASSUMED_MARGIN = 0.08


def approval_table(y_true, pd_score, exposure, thresholds, lgd=ASSUMED_LGD, margin=ASSUMED_MARGIN):
    y_true = np.asarray(y_true)
    pd_score = np.asarray(pd_score)
    exposure = np.asarray(exposure, dtype=float)
    rows = []
    for threshold in thresholds:
        approved = pd_score <= threshold
        defaults = y_true[approved].sum()
        gain = (exposure[approved] * margin * (y_true[approved] == 0)).sum()
        loss = (exposure[approved] * lgd * (y_true[approved] == 1)).sum()
        rows.append(
            {
                "threshold": threshold,
                "approval_rate": approved.mean(),
                "default_rate_approved": defaults / max(approved.sum(), 1),
                "defaulters_declined_share": 1 - defaults / y_true.sum(),
                "net_value": gain - loss,
            }
        )
    return pd.DataFrame(rows)


def best_threshold(table):
    return table.loc[table["net_value"].idxmax()]
