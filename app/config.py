from pydantic import BaseSettings
from app.consts import AppModes


class Settings(BaseSettings):
    BOT_TOKEN: str = ""
    APP_URL: str = ""
    APP_MODE: int = AppModes.Webhook
    WEBHOOK_IS_SET: bool = False

    class Config:
        env_file = '../.env'
        env_file_encoding = "utf-8"


settings = Settings()
