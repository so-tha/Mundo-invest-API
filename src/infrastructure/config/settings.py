from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "Mundo Invest API"
    environment: str = "development"
    debug: bool = True
    database_url: str = "postgresql+asyncpg://postgres:postgres@db:5432/mundo_invest"
    
    pipefy_api_url: str = "https://api.pipefy.com/graphql"
    pipefy_api_token: Optional[str] = None
    pipefy_pipe_id: Optional[str] = None
    
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore" 


settings = Settings()