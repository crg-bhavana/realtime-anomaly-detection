import argparse
from pathlib import Path

from src.anomaly_model import train_model, score_batch_data
from src.dashboard_export import export_alert_summary
from src.simulate_events import simulate_events_to_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Real-time anomaly detection system")
    parser.add_argument("--mode", required=True, choices=["train", "batch_score", "export_dashboard", "simulate"])
    parser.add_argument("--input", help="Path to historical CSV input")
    parser.add_argument("--events", type=int, default=100, help="Number of synthetic events to generate")
    args = parser.parse_args()

    if args.mode in {"train", "batch_score", "export_dashboard"} and not args.input:
        raise ValueError("--input is required for this mode")

    if args.mode == "train":
        train_model(Path(args.input))
    elif args.mode == "batch_score":
        score_batch_data(Path(args.input))
    elif args.mode == "export_dashboard":
        export_alert_summary(Path(args.input))
    elif args.mode == "simulate":
        simulate_events_to_csv(args.events)


if __name__ == "__main__":
    main()
