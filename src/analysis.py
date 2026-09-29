import numpy as np
import pandas as pd
from scipy import stats


def add_missing_category(groups):
    groups = groups.astype("category")
    return groups.cat.add_categories("Missing").fillna("Missing")


def default_rate_table(target, groups, confidence=0.95):
    frame = pd.DataFrame({"target": target, "group": groups})
    table = frame.groupby("group", observed=True)["target"].agg(n="size", defaults="sum")
    intervals = [
        stats.binomtest(int(k), int(n)).proportion_ci(confidence_level=confidence, method="wilson")
        for k, n in zip(table["defaults"], table["n"])
    ]
    table["rate"] = table["defaults"] / table["n"]
    table["low"] = [interval.low for interval in intervals]
    table["high"] = [interval.high for interval in intervals]
    table["label"] = [f"{name}\n(n={n:,})" for name, n in zip(table.index, table["n"])]
    return table.reset_index()


def chi_square_test(target, groups):
    counts = pd.crosstab(groups, target)
    chi2, p_value, dof, _ = stats.chi2_contingency(counts)
    cramers_v = np.sqrt(chi2 / (counts.to_numpy().sum() * (min(counts.shape) - 1)))
    return {"chi2": chi2, "dof": dof, "p_value": p_value, "cramers_v": cramers_v}


def mann_whitney_auc(values, target):
    present = values.notna()
    positives = values[present & (target == 1)]
    negatives = values[present & (target == 0)]
    u_statistic, p_value = stats.mannwhitneyu(positives, negatives, alternative="two-sided")
    auc = u_statistic / (len(positives) * len(negatives))
    return {"auc": auc, "p_value": p_value, "n": int(present.sum())}
