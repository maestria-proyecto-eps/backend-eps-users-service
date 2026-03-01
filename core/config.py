from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Variables que vienen del mensaje del Scrum
    DB_ADMIN_USER: str
    DB_ADMIN_PASSWORD: str
    DB_ADMIN_HOST: str
    DB_ADMIN_PORT: str = "5432"
    DB_ADMIN_NAME: str = "postgres"

    # JWT
    JWT_EXPIRES_MINUTES: int
    JWT_SECRET: str
    JWT_ALGORITHM: str

    @computed_field
    @property
    def DB_URL(self) -> str:
        return f"postgresql://{self.DB_ADMIN_USER}:{self.DB_ADMIN_PASSWORD}@{self.DB_ADMIN_HOST}:{self.DB_ADMIN_PORT}/{self.DB_ADMIN_NAME}"

settings = Settings()