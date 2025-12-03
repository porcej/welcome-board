import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or f"sqlite:///{BASE_DIR}/instance/app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", str(BASE_DIR / "app" / "static" / "uploads"))
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    TIMEZONE = os.getenv("TIMEZONE", "UTC")
    WEATHER_TTL_MINUTES = int(os.getenv("WEATHER_TTL_MINUTES", "60"))


class DevConfig(BaseConfig):
    DEBUG = True


class ProdConfig(BaseConfig):
    DEBUG = False


def get_config():
    env = os.getenv("FLASK_ENV", "development").lower()
    if env == "production":
        return ProdConfig
    return DevConfig


