"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Environment-based configuration. All secrets come from .env or deployment env vars."""

    # Supabase
    supabase_url: str = ""
    supabase_service_role_key: str = ""
    supabase_anon_key: str = ""

    # AI providers
    openrouter_api_key: str = ""

    # Email
    resend_api_key: str = ""
    resend_from_email: str = "audit@airev.app"

    # App
    app_url: str = "http://localhost:8000"
    frontend_url: str = "http://localhost:3000"
    rate_limit_per_minute: int = 10

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
