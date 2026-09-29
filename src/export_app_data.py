import numpy as np
import pandas as pd
import joblib

from src import config
from src.data import load_modelling_table

BINS = 200
MODEL_COMPARISON = [
    ("Logistic regression", "Application", 0.7467),
    ("Logistic regression", "+ ratios", 0.7483),
    ("Logistic regression", "+ history", 0.7577),
    ("Random forest", "Application", 0.7398),
    ("Random forest", "+ ratios", 0.7418),
    ("Random forest", "+ history", 0.7490),
    ("Gradient boosting", "Application", 0.7528),
    ("Gradient boosting", "+ ratios", 0.7601),
    ("Gradient boosting", "+ history", 0.7690),
]


def export():
    table = load_modelling_table()
    bundle = joblib.load(config.MODELS_DIR / "pd_model.joblib")
    profile = joblib.load(config.MODELS_DIR / "input_profile.joblib")
    profile["dtypes"] = {
        c: "float64" if pd.api.types.is_numeric_dtype(table[c]) else "object" for c in bundle["columns"]
    }
    joblib.dump(profile, config.MODELS_DIR / "input_profile.joblib")
    valid = table[table["split"] == "valid"]
    score = bundle["model"].predict_proba(valid[bundle["columns"]])[:, 1]
    frame = pd.DataFrame({"pd": score, "y": valid[config.TARGET].to_numpy(), "credit": valid["AMT_CREDIT"].to_numpy()})
    frame["bin"] = pd.qcut(frame["pd"].rank(method="first"), BINS, labels=False)
    frame["credit_defaulted"] = frame["credit"] * frame["y"]
    grouped = frame.groupby("bin")
    bins = pd.DataFrame(
        {
            "pd_upper": grouped["pd"].max(),
            "applicants": grouped.size(),
            "defaulters": grouped["y"].sum(),
            "credit_sum": grouped["credit"].sum(),
            "credit_sum_defaulted": grouped["credit_defaulted"].sum(),
            "pd_mean": grouped["pd"].mean(),
        }
    )
    bins.to_csv(config.REPORTS_DIR / "pd_bins.csv", index=False)
    frame["decile"] = pd.qcut(frame["pd"], 10, labels=False) + 1
    reliability = frame.groupby("decile").agg(predicted=("pd", "mean"), actual=("y", "mean"), applicants=("y", "size"))
    reliability.to_csv(config.REPORTS_DIR / "reliability.csv")
    pd.DataFrame(MODEL_COMPARISON, columns=["model", "feature_set", "validation_roc_auc"]).to_csv(
        config.REPORTS_DIR / "model_comparison.csv", index=False
    )
    return bins


if __name__ == "__main__":
    export()
