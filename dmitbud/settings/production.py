"""Settings for production."""

import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403


SECRET_KEY = os.getenv('DMITBUD_SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured('Environment variable DMITBUD_SECRET_KEY is not set')

DEBUG = False
ALLOWED_HOSTS = ['.dmitbud.tech']

STATIC_ROOT = "/var/dmitbud/static"

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
