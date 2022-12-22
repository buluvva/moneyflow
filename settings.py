from pydantic import BaseSettings


class Settings(BaseSettings):
    """ Gets data from env and fills params values. """

    TELEGRAM_API_KEY = ''

    POSTGRES_PATH: str = '0.0.0.0'
    POSTGRES_LOGIN: str = ''
    POSTGRES_PASSWORD: str = ''

    GOOGLE_CLIENT_SECRET: dict = ''
    GOOGLE_SERVICE_SECRET: dict = ''


settings = Settings()
