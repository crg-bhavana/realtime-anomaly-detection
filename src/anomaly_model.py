from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from src.config import CONTAMINATION, FEATURE_COLUMNS, MODEL_PATH, OUTPUT_DIR, RANDOM_STATE, ensure_dirs

SCALER_PATH = MODEL_PATH.with_name("scaler.joblib")
DEFAULT_INPUT_PATH = Path("data/sample/historical_metrics.csv")


def _load_data(input_path: Path) -> pd.DataFrame:
    df = pd.read_csv(input_path)
    missing = set(FEATURE_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df


def train_model(input_path: Path) -> None:
    ensure_dirs()
    df = _load_data(input_path)
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(df[FEATURE_COLUMNS])

    model = IsolationForest(
        contamination=CONTAMINATION,
        random_state=RANDOM_STATE,
        n_estimators=200,
    )
    model.fit(x_scaled)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    print(f"Saved model to {MODEL_PATH}")
    print(f"Saved scaler to {SCALER_PATH}")


def score_batch_data(input_path: Path) -> pd.DataFrame:
    ensure_dirs()
    df = _load_data(input_path)
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    x_scaled = scaler.transform(df[FEATURE_COLUMNS])

    df = df.copy()
    df["anomaly_score"] = model.decision_function(x_scaled)
    df["is_anomaly"] = (model.predict(x_scaled) == -1).astype(int)

    output_path = OUTPUT_DIR / "scored_events.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved scored events to {output_path}")
    return df


def main() -> None:
    print(f"Training anomaly model using: {DEFAULT_INPUT_PATH}")
    train_model(DEFAULT_INPUT_PATH)
    score_batch_data(DEFAULT_INPUT_PATH)


if __name__ == "__main__":
    main()