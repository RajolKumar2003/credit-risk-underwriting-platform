import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance


def reference_row(train, columns):
    values = {}
    for column in columns:
        series = train[column]
        if pd.api.types.is_numeric_dtype(series):
            values[column] = series.median()
        else:
            values[column] = series.mode(dropna=True).iloc[0] if series.notna().any() else np.nan
    return values


def _log_odds(probability):
    probability = np.clip(probability, 1e-9, 1 - 1e-9)
    return np.log(probability / (1 - probability))


def local_attribution(model, row, reference, columns, template=None):
    dtypes = (template if template is not None else pd.DataFrame([row[columns]]))[columns].dtypes.to_dict()
    row_frame = pd.DataFrame([row[columns]]).astype(object)
    variants = pd.concat([row_frame] * len(columns), ignore_index=True)
    for position, column in enumerate(columns):
        variants.loc[position, column] = reference[column]
    variants = variants.astype(dtypes)
    row_frame = row_frame.astype(dtypes)
    base = _log_odds(model.predict_proba(row_frame)[:, 1][0])
    replaced = _log_odds(model.predict_proba(variants)[:, 1])
    effect = pd.Series(base - replaced, index=columns)
    return effect.sort_values(key=np.abs, ascending=False)


def global_importance(model, frame, target, columns, repeats=3, seed=42):
    result = permutation_importance(
        model, frame[columns], target, scoring="roc_auc", n_repeats=repeats, random_state=seed, n_jobs=1
    )
    return (
        pd.DataFrame({"auc_drop": result.importances_mean, "spread": result.importances_std}, index=columns)
        .sort_values("auc_drop", ascending=False)
    )
