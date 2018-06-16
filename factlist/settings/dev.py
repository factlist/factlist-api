from .base import *
import os

DEBUG = True

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://" + os.environ.get("REDIS_HOST") + "/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
        "TIMEOUT": None,
    }
}

ALLOWED_HOSTS = [os.environ.get("ALLOWED_HOST"), "localhost"]
