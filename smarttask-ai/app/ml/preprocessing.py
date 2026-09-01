"""Feature engineering and dataset preparation."""

from __future__ import annotations

import pandas as pd

from app.ml.features import (
    DELAY_FEATURE_COLUMNS,
    DELAY_TARGET,
    DELIVERY_SUCCESS_FEATURE_COLUMNS,
    DELIVERY_SUCCESS_TARGET,
    DELIVERY_TARGET,
    DELIVERY_TIME_FEATURE_COLUMNS,
)

PRIORITY_MAP = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
TRAFFIC_MAP = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
TRAFFIC_MULTIPLIER = {"LOW": 1.0, "MEDIUM": 1.12, "HIGH": 1.35}


def encode_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    """Encode priority and traffic columns to numeric scores."""
    out = df.copy()
    if "priority" in out.columns:
        out["priority_score"] = out["priority"].map(PRIORITY_MAP).fillna(1).astype(int)
    if "traffic_level" in out.columns:
        out["traffic_score"] = out["traffic_level"].map(TRAFFIC_MAP).fillna(1).astype(int)
    return out


def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add computed columns used by ML pipelines."""
    out = encode_categoricals(df)
    if {"estimated_duration", "deadline_minutes"}.issubset(out.columns):
        out["deadline_pressure"] = out["estimated_duration"] / out["deadline_minutes"].clip(
            lower=1
        )
    if {"actual_delivery_time", "estimated_duration"}.issubset(out.columns):
        out["delivery_ratio"] = out["actual_delivery_time"] / out["estimated_duration"].clip(
            lower=1
        )
    return out


def prepare_delay_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    enriched = add_derived_features(df)
    x = enriched[DELAY_FEATURE_COLUMNS].astype(float)
    y = enriched[DELAY_TARGET].astype(int)
    return x, y


def prepare_delivery_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    enriched = add_derived_features(df)
    x = enriched[DELIVERY_TIME_FEATURE_COLUMNS].astype(float)
    y = enriched[DELIVERY_TARGET].astype(float)
    return x, y


def prepare_delivery_success_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    enriched = add_derived_features(df)
    x = enriched[DELIVERY_SUCCESS_FEATURE_COLUMNS].astype(float)
    y = enriched[DELIVERY_SUCCESS_TARGET].astype(int)
    return x, y
