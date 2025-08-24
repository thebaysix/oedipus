from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Environment
    OEDIPUS_ENV: str = "prod"

    # Postgres
    POSTGRES_USER: str = "oedipus"
    POSTGRES_PASSWORD: str = "oedipus_password"
    POSTGRES_DB: str = "oedipus"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"

    # Database
    SQLALCHEMY_DATABASE_URL: str = None  # will be set in __init__

    # Redis / Celery
    REDIS_URL: Optional[str] = None
    celery_broker_url: Optional[str] = None
    celery_result_backend: Optional[str] = None

    # Application
    debug: bool = True
    secret_key: str = "your-secret-key-here"

    class Config:
        env_file = ".env"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Build SQLAlchemy URL
        self.SQLALCHEMY_DATABASE_URL = (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

        # Configure Redis/Celery only if not local
        if self.OEDIPUS_ENV != "local":
            self.REDIS_URL = self.REDIS_URL or "redis://localhost:6379/0"
            self.celery_broker_url = self.REDIS_URL
            self.celery_result_backend = self.REDIS_URL
        else:
            self.REDIS_URL = None
            self.celery_broker_url = None
            self.celery_result_backend = None


settings = Settings()
