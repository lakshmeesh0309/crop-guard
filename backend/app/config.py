from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    MONGO_URL: str = "mongodb://localhost:27017"
    MONGO_DB: str = "cropguard_db"

    SECRET_KEY: str = "cropguard-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080

    APP_ENV: str = "development"
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    UPLOAD_DIR: str = "./uploads"
    OPENWEATHER_API_KEY: str = ""

    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str = ""

    # Kaggle credentials for hybrid model training
    KAGGLE_USERNAME: str = ""
    KAGGLE_KEY: str = ""

    DEFAULT_LAT: float = 17.6868
    DEFAULT_LON: float = 83.2185
    DEFAULT_CITY: str = "Visakhapatnam"
    DEFAULT_LANGUAGE: str = "en"

    @property
    def origins_list(self) -> List[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"

settings = Settings()
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Startup security validator
_KNOWN_DEFAULTS = {"cropguard-secret", "cropguard-super-secret-jwt-2026"}
if settings.SECRET_KEY in _KNOWN_DEFAULTS and settings.APP_ENV == "production":
    raise RuntimeError(
        "FATAL: SECRET_KEY is set to a known default. "
        "Set a strong random key in .env before running in production."
    )
