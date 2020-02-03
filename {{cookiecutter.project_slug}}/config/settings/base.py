"""
Base settings to build other settings files upon.
"""

import environ
import sys
import os

ROOT_DIR = (
    environ.Path(__file__) - 3
)  # ({{ cookiecutter.project_slug }}/config/settings/base.py - 3 = {{ cookiecutter.project_slug }}/)
APPS_DIR = ROOT_DIR.path("backend")

env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR.path(".env")))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = env("DJANGO_TIME_ZONE", default="{{cookiecutter.timezone}}")  # pai
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = env("DJANGO_LANGUAGE_CODE", default="en")  # pai
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = env.int("DJANGO_SITE_ID", default=1)  # pai
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [ROOT_DIR.path("locale")]

# pai
TESTING_MODE = 'test' in sys.argv
BACKEND_DIR = ROOT_DIR.path("backend")

APP_DOMAIN = env("APP_DOMAIN", default="localhost:8000")
COOKIE_DOMAIN = env("COOKIE_DOMAIN", default=APP_DOMAIN)
DEFAULT_HTTP_PROTOCOL = env("DEFAULT_HTTP_PROTOCOL", default='http' if DEBUG else 'https')
I18N_PATH_ENABLED = env.bool('I18N_PATH_ENABLED', default=True)
REDIS_ENABLED = env.bool('REDIS_ENABLED', default=False)

# file uploads
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

# slashes
APPEND_SLASH = True

# django-sso-app
from django_sso_app.settings import *
from .extra import EXTRA_APPS

DJANGO_SSO_APP_BACKEND_DOMAINS = env('DJANGO_SSO_APP_BACKEND_DOMAINS', default=[APP_DOMAIN])
DJANGO_SSO_APP_SHAPE = env('DJANGO_SSO_APP_SHAPE', default='backend_only')
_DJANGO_SSO_APP_BACKEND_ENABLED = DJANGO_SSO_APP_SHAPE.find('backend') > -1
if _DJANGO_SSO_APP_BACKEND_ENABLED:
    DJANGO_SSO_APP_APIGATEWAY_HOST = env('DJANGO_SSO_APP_APIGATEWAY_HOST', default='http://kong')
    DJANGO_SSO_APP_BACKEND_CUSTOM_FRONTEND_APP = env('DJANGO_SSO_APP_BACKEND_CUSTOM_FRONTEND_APP', default=None)

# context_processors
REPOSITORY_REV = env("REPOSITORY_REV", default=None)
EMAILS_DOMAIN = env('EMAILS_DOMAIN', default=COOKIE_DOMAIN) # domain name specified in email templates
EMAILS_SITE_NAME = env('EMAILS_SITE_NAME', default=EMAILS_DOMAIN) # site name specified in email templates
GOOGLE_API_KEY = env('GOOGLE_API_KEY', default='undefined')
GOOGLE_MAPS_API_VERSION = env('GOOGLE_MAPS_API_VERSION', default='3.34')
GOOGLE_ANALYTICS_TRACKING_ID = env('GOOGLE_ANALYTICS_TRACKING_ID', default='undefined')

# languages
from .languages import *

# meta
META_DESCRIPTION = env('META_DESCRIPTION', default=APP_DOMAIN)
META_SITE_PROTOCOL = 'https' if DEFAULT_HTTP_PROTOCOL else 'http'
META_USE_SITES = True
# META_SITE_DOMAIN = APP_DOMAIN
META_SITE_NAME = APP_DOMAIN
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_USE_GOOGLEPLUS_PROPERTIES = True


# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
if DEBUG:  # pai
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(ROOT_DIR, 'db.sqlite3'),
        }
    }
    DATABASES["default"]["ATOMIC_REQUESTS"] = True
else:
{% if cookiecutter.use_docker == "y" %}
    DATABASES = {"default": env.db("DATABASE_URL")}
{%- else %}
    DATABASES = {
        "default": env.db("DATABASE_URL", default="postgres://{% if cookiecutter.windows == 'y' %}localhost{% endif %}/{{cookiecutter.project_slug}}")
    }
{%- endif %}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    "django.contrib.admin",
    "django.forms",
    "django.contrib.flatpages",
]
THIRD_PARTY_APPS = [
    "crispy_forms",
    # "allauth",  # django-sso-app
    # "allauth.account",  # django-sso-app
    # "allauth.socialaccount",  # django-sso-app
    "rest_framework",

    # pai
    "corsheaders",
    "meta",
{%- if cookiecutter.use_celery == 'y' %}
    "django_filters",
    "django_celery_beat",
    "django_celery_results",
    "drf_yasg",
{%- endif %}
]

