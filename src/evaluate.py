from scipy import stats
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score


def evaluate(y_true, y_score):
    y_true = y_true.to_numpy()
    ks = stats.ks_2samp(y_score[y_true == 1], y_score[y_true == 0]).statistic
    return {
        "roc_auc": roc_auc_score(y_true, y_score),
        "pr_auc": average_precision_score(y_true, y_score),
        "ks": ks,
        "brier": brier_score_loss(y_true, y_score),
        "mean_predicted": y_score.mean(),
        "actual_rate": y_true.mean(),
    }


def reference_scores(y_true):
    rate = y_true.mean()
    return {
        "pr_auc_of_random_ranking": rate,
        "brier_of_constant_rate": rate * (1 - rate),
    }
