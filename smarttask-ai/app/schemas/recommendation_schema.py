from pydantic import BaseModel, Field

from app.schemas.prediction_schema import PriorityLevel


class DriverCandidate(BaseModel):
    id: int = Field(..., ge=1)
    distance_from_client: float = Field(..., alias="distanceFromClient", ge=0)
    current_tasks: int = Field(..., alias="currentTasks", ge=0)
    performance_score: float = Field(..., alias="performanceScore", ge=0, le=1)
    delay_rate: float = Field(..., alias="delayRate", ge=0, le=1)
    available: bool = True

    model_config = {"populate_by_name": True}


class DriverRecommendationRequest(BaseModel):
    task_id: int = Field(..., alias="taskId", ge=1)
    distance_km: float = Field(..., alias="distanceKm", ge=0)
    priority: PriorityLevel = PriorityLevel.MEDIUM
    deadline_minutes: int = Field(..., alias="deadlineMinutes", ge=1)
    drivers: list[DriverCandidate] = Field(..., min_length=1)

    model_config = {"populate_by_name": True}


class DriverRecommendationResponse(BaseModel):
    task_id: int = Field(..., alias="taskId")
    recommended_driver_id: int = Field(..., alias="recommendedDriverId")
    score: int = Field(..., ge=0, le=100)
    reasons: list[str]
    scoring_method: str = Field("explainable_scoring", alias="scoringMethod")
    model_version: str = Field("1.0.0", alias="modelVersion")

    model_config = {"populate_by_name": True}


class TaskPrioritizationRequest(BaseModel):
    task_id: int = Field(..., alias="taskId", ge=1)
    deadline_minutes: int = Field(..., alias="deadlineMinutes", ge=0)
    priority: PriorityLevel = PriorityLevel.MEDIUM
    delay_probability: float = Field(0.0, alias="delayProbability", ge=0, le=1)
    distance_km: float = Field(..., alias="distanceKm", ge=0)
    estimated_duration: int = Field(..., alias="estimatedDuration", ge=1)
    driver_current_tasks: int = Field(0, alias="driverCurrentTasks", ge=0)

    model_config = {"populate_by_name": True}


class TaskPrioritizationResponse(BaseModel):
    task_id: int = Field(..., alias="taskId")
    priority_score: int = Field(..., alias="priorityScore", ge=0, le=100)
    recommended_priority: PriorityLevel = Field(..., alias="recommendedPriority")
    reason: str
    scoring_method: str = Field("explainable_scoring", alias="scoringMethod")

    model_config = {"populate_by_name": True}
