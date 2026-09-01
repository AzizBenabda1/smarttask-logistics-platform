"""Model evaluation utilities."""

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    recall_score,
    roc_auc_score,
    r2_score,
)


def evaluate_classifier(y_true, y_pred, y_proba=None) -> dict[str, Any]:
    metrics: dict[str, Any] = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
    }
    if y_proba is not None and len(np.unique(y_true)) > 1:
        metrics["roc_auc"] = float(roc_auc_score(y_true, y_proba))
    return metrics


def evaluate_regressor(y_true, y_pred) -> dict[str, Any]:
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": rmse,
        "r2": float(r2_score(y_true, y_pred)),
    }


def select_best_classifier(results: dict[str, dict[str, Any]]) -> str:
    return max(
        results,
        key=lambda name: (
            results[name].get("roc_auc", 0),
            results[name]["f1"],
            results[name]["accuracy"],
        ),
    )


def select_best_regressor(results: dict[str, dict[str, Any]]) -> str:
    return min(results, key=lambda name: (results[name]["rmse"], -results[name]["r2"]))
