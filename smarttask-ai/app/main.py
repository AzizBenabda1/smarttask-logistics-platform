import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api import analytics, chat, health, prediction, recommendation, route
from app.config import get_settings
from app.services.model_service import ModelService

logging.basicConfig(
    level=get_settings().log_level,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger("smarttask-ai")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger.info("SmartTask AI service starting (env=%s)", settings.environment)
    model_service = ModelService(settings)
    model_service.load_all()
    app.state.model_service = model_service
    app.state.settings = settings
    logger.info("Model loading complete")
    yield
    logger.info("SmartTask AI service shutting down")


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="SmartTask AI",
        description="Microservice ML pour prédictions et recommandations logistiques SmartTask",
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.spring_boot_url.rstrip("/"), "http://localhost:9090"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix="/api/ai", tags=["Health"])
    app.include_router(prediction.router, prefix="/api/ai", tags=["Prediction"])
    app.include_router(recommendation.router, prefix="/api/ai", tags=["Recommendation"])
    app.include_router(chat.router, prefix="/api/ai", tags=["Chat"])
    app.include_router(analytics.router, prefix="/api/ai", tags=["Analytics"])
    app.include_router(route.router, prefix="/api/ai", tags=["Route"])

    return app


app = create_app()
