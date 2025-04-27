from .base import *  # noqa

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ["*"]

INTERNAL_IPS = [
    "127.0.0.1",
    '192.168.1.21',
    '192.168.1.42'

]