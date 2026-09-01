from fastapi import APIRouter, Request

from app.schemas.recommendation_schema import (
    DriverRecommendationRequest,
    DriverRecommendationResponse,
    TaskPrioritizationRequest,
    TaskPrioritizationResponse,
)
from app.services.recommendation_service import RecommendationService

router = APIRouter()


@router.post("/recommend/driver", response_model=DriverRecommendationResponse)
def recommend_driver(
    payload: DriverRecommendationRequest, request: Request
) -> DriverRecommendationResponse:
    service = RecommendationService(request.app.state.model_service)
    return service.recommend_driver(payload)


@router.post("/prioritize/task", response_model=TaskPrioritizationResponse)
def prioritize_task(
    payload: TaskPrioritizationRequest, request: Request
) -> TaskPrioritizationResponse:
    service = RecommendationService(request.app.state.model_service)
    return service.prioritize_task(payload)
