import numpy as np
import pandas as pd

from src.policy import ASSUMED_LGD

BAND_EDGES = [0.03, 0.06, 0.10, 0.16]
BAND_LABELS = ["Low", "Moderate", "Elevated", "High", "Very high"]


def assign_band(pd_score):
    index = np.searchsorted(BAND_EDGES, np.asarray(pd_score), side="right")
    return pd.Categorical(np.array(BAND_LABELS)[index], categories=BAND_LABELS, ordered=True)


def expected_loss(pd_score, exposure, lgd=ASSUMED_LGD):
    return np.asarray(pd_score) * lgd * np.asarray(exposure, dtype=float)


def band_summary(y_true, pd_score, exposure, lgd=ASSUMED_LGD):
    frame = pd.DataFrame(
        {
            "band": assign_band(pd_score),
            "y": np.asarray(y_true),
            "pd": np.asarray(pd_score),
            "exposure": np.asarray(exposure, dtype=float),
        }
    )
    frame["expected_loss"] = frame["pd"] * lgd * frame["exposure"]
    frame["realised_loss"] = frame["y"] * lgd * frame["exposure"]
    grouped = frame.groupby("band", observed=True)
    return pd.DataFrame(
        {
            "applicants": grouped.size(),
            "share": grouped.size() / len(frame),
            "mean_pd": grouped["pd"].mean(),
            "actual_default_rate": grouped["y"].mean(),
            "expected_loss": grouped["expected_loss"].sum(),
            "realised_loss": grouped["realised_loss"].sum(),
        }
    )
