from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Any


def _parse_env_var(field_name: str, raw_value: Any):
    if field_name == "ALLOWED_ORIGINS":
        if not raw_value:
            return None
        if isinstance(raw_value, str):
            return [origin.strip() for origin in raw_value.split(",") if origin.strip()]
    return raw_value


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        parse_env_var=_parse_env_var,
    )

    PROJECT_NAME: str = "Prephoria"
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    DATABASE_URL: str = "postgresql+psycopg2://macbook:Aa123456.@localhost:5432/prephoria_db"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]


settings = Settings()
