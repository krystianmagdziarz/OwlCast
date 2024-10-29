from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "StatCollector"
    API_V1_STR: str = "/api/v1"
    
    # ClickHouse settings
    CLICKHOUSE_HOST: str
    CLICKHOUSE_PORT: int = 8123
    CLICKHOUSE_DB: str
    CLICKHOUSE_USER: str
    CLICKHOUSE_PASSWORD: str
    
    # Redis settings
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    
    # Security
    API_KEY_HEADER: str = "X-API-Key"
    SECRET_KEY: str
    
    # Rate limiting
    RATE_LIMIT_PER_SECOND: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
