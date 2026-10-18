
import json
from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ==================================================
# 1. DEFINE PROJECT PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

VALUES_PATH = BASE_DIR / "train_values.csv"
LABELS_PATH = BASE_DIR / "train_labels.csv"
MODEL_PATH = BASE_DIR / "structural_damage_simple_model.pkl"
METRICS_PATH = BASE_DIR / "model_metrics.json"

# ==================================================
# 2. LOAD DATASET
# ==================================================

print("Loading dataset...")

X = pd.read_csv(VALUES_PATH)
y_data = pd.read_csv(LABELS_PATH)

if "damage_grade" not in y_data.columns:
    raise ValueError("The labels CSV must contain a damage_grade column.")

y = y_data["damage_grade"]

# Ensure the input and target rows correspond
if len(X) != len(y):
    raise ValueError("Training data and labels have different row counts.")

print("Dataset loaded successfully.")
print("Total samples:", len(X))

# ==================================================
# 3. PREPARE BUILDING FEATURES
# ==================================================

required_columns = [
    "age",
    "count_floors_pre_eq",
    "count_families",
    "area_percentage",
    "height_percentage",
    "has_secondary_use"
]

missing_columns = [
    column for column in required_columns
    if column not in X.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required dataset columns: {missing_columns}"
    )

# Building size
X["building_size"] = pd.cut(
    X["area_percentage"],
    bins=[-1, 5, 15, float("inf")],
    labels=["Small", "Medium", "Large"]
).astype(str)

# Building height
X["building_height"] = pd.cut(
    X["height_percentage"],
    bins=[-1, 3, 6, float("inf")],
    labels=["Low", "Medium", "High"]
).astype(str)

# Construction material indicators
material_columns = [
    "has_superstructure_adobe_mud",
    "has_superstructure_mud_mortar_stone",
    "has_superstructure_stone_flag",
    "has_superstructure_cement_mortar_stone",
    "has_superstructure_mud_mortar_brick",
    "has_superstructure_cement_mortar_brick",
    "has_superstructure_timber",
    "has_superstructure_bamboo",
    "has_superstructure_rc_non_engineered",
    "has_superstructure_rc_engineered",
    "has_superstructure_other"
]

# Use only material columns present in the dataset
available_material_columns = [
    column for column in material_columns
    if column in X.columns
]

def get_material(row):
    for column in available_material_columns:
        if row[column] == 1:
            return (
                column
                .replace("has_superstructure_", "")
                .replace("_", " ")
                .title()
            )
    return "Other"

X["construction_material"] = X.apply(
    get_material,
    axis=1
)

# Building usage
X["building_usage"] = X["has_secondary_use"].map({
    0: "Residential",
    1: "Other"
})

# Handle missing values in the derived features
X["building_usage"] = X["building_usage"].fillna("Other")

# Select the seven application features
feature_columns = [
    "age",
    "count_floors_pre_eq",
    "count_families",
    "building_size",
    "building_height",
    "construction_material",
    "building_usage"
]

X = X[feature_columns].copy()

# ==================================================
# 4. PREPROCESS FEATURES
# ==================================================

categorical_features = [
    "building_size",
    "building_height",
    "construction_material",
    "building_usage"
]

numerical_features = [
    "age",
    "count_floors_pre_eq",
    "count_families"
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)

# ==================================================
# 5. CREATE RANDOM FOREST MODEL
# ==================================================

model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    (
        "classifier",
        RandomForestClassifier(
            n_estimators=250,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        )
    )
])

# ==================================================
# 6. SPLIT DATA INTO TRAINING AND TESTING SETS
# ==================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

# ==================================================
# 7. TRAIN THE MODEL
# ==================================================

print("\nTraining Random Forest model...")

model.fit(X_train, y_train)

print("Training completed successfully.")

# ==================================================
# 8. CALCULATE ACCURACY AND CONFUSION MATRIX
# ==================================================

y_pred = model.predict(X_test)

# Actual test accuracy
accuracy = accuracy_score(y_test, y_pred)

# Preserve the actual class labels and their order
labels = sorted(y.unique())

# Confusion matrix
cm = confusion_matrix(
    y_test,
    y_pred,
    labels=labels
)

# Detailed classification report
report_text = classification_report(
    y_test,
    y_pred,
    labels=labels,
    zero_division=0
)

report_dict = classification_report(
    y_test,
    y_pred,
    labels=labels,
    output_dict=True,
    zero_division=0
)

print("\n" + "=" * 45)
print("       MODEL EVALUATION RESULTS")
print("=" * 45)

print(f"\nModel Accuracy: {accuracy * 100:.2f}%")

print("\nConfusion Matrix:")
print(cm)

print("\nClassification Report:")
print(report_text)

print("Number of test samples:", len(y_test))

# ==================================================
# 9. SAVE TRAINED MODEL
# ==================================================

joblib.dump(model, MODEL_PATH)

print(f"\nTrained model saved to: {MODEL_PATH}")

# ==================================================
# 10. SAVE METRICS FOR THE DASHBOARD
# ==================================================

metrics = {
    "accuracy": round(float(accuracy), 4),
    "accuracy_percentage": round(float(accuracy * 100), 2),
    "class_labels": [int(label) for label in labels],
    "confusion_matrix": cm.tolist(),
    "classification_report": report_dict,
    "test_samples": int(len(y_test))
}

with open(METRICS_PATH, "w", encoding="utf-8") as file:
    json.dump(metrics, file, indent=4)

print(f"Evaluation metrics saved to: {METRICS_PATH}")

print("\n" + "=" * 45)
print("MODEL TRAINING AND EVALUATION COMPLETED")
print("=" * 45)
