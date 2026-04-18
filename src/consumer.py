import json

from kafka import KafkaConsumer

from src.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC
from src.stream_processor import process_event


def consume_events() -> None:
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        group_id="anomaly-detector-group",
    )

    print(f"Listening on topic '{KAFKA_TOPIC}' at {KAFKA_BOOTSTRAP_SERVERS}...")

    for message in consumer:
        event = message.value
        result = process_event(event)
        print(result)


def main() -> None:
    consume_events()


if __name__ == "__main__":
    main()