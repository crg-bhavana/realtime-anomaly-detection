import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


RESULTS_DIR = Path("results")
INPUT_PATH = RESULTS_DIR / "anomaly_results.csv"
OUTPUT_PATH = RESULTS_DIR / "anomaly_plot.png"


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_PATH)

    normal = df[df["anomaly"] == "normal"]
    anomaly = df[df["anomaly"] == "anomaly"]

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["avg_latency_ms"], label="Average Latency (ms)")
    plt.scatter(normal.index, normal["avg_latency_ms"], label="Normal")
    plt.scatter(anomaly.index, anomaly["avg_latency_ms"], label="Anomaly")

    plt.xlabel("Row Index")
    plt.ylabel("Average Latency (ms)")
    plt.title("Anomaly Detection on Service Health Metrics")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH)
    plt.show()

    print(f"Saved plot to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
