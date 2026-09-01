from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/metrics")
def get_metrics(request: Request) -> dict:
    return request.app.state.model_service.get_metrics()
