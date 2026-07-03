"""Settings for production."""

import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403


SECRET_KEY = os.getenv('DMITBUD_SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured('Environment variable DMITBUD_SECRET_KEY is not set')

DEBUG = False
ALLOWED_HOSTS = ['.dmitbud.tech']
