from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    user: str
    password: str
    host: str
    port: int = 5432
    dbname: str

    #jwt
    JWT_EXPIRES_MINUTES: int
    JWT_SECRET: str
    JWT_ALGORITHM: str

    class Config:
        env_file = ".env"

settings = Settings()
