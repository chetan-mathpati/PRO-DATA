import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]

INPUT = ROOT / "ml" / "features" / "country_energy_features.csv"
MODEL_DIR = ROOT / "ml" / "artifacts"
EVALUATION_DIR = ROOT / "ml" / "evaluation"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
EVALUATION_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT)

FEATURES = [
    "gdp_growth_pct",
    "inflation_pct",
    "unemployment_pct",
    "trade_pct_gdp",
    "exports_pct_gdp",
    "imports_pct_gdp",
    "total_petroleum_production_tbpd",
    "crude_oil_production_tbpd",
    "petroleum_consumption_tj",
    "petroleum_production_yoy_pct",
    "crude_oil_production_yoy_pct",
    "gdp_growth_5yr_avg",
    "inflation_5yr_avg",
    "petroleum_production_5yr_avg",
    "previous_production",
    "production_two_years_ago",
]

TARGET = "next_year_production_decline_target"

df = df.dropna(subset=[TARGET]).copy()

# Chronological split.
# Earlier observations are used for training and later observations
# are reserved for evaluation.
cutoff = df["year"].quantile(0.80)

train = df[df["year"] <= cutoff].copy()
test = df[df["year"] > cutoff].copy()

X_train = train[FEATURES]
y_train = train[TARGET].astype(int)

X_test = test[FEATURES]
y_test = test[TARGET].astype(int)

numeric_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("numeric", numeric_pipeline, FEATURES),
    ]
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            LogisticRegression(
                max_iter=2000,
                class_weight="balanced",
                random_state=42,
            ),
        ),
    ]
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]

metrics = {
    "train_rows": int(len(train)),
    "test_rows": int(len(test)),
    "train_year_min": int(train["year"].min()),
    "train_year_max": int(train["year"].max()),
    "test_year_min": int(test["year"].min()),
    "test_year_max": int(test["year"].max()),
    "accuracy": float(
        accuracy_score(y_test, predictions)
    ),
    "precision": float(
        precision_score(
            y_test,
            predictions,
            zero_division=0,
        )
    ),
    "recall": float(
        recall_score(
            y_test,
            predictions,
            zero_division=0,
        )
    ),
    "roc_auc": (
        float(
            roc_auc_score(
                y_test,
                probabilities,
            )
        )
        if y_test.nunique() > 1
        else None
    ),
}

joblib.dump(
    model,
    MODEL_DIR / "petroleum_decline_model.joblib",
)

with open(
    MODEL_DIR / "evaluation.json",
    "w",
    encoding="utf-8",
) as f:
    json.dump(metrics, f, indent=2)

predictions_df = test[
    [
        "country_code",
        "country_name",
        "year",
        "total_petroleum_production_tbpd",
    ]
].copy()

predictions_df["actual_decline"] = y_test.values
predictions_df["predicted_decline"] = predictions
predictions_df["decline_probability"] = probabilities

predictions_df.to_csv(
    EVALUATION_DIR / "test_predictions.csv",
    index=False,
)

print("=" * 60)
print("MODEL TRAINING COMPLETE")
print("=" * 60)
print(json.dumps(metrics, indent=2))
print()
print("CLASSIFICATION REPORT")
print(classification_report(
    y_test,
    predictions,
    zero_division=0,
))
