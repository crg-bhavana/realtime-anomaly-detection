from pathlib import Path

import pandas as pd

from src.anomaly_model import score_batch_data
from src.config import OUTPUT_DIR


def export_alert_summary(input_path: Path) -> None:
    df = score_batch_data(input_path)
    summary = (
        df.groupby("service_name", as_index=False)
        .agg(
            total_events=("service_name", "size"),
            anomaly_events=("is_anomaly", "sum"),
            avg_latency_ms=("avg_latency_ms", "mean"),
            avg_error_rate=("error_rate", "mean"),
        )
    )
    summary["anomaly_rate_pct"] = (summary["anomaly_events"] / summary["total_events"] * 100).round(2)
    output_path = OUTPUT_DIR / "dashboard_alert_summary.csv"
    summary.to_csv(output_path, index=False)
    print(f"Saved dashboard alert summary to {output_path}")
