from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = "development"
    ai_service_host: str = "0.0.0.0"
    ai_service_port: int = 8000
    spring_boot_url: str = "http://localhost:9090"
    model_path: str = "./app/models"
    delay_model_version: str = "0.0.0"
    delivery_time_model_version: str = "0.0.0"
    delivery_success_model_version: str = "0.0.0"
    priority_model_version: str = "0.0.0"
    log_level: str = "INFO"

    @property
    def models_dir(self) -> Path:
        return Path(self.model_path).resolve()


@lru_cache
def get_settings() -> Settings:
    return Settings()
