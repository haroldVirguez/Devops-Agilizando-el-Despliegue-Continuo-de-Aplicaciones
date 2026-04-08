import os


def _normalize_database_url(url):
    """Normalize Heroku-style ``postgres://`` to ``postgresql://`` for SQLAlchemy + psycopg2."""
    if not url or url.startswith("sqlite"):
        return url
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    JWT_ALGORITHM = "HS256"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-flask-secret-key")
    _db_url = os.environ.get("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = _normalize_database_url(_db_url) or "sqlite:///dev.db"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret-change-me")


class ProductionConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.environ.get("JWT_SECRET_KEY", "")
    _db_url = os.environ.get("DATABASE_URL", "")
    SQLALCHEMY_DATABASE_URI = (
        _normalize_database_url(_db_url) if _db_url else ""
    )
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
