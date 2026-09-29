import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from llm.risk_analyst import DISCLAIMER, Driver, RiskContext, default_client, generate_note
from src.explain import local_attribution
from src.risk import BAND_LABELS, assign_band, expected_loss

REPORTS = ROOT / "reports"
MODELS = ROOT / "models"
NAVY, BLUE, GREY = "#0b2545", "#2a6fb0", "#8d99ae"

st.set_page_config(page_title="Credit Risk Analytics", layout="wide")
st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem;}
    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.12);
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 8px;
        padding: 12px 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_model():
    bundle = joblib.load(MODELS / "pd_model.joblib")
    profile = joblib.load(MODELS / "input_profile.joblib")
    return bundle, profile


@st.cache_data
def load_reports():
    return {
        "metrics": json.loads((REPORTS / "metrics.json").read_text()),
        "bands": pd.read_csv(REPORTS / "band_summary.csv"),
        "importance": pd.read_csv(REPORTS / "permutation_importance.csv", index_col=0),
        "segments": pd.read_csv(REPORTS / "segment_performance.csv"),
        "bins": pd.read_csv(REPORTS / "pd_bins.csv"),
        "reliability": pd.read_csv(REPORTS / "reliability.csv"),
        "comparison": pd.read_csv(REPORTS / "model_comparison.csv"),
    }


def banner():
    st.caption(DISCLAIMER)


def overview(reports):
    st.title("Credit Risk & Loan Underwriting Analytics")
    banner()
    test = reports["metrics"]["test"]
    cols = st.columns(4)
    cols[0].metric("ROC-AUC (test)", f"{test['roc_auc']:.3f}")
    cols[1].metric("PR-AUC (test)", f"{test['pr_auc']:.3f}", help="A random ranking would score 0.081")
    cols[2].metric("KS (test)", f"{test['ks']:.3f}")
    cols[3].metric("Brier (test)", f"{test['brier']:.4f}", help="Predicting the constant rate scores 0.0742")
    st.markdown(
        "The model estimates the probability that a Home Credit applicant will have early repayment "
        "difficulty (late on at least one of the first instalments). It is trained on 184,506 applicants, "
        "and these figures come from a separate test set of 61,503 opened once."
    )
    st.info("Use the sidebar to score an applicant, explore portfolio risk, or test loss assumptions.")


def portfolio(reports):
    st.title("Portfolio Analytics")
    banner()
    bands = reports["bands"].copy()
    bands["actual_default_rate"] *= 100
    st.subheader("Default rate by risk band (validation)")
    st.bar_chart(bands.set_index("band")["actual_default_rate"], color=BLUE)
    shown = bands.copy()
    shown["share"] = (shown["share"] * 100).round(1)
    shown["mean_pd"] = (shown["mean_pd"] * 100).round(2)
    shown["actual_default_rate"] = shown["actual_default_rate"].round(2)
    shown["expected_loss"] = (shown["expected_loss"] / 1e6).round(1)
    shown["realised_loss"] = (shown["realised_loss"] / 1e6).round(1)
    st.dataframe(
        shown.rename(
            columns={
                "share": "share of applicants (%)",
                "mean_pd": "mean predicted PD (%)",
                "actual_default_rate": "actual default rate (%)",
                "expected_loss": "expected loss (m)",
                "realised_loss": "realised loss (m)",
            }
        ),
        hide_index=True,
        use_container_width=True,
    )
    st.subheader("Model performance by segment")
    segments = reports["segments"].copy()
    segments[["actual", "predicted"]] = (segments[["actual", "predicted"]] * 100).round(2)
    segments["auc"] = segments["auc"].round(3)
    chosen = st.selectbox("Segment type", sorted({s.split("=")[0] for s in segments["segment"]}))
    st.dataframe(
        segments[segments["segment"].str.startswith(chosen + "=")].drop(columns="gap"),
        hide_index=True,
        use_container_width=True,
    )
    st.caption("Segment AUC is unreliable below about 1,000 applicants. No fairness claim is made.")


def build_applicant(profile, values):
    reference = profile["reference"]
    row = {column: np.nan for column in reference}
    for column, value in values.items():
        row[column] = value
    return pd.Series(row)


