from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


def _read_secret(name: str) -> str | None:
    path = Path(f"/run/secrets/{name}")
    return path.read_text().strip() if path.exists() else None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    app_env: str = "development"
    debug: bool = False

    # Database — ref: spec.md → PostgreSQL, asyncpg
    database_url: str = "postgresql+asyncpg://myapp:devpassword@localhost:5432/myapp_dev"

    # RabbitMQ — ref: spec.md → RabbitMQ broker
    rabbitmq_user: str = "myapp"
    rabbitmq_password: str = "devpassword"
    rabbitmq_host: str = "localhost"

    @property
    def rabbitmq_url(self) -> str:
        password = _read_secret("rabbitmq_password") or self.rabbitmq_password
        return f"amqp://{self.rabbitmq_user}:{password}@{self.rabbitmq_host}:5672//"

    # S3 — ref: spec.md → S3-Compatible Storage
    s3_endpoint_url: str = "http://localhost:9000"
    s3_public_url: str = "http://localhost:9000"
    s3_region: str = "us-east-1"
    s3_bucket_name: str = "myapp-dev"
    s3_addressing_style: str = "path"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"

    # Email (SMTP) — dev: Mailpit :1025, prod: Mailgun/SendGrid/SES SMTP
    smtp_host: str = "localhost"
    smtp_port: int = 1025
    smtp_tls: bool = False
    smtp_user: str = ""
    smtp_password: str = ""
    email_from: str = "noreply@myapp-dev.local"

    # Auth — ref: spec.md → JWT, HTTP-only cookies
    jwt_secret: str = "dev-jwt-secret-change-in-production-minimum-64-chars-xxxxxxxxxxxxx"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    # Frontend URL — используется для ссылок в письмах
    frontend_url: str = "http://localhost:3000"

    # CORS — ref: spec.md → CORS/Cookie hardening
    allowed_origins: list[str] = ["http://localhost:3000"]

    # Sentry
    sentry_dsn: str = ""


settings = Settings()
