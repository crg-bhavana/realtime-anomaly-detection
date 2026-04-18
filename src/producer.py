import json
import time
from pathlib import Path
from typing import Iterable

import pandas as pd
from kafka import KafkaProducer

from src.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC


def create_producer() -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


def stream_events(events: Iterable[dict], delay_seconds: float = 0.2) -> None:
    producer = create_producer()
    for event in events:
        producer.send(KAFKA_TOPIC, event)
        producer.flush()
        print(f"Sent event: {event}")
        time.sleep(delay_seconds)
    producer.close()


def load_sample_events() -> list[dict]:
    candidates = [
        Path("results/anomaly_results.csv"),
        Path("data/sample/events.csv"),
        Path("data/sample/simulated_events.csv"),
    ]
    for path in candidates:
        if path.exists():
            df = pd.read_csv(path)
            if "anomaly" in df.columns:
                df = df.drop(columns=["anomaly"])
            return df.to_dict(orient="records")
    raise FileNotFoundError("No sample events CSV found in expected locations.")


def main() -> None:
    events = load_sample_events()
    stream_events(events)


if __name__ == "__main__":
    main()