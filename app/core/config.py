from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AI App"
    DEBUG: bool = True
    SECRET_KEY: str = "supersecretkey123" # In production, use a secure random secret
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 1 week

    class Config:
        env_file = ".env"

settings = Settings()
