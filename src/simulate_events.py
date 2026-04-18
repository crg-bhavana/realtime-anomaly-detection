from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import OUTPUT_DIR, ensure_dirs


SERVICES = ["payments-api", "orders-api", "auth-service", "catalog-service"]


def _generate_event(idx: int) -> dict:
    np.random.seed(idx + 42)
    service_name = SERVICES[idx % len(SERVICES)]
    anomaly_boost = 1 if idx % 17 == 0 else 0
    return {
        "timestamp": (datetime.utcnow() + timedelta(seconds=idx)).isoformat(),
        "service_name": service_name,
        "request_count": int(np.random.normal(1200 + 500 * anomaly_boost, 120)),
        "error_rate": round(max(0.0, np.random.normal(0.02 + 0.12 * anomaly_boost, 0.01)), 4),
        "avg_latency_ms": round(max(1.0, np.random.normal(180 + 350 * anomaly_boost, 20)), 2),
        "cpu_utilization": round(min(100.0, np.random.normal(55 + 25 * anomaly_boost, 8)), 2),
        "memory_utilization": round(min(100.0, np.random.normal(60 + 20 * anomaly_boost, 7)), 2),
    }


def generate_events(num_events: int) -> list[dict]:
    return [_generate_event(i) for i in range(num_events)]


def simulate_events_to_csv(num_events: int) -> Path:
    ensure_dirs()
    events = generate_events(num_events)
    df = pd.DataFrame(events)
    output_path = OUTPUT_DIR / "simulated_events.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved simulated events to {output_path}")
    return output_path
