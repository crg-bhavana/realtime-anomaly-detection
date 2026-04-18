import pandas as pd
from sklearn.ensemble import IsolationForest


FEATURE_COLUMNS = [
    "request_count",
    "error_rate",
    "avg_latency_ms",
    "cpu_utilization",
    "memory_utilization",
]


def main():
    df = pd.read_csv("data/sample/historical_metrics.csv")

    print("Columns:", df.columns.tolist())
    print(df.head())

    model = IsolationForest(contamination=0.1, random_state=42)

    df["anomaly_flag"] = model.fit_predict(df[FEATURE_COLUMNS])
    df["anomaly"] = df["anomaly_flag"].map({1: "normal", -1: "anomaly"})

    print("\nAnomaly Detection Results:")
    print(df[["timestamp", "service_name"] + FEATURE_COLUMNS + ["anomaly"]])

    df.to_csv("results/anomaly_results.csv", index=False)
    print("\nSaved results to results/anomaly_results.csv")


if __name__ == "__main__":
    main()