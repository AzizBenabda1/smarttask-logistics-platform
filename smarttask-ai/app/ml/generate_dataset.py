"""
Generate a SYNTHETIC development dataset for SmartTask AI.

IMPORTANT: This data is for prototyping only — not real SmartTask production data.
Replace with exported PostgreSQL data when sufficient history exists.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

PRIORITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
TRAFFIC_LEVELS = ["LOW", "MEDIUM", "HIGH"]
ZONES = ["Tunis", "Ariana", "Ben Arous", "Manouba", "Sousse"]


def generate_synthetic_dataset(n_samples: int = 3000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    distance_km = rng.uniform(1.0, 35.0, n_samples)
    estimated_duration = np.clip(
        distance_km * rng.uniform(1.8, 4.2, n_samples) + rng.normal(0, 4, n_samples),
        10,
        150,
    ).astype(int)
    slack = rng.integers(-15, 45, n_samples)
    deadline_minutes = np.clip(estimated_duration + slack, 15, 200).astype(int)

    priority = rng.choice(PRIORITIES, n_samples, p=[0.15, 0.35, 0.35, 0.15])
    hour = rng.integers(7, 22, n_samples)
    day_of_week = rng.integers(0, 7, n_samples)
    driver_current_tasks = rng.integers(0, 8, n_samples)
    driver_delay_rate = np.clip(
        rng.beta(2, 10, n_samples) + driver_current_tasks * 0.025,
        0,
        0.95,
    )
    driver_performance = np.clip(1.0 - driver_delay_rate + rng.normal(0, 0.08, n_samples), 0.35, 1.0)
    traffic_level = rng.choice(TRAFFIC_LEVELS, n_samples, p=[0.35, 0.4, 0.25])
    zone = rng.choice(ZONES, n_samples)

    traffic_mult = np.array([1.0 if t == "LOW" else 1.12 if t == "MEDIUM" else 1.35 for t in traffic_level])
    rush_hour = ((hour >= 8) & (hour <= 10)) | ((hour >= 17) & (hour <= 19))
    rush_bonus = np.where(rush_hour, rng.uniform(5, 15, n_samples), 0)

    actual_delivery_time = np.clip(
        estimated_duration * traffic_mult
        + driver_current_tasks * rng.uniform(2, 5, n_samples)
        + rush_bonus
        + rng.normal(0, 6, n_samples),
        8,
        240,
    ).astype(int)

    priority_score = np.array([PRIORITIES.index(p) for p in priority])
    deadline_pressure = estimated_duration / np.maximum(deadline_minutes, 1)
    traffic_score = np.array([TRAFFIC_LEVELS.index(t) for t in traffic_level])

    address_completeness_score = np.clip(
        rng.uniform(0.35, 1.0, n_samples) - np.where(distance_km > 25, 0.15, 0),
        0.2,
        1.0,
    )
    client_incident_rate = np.clip(rng.beta(1.2, 9, n_samples), 0, 0.85)
    client_failed_delivery_rate = np.clip(
        client_incident_rate * 0.55 + rng.uniform(0, 0.12, n_samples),
        0,
        0.9,
    )
    product_fragile_score = rng.choice([0, 1], n_samples, p=[0.68, 0.32]).astype(float)

    delay_logit = (
        2.2 * (deadline_pressure - 0.75)
        + 0.9 * traffic_score
        + 0.35 * driver_current_tasks
        + 2.5 * driver_delay_rate
        + 0.25 * priority_score
        + rng.normal(0, 0.35, n_samples)
    )
    delayed_prob = 1 / (1 + np.exp(-delay_logit))
    delayed = (delayed_prob > 0.5).astype(int)
    # Ensure some delayed cases also exceed deadline
    delayed = np.where(actual_delivery_time > deadline_minutes, 1, delayed)

    success_logit = (
        2.2 * address_completeness_score
        - 1.6 * client_incident_rate
        - 2.0 * client_failed_delivery_rate
        - 0.7 * traffic_score
        - 0.25 * priority_score
        - 0.35 * driver_current_tasks
        - 0.45 * driver_delay_rate
        - 1.8 * delayed
        - 0.15 * product_fragile_score
        + rng.normal(0, 0.28, n_samples)
    )
    delivery_success = (1 / (1 + np.exp(-success_logit)) > 0.52).astype(int)

    return pd.DataFrame(
        {
            "task_id": np.arange(1, n_samples + 1),
            "distance_km": np.round(distance_km, 2),
            "estimated_duration": estimated_duration,
            "deadline_minutes": deadline_minutes,
            "priority": priority,
            "hour": hour,
            "day_of_week": day_of_week,
            "driver_current_tasks": driver_current_tasks,
            "driver_delay_rate": np.round(driver_delay_rate, 4),
            "driver_performance": np.round(driver_performance, 4),
            "traffic_level": traffic_level,
            "zone": zone,
            "address_completeness_score": np.round(address_completeness_score, 4),
            "client_incident_rate": np.round(client_incident_rate, 4),
            "client_failed_delivery_rate": np.round(client_failed_delivery_rate, 4),
            "product_fragile_score": product_fragile_score,
            "actual_delivery_time": actual_delivery_time,
            "delayed": delayed,
            "delivery_success": delivery_success,
            "dataset_type": "SYNTHETIC_DEV",
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic SmartTask delivery dataset")
    parser.add_argument("--samples", type=int, default=3000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/raw/smarttask_delivery_dataset.csv"),
    )
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    df = generate_synthetic_dataset(args.samples, args.seed)
    df.to_csv(args.output, index=False)
    print(f"Synthetic dataset saved: {args.output} ({len(df)} rows)")
    print(f"Delayed rate: {df['delayed'].mean():.2%}")


if __name__ == "__main__":
    main()
