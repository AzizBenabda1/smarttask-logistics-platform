"""Run full ML training pipeline: dataset -> delay model -> delivery time model."""

from __future__ import annotations

from pathlib import Path

from app.config import get_settings
from app.ml.generate_dataset import generate_synthetic_dataset
from app.ml.train_delay import train_delay_model
from app.ml.train_delivery_success import train_delivery_success_model
from app.ml.train_delivery_time import train_delivery_time_model


def main() -> None:
    settings = get_settings()
    dataset_path = Path("data/raw/smarttask_delivery_dataset.csv")
    dataset_path.parent.mkdir(parents=True, exist_ok=True)

    if not dataset_path.exists():
        print("Generating synthetic dataset...")
        generate_synthetic_dataset().to_csv(dataset_path, index=False)

    print("Training delay model...")
    delay_meta = train_delay_model(dataset_path, settings.models_dir)
    print("Training delivery time model...")
    delivery_meta = train_delivery_time_model(dataset_path, settings.models_dir)
    print("Training delivery success model...")
    success_meta = train_delivery_success_model(dataset_path, settings.models_dir)

    print("\n=== Training complete ===")
    print(f"Delay model: {delay_meta['delay_best_algorithm']} "
          f"(F1={delay_meta['delay_metrics']['f1']:.3f})")
    print(
        f"Delivery time model: {delivery_meta['delivery_time_best_algorithm']} "
        f"(MAE={delivery_meta['delivery_time_metrics']['mae']:.1f} min)"
    )
    print(
        f"Delivery success model: {success_meta['delivery_success_best_algorithm']} "
        f"(F1={success_meta['delivery_success_metrics']['f1']:.3f})"
    )


if __name__ == "__main__":
    main()
