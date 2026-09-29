import numpy as np
import pandas as pd

from src.features_v2 import external_score_features, recent_installment_features


def test_external_features_use_available_scores_only():
    frame = pd.DataFrame({"EXT_SOURCE_1": [np.nan, 0.5], "EXT_SOURCE_2": [0.4, 0.5], "EXT_SOURCE_3": [0.6, np.nan]})
    result = external_score_features(frame)
    assert abs(result["EXT_MEAN"][0] - 0.5) < 1e-9
    assert abs(result["EXT_MIN"][1] - 0.5) < 1e-9
    assert abs(result["EXT_PRODUCT"][0] - 0.24) < 1e-9


def test_recent_window_excludes_old_instalments():
    installments = pd.DataFrame(
        {
            "SK_ID_CURR": [1, 1, 1],
            "DAYS_INSTALMENT": [-800, -100, -50],
            "DAYS_ENTRY_PAYMENT": [-790, -100, -45],
            "AMT_INSTALMENT": [100.0, 100.0, 100.0],
            "AMT_PAYMENT": [100.0, 100.0, 100.0],
        }
    )
    result = recent_installment_features(installments)
    assert result.loc[1, "INST_RECENT_LATE_SHARE"] == 0.5
    assert result.loc[1, "INST_RECENT_MAX_DAYS_LATE"] == 5
    assert abs(result.loc[1, "INST_MEAN_DAYS_LATE"] - 5) < 1e-9
