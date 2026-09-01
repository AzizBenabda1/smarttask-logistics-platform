from pydantic import BaseModel, Field

from app.schemas.prediction_schema import PriorityLevel


class RouteMissionStop(BaseModel):
    task_id: int = Field(..., alias="taskId", ge=1)
    title: str = ""
    zone: str | None = None
    delivery_address: str = Field("", alias="deliveryAddress")
    priority: PriorityLevel = PriorityLevel.MEDIUM
    deadline_minutes: int = Field(60, alias="deadlineMinutes", ge=0)
    estimated_minutes: int = Field(30, alias="estimatedMinutes", ge=1)

    model_config = {"populate_by_name": True}


class RouteOptimizationRequest(BaseModel):
    driver_id: int = Field(..., alias="driverId", ge=1)
    missions: list[RouteMissionStop] = Field(..., min_length=1)

    model_config = {"populate_by_name": True}


class RouteStopResult(BaseModel):
    order: int
    task_id: int = Field(..., alias="taskId")
    title: str
    zone: str | None = None
    delivery_address: str = Field("", alias="deliveryAddress")
    priority: PriorityLevel
    estimated_minutes: int = Field(..., alias="estimatedMinutes")
    urgency_label: str = Field("NORMAL", alias="urgencyLabel")

    model_config = {"populate_by_name": True}


class RouteOptimizationResponse(BaseModel):
    driver_id: int = Field(..., alias="driverId")
    stops: list[RouteStopResult]
    manual_total_minutes: int = Field(..., alias="manualTotalMinutes")
    optimized_total_minutes: int = Field(..., alias="optimizedTotalMinutes")
    estimated_time_saved_minutes: int = Field(..., alias="estimatedTimeSavedMinutes")
    scoring_method: str = Field("priority_deadline_greedy", alias="scoringMethod")
    summary: str

    model_config = {"populate_by_name": True}
