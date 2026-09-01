from fastapi import APIRouter, HTTPException, Request, status

from app.schemas.prediction_schema import (
    AnomalyDetectionRequest,
    AnomalyDetectionResponse,
    DelayPredictionRequest,
    DelayPredictionResponse,
    DeliverySuccessPredictionRequest,
    DeliverySuccessPredictionResponse,
    DeliveryTimePredictionRequest,
    DeliveryTimePredictionResponse,
)
from app.schemas.recommendation_schema import (
    DriverRecommendationRequest,
    DriverRecommendationResponse,
    TaskPrioritizationRequest,
    TaskPrioritizationResponse,
)
from app.services.model_service import ModelNotLoadedError

router = APIRouter()


@router.post("/predict/delay", response_model=DelayPredictionResponse)
def predict_delay(payload: DelayPredictionRequest, request: Request) -> DelayPredictionResponse:
    from app.services.prediction_service import PredictionService

    service = PredictionService(request.app.state.model_service)
    try:
        return service.predict_delay(payload)
    except ModelNotLoadedError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc


@router.post("/predict/delivery-time", response_model=DeliveryTimePredictionResponse)
def predict_delivery_time(
    payload: DeliveryTimePredictionRequest, request: Request
) -> DeliveryTimePredictionResponse:
    from app.services.prediction_service import PredictionService

    service = PredictionService(request.app.state.model_service)
    try:
        return service.predict_delivery_time(payload)
    except ModelNotLoadedError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc


@router.post("/predict/delivery-success", response_model=DeliverySuccessPredictionResponse)
def predict_delivery_success(
    payload: DeliverySuccessPredictionRequest, request: Request
) -> DeliverySuccessPredictionResponse:
    from app.services.prediction_service import PredictionService

    service = PredictionService(request.app.state.model_service)
    return service.predict_delivery_success(payload)


@router.post("/detect/anomaly", response_model=AnomalyDetectionResponse)
def detect_anomaly(
    payload: AnomalyDetectionRequest, request: Request
) -> AnomalyDetectionResponse:
    from app.services.analytics_service import AnalyticsService

    service = AnalyticsService(request.app.state.model_service)
    return service.detect_anomaly(payload)
