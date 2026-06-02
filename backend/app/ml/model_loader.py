import joblib
from functools import lru_cache

MODEL_PATH = "ml_models/task_category_model_datasetv6.joblib"


# singleton for only loading once and caching the model in memory for subsequent calls
@lru_cache(maxsize=1)
def get_category_model():
    return joblib.load(MODEL_PATH)
