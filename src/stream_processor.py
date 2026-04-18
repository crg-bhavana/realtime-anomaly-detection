from datetime import datetime

import joblib
import pandas as pd

from src.anomaly_model import SCALER_PATH
from src.config import FEATURE_COLUMNS, MODEL_PATH, OUTPUT_DIR, ensure_dirs


def process_event(event: dict) -> dict:
    ensure_dirs()
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    row = pd.DataFrame([event])
    x_scaled = scaler.transform(row[FEATURE_COLUMNS])
    score = float(model.decision_function(x_scaled)[0])
    is_anomaly = int(model.predict(x_scaled)[0] == -1)

    result = {
        "timestamp": event.get("timestamp", datetime.utcnow().isoformat()),
        "service_name": event.get("service_name", "unknown"),
        "anomaly_score": round(score, 4),
        "is_anomaly": is_anomaly,
    }

    output_path = OUTPUT_DIR / "stream_alerts.csv"
    result_df = pd.DataFrame([result])
    header = not output_path.exists()
    result_df.to_csv(output_path, mode="a", index=False, header=header)
    return result
