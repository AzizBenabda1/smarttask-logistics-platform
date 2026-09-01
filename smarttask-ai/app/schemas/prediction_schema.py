from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class PriorityLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class TrafficLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class DelayPredictionRequest(BaseModel):
    task_id: int = Field(..., alias="taskId", ge=1)
    distance_km: float = Field(..., alias="distanceKm", ge=0)
    estimated_duration: int = Field(..., alias="estimatedDuration", ge=1)
    deadline_minutes: int = Field(..., alias="deadlineMinutes", ge=1)
    priority: PriorityLevel = PriorityLevel.MEDIUM
    hour: int = Field(..., ge=0, le=23)
    day_of_week: int = Field(..., alias="dayOfWeek", ge=0, le=6)
    driver_current_tasks: int = Field(0, alias="driverCurrentTasks", ge=0)
    driver_delay_rate: float = Field(0.0, alias="driverDelayRate", ge=0, le=1)
    traffic_level: TrafficLevel = TrafficLevel.MEDIUM

    model_config = {"populate_by_name": True}


class DelayPredictionResponse(BaseModel):
    task_id: int = Field(..., alias="taskId")
    delay_probability: float = Field(..., alias="delayProbability", ge=0, le=1)
    risk_level: RiskLevel = Field(..., alias="riskLevel")
    model_version: str = Field(..., alias="modelVersion")
    explanation: list[str]

    model_config = {"populate_by_name": True}


class DeliveryTimePredictionRequest(BaseModel):
    task_id: int = Field(..., alias="taskId", ge=1)
    distance_km: float = Field(..., alias="distanceKm", ge=0)
    estimated_duration: int = Field(..., alias="estimatedDuration", ge=1)
    priority: PriorityLevel = PriorityLevel.MEDIUM
    hour: int = Field(..., ge=0, le=23)
    day_of_week: int = Field(..., alias="dayOfWeek", ge=0, le=6)
    driver_current_tasks: int = Field(0, alias="driverCurrentTasks", ge=0)
    driver_performance: float = Field(0.8, alias="driverPerformance", ge=0, le=1)
    traffic_level: TrafficLevel = TrafficLevel.MEDIUM
    zone: str | None = None

    model_config = {"populate_by_name": True}


class DeliveryTimePredictionResponse(BaseModel):
    task_id: int = Field(..., alias="taskId")
    estimated_delivery_time: int = Field(..., alias="estimatedDeliveryTime", ge=1)
    unit: Literal["minutes"] = "minutes"
    model_version: str = Field(..., alias="modelVersion")
    explanation: list[str]

    model_config = {"populate_by_name": True}


class AnomalyDetectionRequest(BaseModel):
    task_id: int | None = Field(None, alias="taskId")
    driver_id: int | None = Field(None, alias="driverId")
    actual_delivery_time: float | None = Field(None, alias="actualDeliveryTime", ge=0)
    expected_delivery_time: float | None = Field(None, alias="expectedDeliveryTime", ge=0)
    driver_current_tasks: int | None = Field(None, alias="driverCurrentTasks", ge=0)
    incidents_last_7_days: int | None = Field(None, alias="incidentsLast7Days", ge=0)
    zone_delay_rate: float | None = Field(None, alias="zoneDelayRate", ge=0, le=1)

    model_config = {"populate_by_name": True}


class AnomalyDetectionResponse(BaseModel):
    anomaly: bool
    score: float = Field(..., ge=0, le=1)
    reason: str
    explanation: list[str]


class DeliverySuccessPredictionRequest(BaseModel):
    task_id: int | None = Field(None, alias="taskId", ge=1)
    reference_id: str | None = Field(None, alias="referenceId")
    client_id: int | None = Field(None, alias="clientId", ge=1)
    delivery_address: str = Field(..., alias="deliveryAddress", min_length=3)
    distance_km: float = Field(..., alias="distanceKm", ge=0)
    estimated_duration: int = Field(..., alias="estimatedDuration", ge=1)
    deadline_minutes: int = Field(..., alias="deadlineMinutes", ge=1)
    priority: PriorityLevel = PriorityLevel.MEDIUM
    hour: int = Field(..., ge=0, le=23)
    day_of_week: int = Field(..., alias="dayOfWeek", ge=0, le=6)
    address_completeness_score: float = Field(
        0.7, alias="addressCompletenessScore", ge=0, le=1
    )
    client_incident_rate: float = Field(0.05, alias="clientIncidentRate", ge=0, le=1)
    client_failed_delivery_rate: float = Field(
        0.05, alias="clientFailedDeliveryRate", ge=0, le=1
    )
    product_fragile_score: float = Field(0.0, alias="productFragileScore", ge=0, le=1)
    driver_current_tasks: int = Field(0, alias="driverCurrentTasks", ge=0)
    driver_delay_rate: float = Field(0.1, alias="driverDelayRate", ge=0, le=1)
    traffic_level: TrafficLevel = TrafficLevel.MEDIUM

    model_config = {"populate_by_name": True}


class DeliverySuccessPredictionResponse(BaseModel):
    task_id: int | None = Field(None, alias="taskId")
    reference_id: str | None = Field(None, alias="referenceId")
    success_probability: float = Field(..., alias="successProbability", ge=0, le=1)
    risk_level: RiskLevel = Field(..., alias="riskLevel")
    factors: list[str]
    suggested_actions: list[str] = Field(..., alias="suggestedActions")
    model_version: str = Field(..., alias="modelVersion")
    explanation: list[str]
    rule_based: bool = Field(False, alias="ruleBased")

    model_config = {"populate_by_name": True}
