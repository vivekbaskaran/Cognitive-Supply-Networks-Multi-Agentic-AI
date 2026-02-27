from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = "Cognitive Supply Network Agent"
    default_user: str = "demo_user"
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    google_api_key: str = Field(..., env="GOOGLE_API_KEY")
    port: int = 8000
    provider: str = Field("google", env="PROVIDER")  # "openai" or "google"
    session_timeout : int = 3600  # in seconds
    use_in_memory: bool = True

    class Config:
        env_file = ".env"


settings = Settings()