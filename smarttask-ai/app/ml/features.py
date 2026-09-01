"""Shared feature definitions aligned with SmartTask domain and prediction API."""

from __future__ import annotations

DELAY_FEATURE_COLUMNS = [
    "distance_km",
    "estimated_duration",
    "deadline_minutes",
    "priority_score",
    "hour",
    "day_of_week",
    "driver_current_tasks",
    "driver_delay_rate",
    "traffic_score",
]

DELIVERY_TIME_FEATURE_COLUMNS = [
    "distance_km",
    "estimated_duration",
    "priority_score",
    "hour",
    "day_of_week",
    "driver_current_tasks",
    "driver_performance",
    "traffic_score",
]

DELIVERY_SUCCESS_FEATURE_COLUMNS = [
    "address_completeness_score",
    "distance_km",
    "estimated_duration",
    "deadline_minutes",
    "priority_score",
    "hour",
    "day_of_week",
    "client_incident_rate",
    "client_failed_delivery_rate",
    "traffic_score",
    "product_fragile_score",
    "driver_current_tasks",
    "driver_delay_rate",
]

DELAY_TARGET = "delayed"
DELIVERY_TARGET = "actual_delivery_time"
DELIVERY_SUCCESS_TARGET = "delivery_success"
