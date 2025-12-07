import json
from typing import List, Any

from pydantic_settings import BaseSettings, SettingsConfigDict


def _parse_env_var(field_name: str, raw_value: Any):
    if field_name == "ALLOWED_ORIGINS":
        if raw_value is None or raw_value == "":
            return []
        if isinstance(raw_value, str):
            return [origin.strip() for origin in raw_value.split(",") if origin.strip()]
    return raw_value


def _safe_json_loads(value: str):
    try:
        return json.loads(value)
    except Exception:
        return value


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        parse_env_var=_parse_env_var,
        json_loads=_safe_json_loads,
    )

    PROJECT_NAME: str = "Prephoria"
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Override from Render env variable
    DATABASE_URL: str = ""

    # Render will pass a string "a,b,c" → we split to list
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]


settings = Settings()
