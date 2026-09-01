"""Train delivery time regression model."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor

from app.config import get_settings
from app.ml.evaluation import evaluate_regressor, select_best_regressor
from app.ml.preprocessing import prepare_delivery_dataset


def build_candidates() -> dict[str, Pipeline]:
    return {
        "linear_regression": Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", LinearRegression()),
            ]
        ),
        "random_forest": Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "model",
                    RandomForestRegressor(
                        n_estimators=200,
                        max_depth=14,
                        random_state=42,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
        "xgboost": Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "model",
                    XGBRegressor(
                        n_estimators=250,
                        max_depth=6,
                        learning_rate=0.08,
                        subsample=0.9,
                        colsample_bytree=0.9,
                        random_state=42,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
    }


def train_delivery_time_model(
    dataset_path: Path,
    models_dir: Path,
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict:
    df = pd.read_csv(dataset_path)
    x, y = prepare_delivery_dataset(df)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=test_size, random_state=random_state
    )

    results: dict[str, dict] = {}
    fitted: dict[str, Pipeline] = {}

    for name, pipeline in build_candidates().items():
        pipeline.fit(x_train, y_train)
        preds = pipeline.predict(x_test)
        metrics = evaluate_regressor(y_test, preds)
        results[name] = metrics
        fitted[name] = pipeline
        print(
            f"[{name}] mae={metrics['mae']:.2f} rmse={metrics['rmse']:.2f} r2={metrics['r2']:.3f}"
        )

    best_name = select_best_regressor(results)
    best_pipeline = fitted[best_name]
    models_dir.mkdir(parents=True, exist_ok=True)
    model_path = models_dir / "delivery_time_model.pkl"
    joblib.dump(best_pipeline, model_path)

    metadata = {
        "delivery_time_model_version": "1.0.0",
        "delivery_time_best_algorithm": best_name,
        "delivery_time_metrics": results[best_name],
        "delivery_time_all_results": results,
        "dataset": str(dataset_path),
        "dataset_type": "SYNTHETIC_DEV",
        "samples": len(df),
    }
    _save_metadata(models_dir, metadata)
    print(f"Best delivery time model: {best_name} -> {model_path}")
    return metadata


def _save_metadata(models_dir: Path, patch: dict) -> None:
    meta_path = models_dir / "model_metadata.json"
    existing = {}
    if meta_path.exists():
        existing = json.loads(meta_path.read_text(encoding="utf-8"))
    existing.update(patch)
    meta_path.write_text(json.dumps(existing, indent=2), encoding="utf-8")


def main() -> None:
    settings = get_settings()
    parser = argparse.ArgumentParser(description="Train SmartTask delivery time model")
    parser.add_argument(
        "--dataset",
        type=Path,
        default=Path("data/raw/smarttask_delivery_dataset.csv"),
    )
    parser.add_argument("--models-dir", type=Path, default=settings.models_dir)
    args = parser.parse_args()

    if not args.dataset.exists():
        raise FileNotFoundError(
            f"Dataset not found: {args.dataset}. Run: python -m app.ml.generate_dataset"
        )

    train_delivery_time_model(args.dataset, args.models_dir)


if __name__ == "__main__":
    main()
