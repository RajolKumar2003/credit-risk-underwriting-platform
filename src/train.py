import time

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    FunctionTransformer,
    OneHotEncoder,
    OrdinalEncoder,
    SplineTransformer,
    StandardScaler,
)

from src import config
from src.evaluate import evaluate
from src.features import RATIO_FEATURES
from src.history import HISTORY_FEATURES

EXTERNAL_SCORES = ["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]
SOCIAL_CIRCLE = [
    "OBS_30_CNT_SOCIAL_CIRCLE",
    "DEF_30_CNT_SOCIAL_CIRCLE",
    "OBS_60_CNT_SOCIAL_CIRCLE",
    "DEF_60_CNT_SOCIAL_CIRCLE",
]
POSITIVE_AMOUNTS = [
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "AMT_GOODS_PRICE",
    "INCOME_PER_FAMILY_MEMBER",
]
NOT_FEATURES = [config.ID_COLUMN, config.TARGET, "split"]


def feature_columns(table, ratios=False, history=False, drop=()):
    excluded = set(NOT_FEATURES) | set(RATIO_FEATURES) | set(HISTORY_FEATURES)
    columns = [c for c in table.columns if c not in excluded]
    if ratios:
        columns += RATIO_FEATURES
    if history:
        columns += HISTORY_FEATURES
    return [c for c in columns if c not in set(drop)]


def split_by_type(table, columns):
    numeric = [c for c in columns if pd.api.types.is_numeric_dtype(table[c])]
    categorical = [c for c in columns if c not in numeric]
    return categorical, numeric


def make_logistic(table, columns, class_weight=None, log_amounts=False, spline_columns=(), C=1.0):
    categorical, numeric = split_by_type(table, columns)
    splined = [c for c in numeric if c in spline_columns]
    logged = [c for c in numeric if log_amounts and c in POSITIVE_AMOUNTS and c not in splined]
    plain = [c for c in numeric if c not in logged and c not in splined]
    fill_and_scale = [
        ("impute", SimpleImputer(strategy="median", add_indicator=True)),
        ("scale", StandardScaler()),
    ]
    transformers = [
        (
            "categories",
            Pipeline(
                [
                    ("impute", SimpleImputer(strategy="constant", fill_value="Missing")),
                    ("onehot", OneHotEncoder(handle_unknown="ignore", min_frequency=200, sparse_output=False)),
                ]
            ),
            categorical,
        ),
        ("numbers", Pipeline(fill_and_scale), plain),
    ]
    if logged:
        log_step = [("log", FunctionTransformer(np.log1p, feature_names_out="one-to-one"))]
        transformers.append(("log_numbers", Pipeline(log_step + fill_and_scale), logged))
    if splined:
        spline_step = [
            ("impute", SimpleImputer(strategy="median")),
            ("spline", SplineTransformer(n_knots=6, degree=3, knots="quantile", extrapolation="constant")),
        ]
        transformers.append(("splines", Pipeline(spline_step), splined))
    preprocess = ColumnTransformer(transformers, verbose_feature_names_out=False)
    model = LogisticRegression(C=C, max_iter=1000, class_weight=class_weight, random_state=config.RANDOM_SEED)
    return Pipeline([("prepare", preprocess), ("model", model)])


def ordinal_preprocess(table, columns):
    categorical, numeric = split_by_type(table, columns)
    encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=np.nan)
    preprocess = ColumnTransformer(
        [("categories", encoder, categorical), ("numbers", "passthrough", numeric)],
        verbose_feature_names_out=False,
    )
    return preprocess, len(categorical), len(numeric)


def make_boosting(table, columns, class_weight=None, **settings):
    preprocess, n_categorical, n_numeric = ordinal_preprocess(table, columns)
    is_categorical = np.array([True] * n_categorical + [False] * n_numeric)
    parameters = {
        "learning_rate": 0.06,
        "max_iter": 500,
        "min_samples_leaf": 100,
        "l2_regularization": 1.0,
        "early_stopping": True,
        "validation_fraction": 0.1,
        "n_iter_no_change": 25,
    }
    parameters.update(settings)
    model = HistGradientBoostingClassifier(
        categorical_features=is_categorical,
        class_weight=class_weight,
        random_state=config.RANDOM_SEED,
        **parameters,
    )
    return Pipeline([("prepare", preprocess), ("model", model)])


def make_forest(table, columns, class_weight=None, **settings):
    preprocess, _, _ = ordinal_preprocess(table, columns)
    parameters = {"n_estimators": 100, "min_samples_leaf": 50, "max_samples": 0.5, "n_jobs": -1}
    parameters.update(settings)
    model = RandomForestClassifier(class_weight=class_weight, random_state=config.RANDOM_SEED, **parameters)
    return Pipeline([("prepare", preprocess), ("model", model)])


def fit_and_score(model, table, columns, evaluate_on="valid"):
    if evaluate_on == "test":
        raise ValueError("The test split is reserved for the final model.")
    train = table[table["split"] == "train"]
    held_out = table[table["split"] == evaluate_on]
    started = time.time()
    model.fit(train[columns], train[config.TARGET])
    probabilities = model.predict_proba(held_out[columns])[:, 1]
    scores = evaluate(held_out[config.TARGET], probabilities)
    scores["seconds"] = time.time() - started
    return scores, probabilities


def final_test_score(model, table, columns):
    train = table[table["split"] == "train"]
    test = table[table["split"] == "test"]
    model.fit(train[columns], train[config.TARGET])
    probabilities = model.predict_proba(test[columns])[:, 1]
    return evaluate(test[config.TARGET], probabilities), probabilities
