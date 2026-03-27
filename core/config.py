from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # --- CONFIGURACIÓN BASE DE DATOS ADMINISTRATIVA ---
    DB_ADMIN_USER: str
    DB_ADMIN_PASSWORD: str
    DB_ADMIN_HOST: str
    DB_ADMIN_PORT: int = 5432
    DB_ADMIN_NAME: str

    # --- CONFIGURACIÓN BASE DE DATOS OPERATIVA ---
    DB_OP_USER: str
    DB_OP_PASSWORD: str
    DB_OP_HOST: str
    DB_OP_PORT: int = 5432
    DB_OP_NAME: str

    # --- JWT ---
    JWT_EXPIRES_MINUTES: int
    JWT_SECRET: str
    JWT_ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()