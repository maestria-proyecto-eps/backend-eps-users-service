from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ADMIN
    DB_ADMIN_USER: str = "test"
    DB_ADMIN_PASSWORD: str = "test"
    DB_ADMIN_HOST: str = "localhost"
    DB_ADMIN_PORT: int = 5432
    DB_ADMIN_NAME: str = "test_db"

    # OPERATIVA
    DB_OP_USER: str = "test"
    DB_OP_PASSWORD: str = "test"
    DB_OP_HOST: str = "localhost"
    DB_OP_PORT: int = 5432
    DB_OP_NAME: str = "test_db"

    # JWT
    JWT_EXPIRES_MINUTES: int = 60
    JWT_SECRET: str = "test-secret"
    JWT_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()