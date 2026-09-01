from fastapi import APIRouter

from app.schemas.route_schema import RouteOptimizationRequest, RouteOptimizationResponse
from app.services.route_optimization_service import RouteOptimizationService

router = APIRouter()
_service = RouteOptimizationService()


@router.post("/optimize/route", response_model=RouteOptimizationResponse)
def optimize_route(payload: RouteOptimizationRequest) -> RouteOptimizationResponse:
    return _service.optimize(payload)
