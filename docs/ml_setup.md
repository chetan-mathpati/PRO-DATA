PRO DATA - ML SETUP

PURPOSE

The ML component provides an experimental baseline for identifying
countries where petroleum production may decline by at least
10 percent in the following year.


FEATURE GENERATION

Run:

python ml/features/build_features.py

The feature pipeline reads the analytical mart:

analytics.mart_country_economic_energy

and creates:

ml/features/country_energy_features.csv

The target is based on the following year's observed petroleum
production.


MODEL TRAINING

Run:

python ml/training/train_model.py

The training pipeline:

1. Loads the generated feature dataset.
2. Removes rows without a known target.
3. Splits observations chronologically.
4. Imputes missing numeric values using the training pipeline.
5. Standardizes numeric features.
6. Trains logistic regression with balanced class weights.
7. Evaluates the held-out period.
8. Saves the trained model.
9. Saves evaluation metrics.
10. Saves test predictions.


OUTPUTS

ml/artifacts/petroleum_decline_model.joblib
Trained model pipeline.

ml/artifacts/evaluation.json
Evaluation metrics and train/test period information.

ml/evaluation/test_predictions.csv
Country-level held-out predictions and probabilities.


VALIDATION

The train/test split is chronological rather than random because
the target represents a future-year outcome.

This reduces the risk of temporal leakage during evaluation.


INTERPRETATION

The current model is an experimental analytical baseline.

Its evaluation results should be interpreted as a model diagnostic,
not as evidence of reliable production forecasting capability.

The model is not presented as a production forecasting service.