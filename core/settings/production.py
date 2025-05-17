from .base import *  # noqa

DEBUG = True

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:5174",
    "http://localhost:5173",
    "https://admin.kassalite.uz",
    "https://kassalite.uz",
    "https://account.kassalite.uz"
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:5174",
    "http://localhost:5173",
    "https://admin.kassalite.uz",
    "https://kassalite.uz",
    "https://account.kassalite.uz"
]
