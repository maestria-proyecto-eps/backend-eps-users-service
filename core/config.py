from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field

class Settings(BaseSettings):
    DB_OP_USER: str
    DB_OP_PASSWORD: str
    DB_OP_HOST: str
    DB_OP_PORT: int
    DB_OP_NAME: str

    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXPIRES_MINUTES: int

    @property # O @computed_field en Pydantic v2
    def DB_URL(self) -> str:
        # Usamos los nombres correctos aquí también
        return f"postgresql://{self.DB_OP_USER}:{self.DB_OP_PASSWORD}@{self.DB_OP_HOST}:{self.DB_OP_PORT}/{self.DB_OP_NAME}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()