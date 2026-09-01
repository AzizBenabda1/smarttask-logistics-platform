"""Pytest setup — ensure ML models exist for integration tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.config import get_settings


@pytest.fixture(scope="session", autouse=True)
def ensure_trained_models():
    settings = get_settings()
    delay_model = settings.models_dir / "delay_model.pkl"
    delivery_model = settings.models_dir / "delivery_time_model.pkl"
    dataset = Path("data/raw/smarttask_delivery_dataset.csv")

    if not delay_model.exists() or not delivery_model.exists():
        from app.ml.generate_dataset import generate_synthetic_dataset
        from app.ml.train_delay import train_delay_model
        from app.ml.train_delivery_time import train_delivery_time_model

        dataset.parent.mkdir(parents=True, exist_ok=True)
        if not dataset.exists():
            generate_synthetic_dataset(n_samples=1500).to_csv(dataset, index=False)
        train_delay_model(dataset, settings.models_dir)
        train_delivery_time_model(dataset, settings.models_dir)

    yield
