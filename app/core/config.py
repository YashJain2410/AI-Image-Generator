from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "AI Image Generator"
    ENVIRONMENT: str = Field(default="development")

    API_V1_PREFIX: str = "/api/v1"

    FAL_API_KEY: str | None = None
    REPLICATE_API_TOKEN: str | None = None
    HUGGINGFACE_API_TOKEN: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()