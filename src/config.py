from pathlib import Path

import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = BASE_DIR / "artifacts"
MODEL_DIR = ARTIFACT_DIR / "models"
OUTPUT_DIR = ARTIFACT_DIR / "outputs"
MODEL_PATH = MODEL_DIR / "isolation_forest.joblib"
CONFIG_PATH = BASE_DIR / "config" / "settings.yaml"


with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    SETTINGS = yaml.safe_load(f)

FEATURE_COLUMNS = SETTINGS["features"]
KAFKA_BOOTSTRAP_SERVERS = SETTINGS["kafka"]["bootstrap_servers"]
KAFKA_TOPIC = SETTINGS["kafka"]["topic"]
CONTAMINATION = SETTINGS["model"]["contamination"]
RANDOM_STATE = SETTINGS["model"]["random_state"]


def ensure_dirs() -> None:
    for path in [ARTIFACT_DIR, MODEL_DIR, OUTPUT_DIR]:
        path.mkdir(parents=True, exist_ok=True)
