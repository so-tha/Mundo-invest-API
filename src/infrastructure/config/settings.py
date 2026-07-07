from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )
    app_name: str = "Mundo Invest API"
    environment: str = "development"
    debug: bool = True
    database_url: str = "postgresql+asyncpg://postgres:postgres@db:5432/mundo_invest"

    pipefy_api_url: str = "https://api.pipefy.com/graphql"
    pipefy_api_token: Optional[str] = None
    pipefy_pipe_id: Optional[str] = None

    api_key: Optional[str] = None
    cors_origins: str = "*"

    host: str = "0.0.0.0"
    port: int = 8000


settings = Settings()