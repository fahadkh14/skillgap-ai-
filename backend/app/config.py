import os
from datetime import timedelta


class Config:
    """Application configuration loaded from environment variables."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret-change-me")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)
    JWT_TOKEN_LOCATION = ["headers"]

    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/skillgap")
    MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "skillgap")

    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:8050").split(",")

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max upload
    ALLOWED_RESUME_EXTENSIONS = {"pdf", "docx"}
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "/tmp/skillgap_uploads")

    FLASK_ENV = os.environ.get("FLASK_ENV", "production")
    DEBUG = FLASK_ENV == "development"