def assess(reports):
    st.title("Customer Risk Assessment")
    banner()
    bundle, profile = load_model()
    st.markdown(
        "Enter what you know about an applicant. Fields left as *unknown* are passed to the model as missing, "
        "which it handles natively. In the training data a missing external score was itself a risk signal, so leaving these unknown tends to raise the estimate. "
        "External scores and credit-history fields come from outside sources that a user could not normally type in; "
        "they are optional here, and results without them are weaker (the model loses about 0.03 AUC without the external scores)."
    )
    left, right = st.columns(2)
    values, known = {}, []
    with left:
        st.subheader("Loan and income")
        values["AMT_CREDIT"] = st.number_input("Loan amount", 45000.0, 4050000.0, 500000.0, 10000.0)
        values["AMT_ANNUITY"] = st.number_input("Annual repayment (annuity)", 1600.0, 260000.0, 25000.0, 1000.0)
        values["AMT_INCOME_TOTAL"] = st.number_input("Annual income", 25000.0, 1000000.0, 150000.0, 5000.0)
        values["AMT_GOODS_PRICE"] = st.number_input("Goods price", 40000.0, 4050000.0, 450000.0, 10000.0)
        years = st.slider("Years in current job", 0.0, 40.0, 5.0, 0.5)
        values["DAYS_EMPLOYED"] = -years * 365.25
        values["DAYS_EMPLOYED_ANOMALY"] = 0
        values["NAME_CONTRACT_TYPE"] = st.selectbox("Contract type", profile["categories"]["NAME_CONTRACT_TYPE"])
        known += ["AMT_CREDIT", "AMT_ANNUITY", "AMT_INCOME_TOTAL", "AMT_GOODS_PRICE", "DAYS_EMPLOYED", "NAME_CONTRACT_TYPE"]
    with right:
        st.subheader("Optional outside information")
        for label, name in [("External score 2 (0-1)", "EXT_SOURCE_2"), ("External score 3 (0-1)", "EXT_SOURCE_3")]:
            if st.checkbox(f"I know {label}"):
                values[name] = st.slider(label, 0.0, 1.0, 0.5, 0.01)
                known.append(name)
        if st.checkbox("I know the applicant's earlier-instalment record"):
            values["INST_LATE_SHARE"] = st.slider("Share of past instalments paid late", 0.0, 1.0, 0.05, 0.01)
            known.append("INST_LATE_SHARE")
        if st.checkbox("I know the applicant's bureau record"):
            values["BUREAU_CREDIT_COUNT"] = st.number_input("Number of credits on bureau record", 0, 50, 3)
            values["BUREAU_ACTIVE_COUNT"] = st.number_input("Of which active", 0, 50, 1)
            known += ["BUREAU_CREDIT_COUNT", "BUREAU_ACTIVE_COUNT"]
    values["CREDIT_INCOME_RATIO"] = values["AMT_CREDIT"] / values["AMT_INCOME_TOTAL"]
    values["ANNUITY_INCOME_RATIO"] = values["AMT_ANNUITY"] / values["AMT_INCOME_TOTAL"]
    values["CREDIT_ANNUITY_RATIO"] = values["AMT_CREDIT"] / values["AMT_ANNUITY"]
    known += ["CREDIT_INCOME_RATIO", "ANNUITY_INCOME_RATIO", "CREDIT_ANNUITY_RATIO"]
    lgd = st.slider("Assumed LGD", 0.1, 0.9, 0.45, 0.05)
    if not st.button("Assess applicant", type="primary"):
        return
    row = build_applicant(profile, values)
    columns = bundle["columns"]
    dtypes = {c: profile["dtypes"][c] for c in columns}
    template = pd.DataFrame({c: pd.Series(dtype=d) for c, d in dtypes.items()})
    applicant = pd.DataFrame([row[columns]]).astype(dtypes)
    probability = float(bundle["model"].predict_proba(applicant)[:, 1][0])
    band = str(assign_band([probability])[0])
    loss = float(expected_loss(probability, values["AMT_CREDIT"], lgd=lgd))
    cols = st.columns(4)
    cols[0].metric("Probability of default", f"{probability * 100:.1f}%")
    cols[1].metric("Risk band", band)
    cols[2].metric("Expected loss", f"{loss:,.0f}")
    cols[3].metric("Illustrative cutoff", f"{bundle['threshold'] * 100:.0f}%")
    if probability <= bundle["threshold"]:
        st.success("Below the illustrative approval cutoff.")
    else:
        st.warning("Above the illustrative approval cutoff.")
    reference = profile["reference"]
    known = list(dict.fromkeys(k for k in known if k in columns))
    effects = local_attribution(bundle["model"], row, reference, columns, template=template)
    effects = effects[effects.index.isin(known)].head(6)
    drivers = [
        Driver(
            feature=name,
            applicant_value=f"{row[name]:.4g}" if isinstance(row[name], (int, float, np.floating)) else str(row[name]),
            typical_value=f"{reference[name]:.4g}" if isinstance(reference[name], (int, float, np.floating)) else str(reference[name]),
            effect=float(effect),
            direction="raises" if effect > 0 else "lowers",
        )
        for name, effect in effects.items()
    ]
    st.subheader("Main drivers (occlusion, not SHAP)")
    st.dataframe(pd.DataFrame([d.model_dump() for d in drivers]), hide_index=True, use_container_width=True)
    bands = reports["bands"].set_index("band")
    st.session_state["context"] = RiskContext(
        pd=probability,
        band=band,
        cutoff=float(bundle["threshold"]),
        exposure=float(values["AMT_CREDIT"]),
        lgd=lgd,
        expected_loss=loss,
        portfolio_default_rate=float(reports["metrics"]["test"]["actual_rate"]),
        band_default_rate=float(bands.loc[band, "actual_default_rate"]),
        drivers=drivers,
    )
    st.caption("Open 'AI Risk Analyst' in the sidebar for a written note based on these numbers.")


