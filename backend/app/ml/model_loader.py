from functools import lru_cache
from pathlib import Path

import joblib

MODEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "ml_models"
    / "task_category_model_datasetv6.joblib"
)


# singleton for only loading once and caching the model in memory for subsequent calls
@lru_cache(maxsize=1)
def get_category_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"ML model not found: {MODEL_PATH}")

    return joblib.load(MODEL_PATH)
