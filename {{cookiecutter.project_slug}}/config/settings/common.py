import os
import sys
import environ

env = environ.Env()
gettext = lambda s: s

# pai
TESTING_MODE = 'test' in sys.argv

ROOT_DIR = (
    environ.Path(__file__) - 3
)  # (django_sso_app/backend/config/settings/common.py - 4 = django_sso_app/)
BACKEND_DIR = ROOT_DIR.path("backend")

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR.path(".env")))


# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", default=True)

# defaults
APP_DOMAIN = env("APP_DOMAIN", default="localhost:8000")
COOKIE_DOMAIN = env("COOKIE_DOMAIN", default='localhost')
DEFAULT_HTTP_PROTOCOL = env("DEFAULT_HTTP_PROTOCOL", default='http' if DEBUG else 'https')
I18N_PATH_ENABLED = env.bool('I18N_PATH_ENABLED', default=True)

# django-sso-app
from django_sso_app.backend.settings import *

DJANGO_SSO_APP_BACKEND_DOMAINS = env('DJANGO_SSO_APP_BACKEND_DOMAINS', default=[APP_DOMAIN])
DJANGO_SSO_APP_SHAPE = env('DJANGO_SSO_APP_SHAPE', default='backend_only')
_DJANGO_SSO_APP_BACKEND_ENABLED = DJANGO_SSO_APP_SHAPE.find('backend') > -1
if _DJANGO_SSO_APP_BACKEND_ENABLED:
    DJANGO_SSO_APP_APIGATEWAY_HOST = env('DJANGO_SSO_APP_APIGATEWAY_HOST', default='http://kong')
    DJANGO_SSO_APP_BACKEND_CUSTOM_FRONTEND_APP = env('DJANGO_SSO_APP_BACKEND_CUSTOM_FRONTEND_APP', default=None)


# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = env("DJANGO_TIME_ZONE", default="UTC") # pai
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = env("DJANGO_LANGUAGE_CODE", default="en") # pai
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = env.int("DJANGO_SITE_ID", default=1) # pai
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [BACKEND_DIR.path("locale")]

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
# MIGRATION_MODULES = {"sites": "backend.contrib.sites.migrations"} # pai


# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(BACKEND_DIR.path("fixtures")),)

# file uploads
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

APPEND_SLASH = True

# context_processors
REPOSITORY_REV = env("REPOSITORY_REV", default=None)
EMAILS_DOMAIN = env('EMAILS_DOMAIN', default=COOKIE_DOMAIN) # domain name specified in email templates
EMAILS_SITE_NAME = env('EMAILS_SITE_NAME', default=EMAILS_DOMAIN) # site name specified in email templates
GOOGLE_API_KEY = env('GOOGLE_API_KEY', default='undefined')
GOOGLE_MAPS_API_VERSION = env('GOOGLE_MAPS_API_VERSION', default='3.34')
GOOGLE_ANALYTICS_TRACKING_ID = env('GOOGLE_ANALYTICS_TRACKING_ID', default='undefined')