def performance(reports):
    st.title("Model Performance")
    banner()
    test, bench = reports["metrics"]["test"], reports["metrics"]["benchmark_test"]
    table = pd.DataFrame({"Gradient boosting": test, "Logistic benchmark": bench}).T
    st.dataframe(table[["roc_auc", "pr_auc", "ks", "brier"]].round(4), use_container_width=True)
    st.subheader("Calibration by decile (validation)")
    rel = reports["reliability"].set_index("decile")[["predicted", "actual"]] * 100
    st.line_chart(rel, color=[GREY, BLUE])
    st.caption("Predicted and actual default rates agree in every decile, so no calibrator was needed.")
    st.subheader("Model and feature-set comparison (validation ROC-AUC)")
    pivot = reports["comparison"].pivot(index="model", columns="feature_set", values="validation_roc_auc")
    st.dataframe(pivot[["Application", "+ ratios", "+ history"]], use_container_width=True)


def explain(reports):
    st.title("Explainability")
    banner()
    imp = reports["importance"].head(15).iloc[::-1]
    st.subheader("Permutation importance (drop in AUC when a column is shuffled)")
    st.bar_chart(imp["auc_drop"], horizontal=True, color=BLUE)
    st.markdown(
        "Method: shuffle one column at a time on 25,000 validation rows. Correlated columns share importance, "
        "so loan-size variables (credit, goods price, annuity) understate their joint effect. "
        "Single-applicant drivers use occlusion (replace one feature with the typical value); this ignores interactions and is not SHAP."
    )


def loss_page(reports):
    st.title("Expected Loss and Approval Cutoff")
    banner()
    st.markdown("Expected loss = PD x LGD x EAD, with EAD = loan amount. The values below are project assumptions, not facts about any lender.")
    lgd = st.slider("LGD", 0.1, 0.9, 0.45, 0.05)
    margin = st.slider("Margin on a repaid loan", 0.01, 0.20, 0.08, 0.01)
    bins = reports["bins"]
    good = bins["credit_sum"] - bins["credit_sum_defaulted"]
    gain = (good * margin - bins["credit_sum_defaulted"] * lgd).cumsum()
    result = pd.DataFrame(
        {
            "approve if PD at most": bins["pd_upper"],
            "approval rate": bins["applicants"].cumsum() / bins["applicants"].sum(),
            "net value (m)": gain / 1e6,
        }
    )
    best = result.loc[result["net value (m)"].idxmax()]
    cols = st.columns(3)
    cols[0].metric("Best cutoff (PD)", f"{best['approve if PD at most'] * 100:.1f}%")
    cols[1].metric("Approval rate", f"{best['approval rate'] * 100:.0f}%")
    cols[2].metric("Net value vs approving all", f"{best['net value (m)'] - result['net value (m)'].iloc[-1]:,.0f} m")
    st.line_chart(result.set_index("approve if PD at most")["net value (m)"], color=BLUE)
    st.caption("Computed on the validation split in 200 risk bins, so cutoffs are accurate to about 0.5% of applicants.")


def analyst():
    st.title("AI Risk Analyst")
    banner()
    context = st.session_state.get("context")
    if context is None:
        st.info("Assess an applicant first; the note is written from that result.")
        return
    client = default_client()
    if client is None:
        st.caption("No ANTHROPIC_API_KEY set: showing the deterministic template note.")
    note, source = generate_note(context, client)
    st.write(note)
    st.caption(f"Source: {source}. The note may only use numbers from the model output; anything else triggers the template fallback.")
    with st.expander("Structured input given to the analyst"):
        st.json(json.loads(context.model_dump_json()))


def about():
    st.title("About")
    banner()
    st.markdown(
        """
**Data.** Home Credit Default Risk (Kaggle). The label is late payment on an early instalment, not lifetime default.

**Limits.** One random split of one historical portfolio, no time dimension, so nothing is known about performance after economic change.
The most valuable inputs are anonymised external scores that a real user could not supply. Age and gender are inputs of the trained model
(the effect of removing them was measured and is small); this app does not ask for gender. Loss and margin figures are illustrative.

**Not for real decisions.** This is an educational project and not a lending policy.
"""
    )


PAGES = {
    "Overview": lambda r: overview(r),
    "Portfolio Analytics": lambda r: portfolio(r),
    "Customer Risk Assessment": lambda r: assess(r),
    "Model Performance": lambda r: performance(r),
    "Explainability": lambda r: explain(r),
    "Expected Loss": lambda r: loss_page(r),
    "AI Risk Analyst": lambda r: analyst(),
    "About": lambda r: about(),
}

reports = load_reports()
choice = st.sidebar.radio("Page", list(PAGES))
PAGES[choice](reports)