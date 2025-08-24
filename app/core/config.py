from pydantic_settings import BaseSettings
from pydantic import field_validator, Field
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
    SQLALCHEMY_DATABASE_URL: str = Field(default="")  # will be built dynamically

    # Redis / Celery
    REDIS_URL: Optional[str] = None
    celery_broker_url: Optional[str] = None
    celery_result_backend: Optional[str] = None

    # Application
    debug: bool = True
    secret_key: str = "your-secret-key-here"

    class Config:
        env_file = ".env"

    # Use Pydantic v2 validator to build SQLAlchemy URL after init
    @field_validator("SQLALCHEMY_DATABASE_URL", mode="before")
    def build_sqlalchemy_url(cls, v, info):
        return (
            f"postgresql://{info.data.get('POSTGRES_USER')}:{info.data.get('POSTGRES_PASSWORD')}@"
            f"{info.data.get('POSTGRES_HOST')}:{info.data.get('POSTGRES_PORT')}/{info.data.get('POSTGRES_DB')}"
        )

    @field_validator("REDIS_URL", mode="before")
    def configure_redis(cls, v, info):
        if info.data.get("OEDIPUS_ENV") == "local":
            return None
        return v or "redis://localhost:6379/0"

    @field_validator("celery_broker_url", "celery_result_backend", mode="before")
    def configure_celery(cls, v, info):
        if info.data.get("OEDIPUS_ENV") == "local":
            return None
        return info.data.get("REDIS_URL") or v


settings = Settings()
