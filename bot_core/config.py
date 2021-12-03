from pydantic import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str = ""
    APP_URL: str = ""

    class Config:
        env_file = '../.env'
        env_file_encoding = "utf-8"


settings = Settings()
