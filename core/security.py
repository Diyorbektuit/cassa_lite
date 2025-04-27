import os
from dotenv import load_dotenv
load_dotenv()


class Security:
    DJANGO_SETTINGS_MODULE: str = os.getenv('DJANGO_SETTINGS_MODULE')
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    DEBUG: bool = os.getenv('DEBUG')

    DB_ENGINE: str = os.getenv('DB_ENGINE')
    DB_NAME: str = os.getenv('DB_NAME')
    DB_USER: str = os.getenv('DB_USER')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = os.getenv('DB_PORT')

    GOOGLE_CLIENT_ID: str= os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET: str = os.getenv('GOOGLE_CLIENT_SECRET')
    google_redirect_uri: str = os.getenv('google_redirect_uri')
    redirect_url: str = os.getenv('redirect_url')

    BOT_TOKEN: str = os.getenv('BOT_TOKEN')


SECURITY = Security()