LOCAL_APPS = [
    "backend.users.apps.UsersConfig",
    # Your stuff: custom apps go here
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS + DJANGO_SSO_APP_DJANGO_APPS + EXTRA_APPS  # pai

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
# MIGRATION_MODULES = {"sites": "{{ cookiecutter.project_slug }}.contrib.sites.migrations"}  # pai

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    # "allauth.account.auth_backends.AuthenticationBackend",  # django-sso-app
] + DJANGO_SSO_APP_DJANGO_AUTHENTICATION_BACKENDS
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "/"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
""" pai
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
"""
AUTH_PASSWORD_VALIDATORS = []  # pai

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django_sso_app.backend.middleware.x_forwarded_for.middleware.XForwardedForMiddleware",  # pai
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # pai
{%- if cookiecutter.use_whitenoise == 'y' %}
    "whitenoise.middleware.WhiteNoiseMiddleware",
{%- endif %}
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_sso_app.core.middleware.DjangoSsoAppAuthenticationMiddleware",  # django-sso-app
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",  # pai
]

# STATIC
# ------------------------------------------------------------------------------
# pai
_ENV_PUBLIC_ROOT = env('DJANGO_PUBLIC_ROOT', default=None)
if _ENV_PUBLIC_ROOT is None:
    PUBLIC_ROOT = ROOT_DIR.path("public")
else:
    PUBLIC_ROOT = environ.Path(_ENV_PUBLIC_ROOT)

# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(PUBLIC_ROOT("static"))  # pai
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(BACKEND_DIR.path("static"))]  # pai
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(PUBLIC_ROOT("media"))  # pai
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [str(APPS_DIR.path("templates"))],
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                # "{{ cookiecutter.project_slug }}.utils.context_processors.settings_context",  # pai

                # django-sso-app
                'django_sso_app.core.context_processors.django_sso_app_context',
                'django_sso_app.backend.context_processors.get_repository_rev',
                'django_sso_app.backend.context_processors.get_meta_info',
            ],
        },
    }
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap4"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# pai
ENABLE_HTTPS = env.bool("ENABLE_HTTPS", default=not DEBUG)
ACCOUNT_DEFAULT_HTTP_PROTOCOL = env("ACCOUNT_DEFAULT_HTTP_PROTOCOL", default="https" if ENABLE_HTTPS else "http")

# CSRF
if DEBUG:
    CSRF_COOKIE_DOMAIN = None
    CORS_ORIGIN_ALLOW_ALL = True
    CSRF_TRUSTED_ORIGINS = []
else:
    CSRF_COOKIE_DOMAIN = APP_DOMAIN
    CSRF_TRUSTED_ORIGINS = ['.{0}'.format(COOKIE_DOMAIN)]

# cors
if DEBUG:
    CORS_ORIGIN_ALLOW_ALL = True
else:
    # https://github.com/ottoyiu/django-cors-headers
    # CORS headers defaults to 'accounts.example.com'
    _CORS_ORIGINS = env("CORS_ORIGINS", default='{0}://{1}'.format(ACCOUNT_DEFAULT_HTTP_PROTOCOL, COOKIE_DOMAIN))
    CORS_ORIGIN_WHITELIST = list(map(lambda x: '{}'.format(x.replace(' ', '')), _CORS_ORIGINS.split(',')))
    #CORS_ORIGIN_WHITELIST = _CORS_ORIGINS.split(',')
    CORS_ALLOW_CREDENTIALS = True


# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
# https://docs.djangoproject.com/en/2.2/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""{{cookiecutter.author_name}}""", "{{cookiecutter.email}}")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

{% if cookiecutter.use_celery == 'y' -%}
# Celery
# ------------------------------------------------------------------------------
if USE_TZ:
    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
""" pai
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
"""
if REDIS_ENABLED:
    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
    CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/0")
    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
    # CELERY_RESULT_BACKEND = CELERY_BROKER_URL
else:
    # https://docs.celeryproject.org/en/3.1/getting-started/brokers/django.html
    CELERY_BROKER_URL = 'django://'
    # django-sso-app
    CELERY_CACHE_BACKEND = 'django-cache'

CELERY_RESULT_BACKEND = 'django-db'  # pai

# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = 5 * 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

{%- endif %}
# django-allauth
# ------------------------------------------------------------------------------
""" pai
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "username"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = "{{cookiecutter.project_slug}}.users.adapters.AccountAdapter"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = "{{cookiecutter.project_slug}}.users.adapters.SocialAccountAdapter"
"""

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

{% if cookiecutter.use_compressor == 'y' -%}
# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/quickstart/#installation
INSTALLED_APPS += ["compressor"]
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]
{%- endif %}
{% if cookiecutter.use_drf == "y" -%}
# django-reset-framework
# -------------------------------------------------------------------------------
# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # "rest_framework.authentication.SessionAuthentication",  # pai
        "django_sso_app.core.api.authentication.DjangoSsoApiAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),

    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    # "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),

    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z",

    # "DEFAULT_RENDERER_CLASSES": (
    #     "rest_framework.renderers.JSONRenderer",
    #     "rest_framework.renderers.BrowsableAPIRenderer",
    # ),
}
{%- endif %}
# Your stuff...
# ------------------------------------------------------------------------------

from .extra import *  # pai
