import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier

from src.explain import local_attribution, reference_row


def test_attribution_points_to_driving_feature():
    rng = np.random.default_rng(0)
    frame = pd.DataFrame({"signal": rng.normal(size=4000), "noise": rng.normal(size=4000)})
    target = (frame["signal"] + rng.normal(scale=0.5, size=4000) > 1).astype(int)
    model = HistGradientBoostingClassifier(random_state=0).fit(frame, target)
    reference = reference_row(frame, list(frame.columns))
    row = pd.Series({"signal": 2.5, "noise": 0.0})
    effect = local_attribution(model, row, reference, ["signal", "noise"])
    assert effect.index[0] == "signal"
    assert effect["signal"] > 0
