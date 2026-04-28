from .base import *
from decouple import config

DEBUG = True

SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-sea-doo-romania-dev-only-change-in-production-xyz123',
)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='*',
    cast=lambda v: [s.strip() for s in v.split(',')],
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

HERO_VIDEO_URL = config('HERO_VIDEO_URL', default='')
FORUM_EXTERNAL_URL = config('FORUM_EXTERNAL_URL', default='https://forum.domain.ro')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
