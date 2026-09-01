import json
import logging
from enum import Enum
from pathlib import Path
from typing import Any

import joblib

from app.config.settings import Settings

logger = logging.getLogger(__name__)


class ModelState(str, Enum):
    LOADED = "loaded"
    NOT_FOUND = "not_found"
    ERROR = "error"


class ModelService:
    """Loads ML models once at startup and serves predictions."""

    DELAY_MODEL_FILE = "delay_model.pkl"
    DELIVERY_TIME_MODEL_FILE = "delivery_time_model.pkl"
    DELIVERY_SUCCESS_MODEL_FILE = "delivery_success_model.pkl"
    PRIORITY_MODEL_FILE = "priority_model.pkl"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.models_dir = settings.models_dir
        self.delay_model: Any | None = None
        self.delivery_time_model: Any | None = None
        self.delivery_success_model: Any | None = None
        self.priority_model: Any | None = None
        self._prediction_count = 0
        self._error_count = 0

    def load_all(self) -> None:
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self._load_metadata()
        self.delay_model = self._load_model(self.DELAY_MODEL_FILE, "delay")
        self.delivery_time_model = self._load_model(
            self.DELIVERY_TIME_MODEL_FILE, "delivery_time"
        )
        self.delivery_success_model = self._load_model(
            self.DELIVERY_SUCCESS_MODEL_FILE, "delivery_success"
        )
        self.priority_model = self._load_model(self.PRIORITY_MODEL_FILE, "priority")

    def _load_metadata(self) -> None:
        meta_path = self.models_dir / "model_metadata.json"
        if not meta_path.exists():
            return
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            if "delay_model_version" in meta:
                self.settings.delay_model_version = meta["delay_model_version"]
            if "delivery_time_model_version" in meta:
                self.settings.delivery_time_model_version = meta["delivery_time_model_version"]
            if "delivery_success_model_version" in meta:
                self.settings.delivery_success_model_version = meta[
                    "delivery_success_model_version"
                ]
            if "priority_model_version" in meta:
                self.settings.priority_model_version = meta["priority_model_version"]
            logger.info("Loaded model metadata from %s", meta_path)
        except Exception as exc:
            logger.warning("Could not load model metadata: %s", exc)

    def _load_model(self, filename: str, name: str) -> Any | None:
        path = self.models_dir / filename
        if not path.exists():
            logger.warning("Model %s not found at %s — train models first", name, path)
            return None
        try:
            model = joblib.load(path)
            logger.info("Model loaded: %s (%s)", name, path)
            return model
        except Exception as exc:
            logger.error("Failed to load model %s: %s", name, exc)
            self._error_count += 1
            return None

    def model_state(self, model: Any | None) -> ModelState:
        if model is not None:
            return ModelState.LOADED
        path_exists = any(self.models_dir.glob("*.pkl"))
        return ModelState.NOT_FOUND if not path_exists else ModelState.ERROR

    def record_prediction(self) -> None:
        self._prediction_count += 1

    def record_error(self) -> None:
        self._error_count += 1

    def get_metrics(self) -> dict[str, Any]:
        return {
            "predictionCount": self._prediction_count,
            "errorCount": self._error_count,
            "delayModelVersion": self.settings.delay_model_version,
            "deliveryTimeModelVersion": self.settings.delivery_time_model_version,
            "deliverySuccessModelVersion": self.settings.delivery_success_model_version,
            "priorityModelVersion": self.settings.priority_model_version,
        }

    def require_delay_model(self) -> Any:
        if self.delay_model is None:
            raise ModelNotLoadedError("delay_model")
        return self.delay_model

    def require_delivery_time_model(self) -> Any:
        if self.delivery_time_model is None:
            raise ModelNotLoadedError("delivery_time_model")
        return self.delivery_time_model

    def require_delivery_success_model(self) -> Any:
        if self.delivery_success_model is None:
            raise ModelNotLoadedError("delivery_success_model")
        return self.delivery_success_model


class ModelNotLoadedError(Exception):
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        super().__init__(f"Model '{model_name}' is not loaded. Run training scripts first.")
