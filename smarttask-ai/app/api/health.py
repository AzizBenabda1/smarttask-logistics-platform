from fastapi import APIRouter, Request

from app import __version__

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    return {
        "status": "UP",
        "service": "smarttask-ai",
        "version": __version__,
    }


@router.get("/model/status")
def model_status(request: Request) -> dict:
    model_service = request.app.state.model_service
    return {
        "delayModel": model_service.model_state(model_service.delay_model).value,
        "deliveryTimeModel": model_service.model_state(
            model_service.delivery_time_model
        ).value,
        "deliverySuccessModel": model_service.model_state(
            model_service.delivery_success_model
        ).value,
        "priorityModel": model_service.model_state(model_service.priority_model).value,
        "modelsPath": str(model_service.models_dir),
    }
