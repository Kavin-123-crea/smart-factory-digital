import numpy as np
import pandas as pd
import joblib

from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "predictive_maintenance_model.pkl"
RANDOM_STATE = 42

FEATURES = [
    "Temperature",
    "Power_kW",
    "Cycle_Time",
    "Conveyor_Speed",
    "Production_Count",
]

# --------------------------------------------------
# GENERATE SYNTHETIC FACTORY HISTORY
# --------------------------------------------------

def generate_data(n_samples=5000):
    rng = np.random.default_rng(RANDOM_STATE)

    temperature = rng.uniform(28, 65, n_samples)
    power = rng.uniform(0.5, 6.0, n_samples)
    cycle_time = rng.uniform(1.5, 7.0, n_samples)
    conveyor_speed = rng.uniform(0.0, 1.5, n_samples)
    production_count = rng.integers(0, 5000, n_samples)

    # Synthetic risk rule:
    # Higher temperature, power and cycle time increase risk.
    risk_score = (
        0.35 * np.clip((temperature - 40) / 25, 0, 1)
        + 0.20 * np.clip((power - 3) / 3, 0, 1)
        + 0.35 * np.clip((cycle_time - 2.5) / 4.5, 0, 1)
        + 0.10 * np.clip((0.5 - conveyor_speed) / 0.5, 0, 1)
    )

    # Introduce variation so the target is not perfectly deterministic.
    risk_score += rng.normal(0, 0.08, n_samples)
    failure_risk = (risk_score >= 0.40).astype(int)

    df = pd.DataFrame({
        "Temperature": temperature,
        "Power_kW": power,
        "Cycle_Time": cycle_time,
        "Conveyor_Speed": conveyor_speed,
        "Production_Count": production_count,
        "Failure_Risk": failure_risk,
    })

    return df


# --------------------------------------------------
# TRAIN AND EVALUATE
# --------------------------------------------------

def main():
    print("=" * 60)
    print("SMART FACTORY - PREDICTIVE MAINTENANCE")
    print("=" * 60)

    df = generate_data()

    X = df[FEATURES]
    y = df["Failure_Risk"]

    print(f"Generated samples: {len(df)}")
    print(f"Normal samples: {(y == 0).sum()}")
    print(f"Risk samples: {(y == 1).sum()}")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=8,
        min_samples_leaf=3,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("\n--- TEST RESULTS ---")
    print(f"Accuracy : {accuracy_score(y_test, predictions):.4f}")
    print(
        f"Precision: "
        f"{precision_score(y_test, predictions, zero_division=0):.4f}"
    )
    print(
        f"Recall   : "
        f"{recall_score(y_test, predictions, zero_division=0):.4f}"
    )
    print(
        f"F1 Score : "
        f"{f1_score(y_test, predictions, zero_division=0):.4f}"
    )

    print("\nClassification report:")
    print(classification_report(
        y_test,
        predictions,
        target_names=["Normal", "Failure Risk"],
        zero_division=0,
    ))

    print("Confusion matrix:")
    print(confusion_matrix(y_test, predictions))

    joblib.dump({
        "model": model,
        "features": FEATURES,
        "target_description": (
            "Synthetic risk label based on generated operating conditions"
        ),
    }, MODEL_PATH)

    print(f"\nModel saved to: {MODEL_PATH}")

    # Example prediction using one synthetic sample.
    sample = X_test.iloc[[0]]
    risk_probability = model.predict_proba(sample)[0][
        list(model.classes_).index(1)
    ]

    print("\n--- EXAMPLE PREDICTION ---")
    print(sample.to_string(index=False))
    print(f"Estimated synthetic failure risk: {risk_probability:.1%}")

    print("\nNOTE: Training and testing use synthetic data.")
    print("This is a prototype, not a validated real-machine failure predictor.")


if __name__ == "__main__":
    main()