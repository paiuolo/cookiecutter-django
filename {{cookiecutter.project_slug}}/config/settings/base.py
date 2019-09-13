"""
Base settings to build other settings files upon.
"""

import os
import sys
import environ

os.environ.setdefault('DJANGO_SSO_APP_USER_PROFILE', 'backend.profiles')

env = environ.Env()
gettext = lambda s: s


ROOT_DIR = (
    environ.Path(__file__) - 3
)  # ({{ cookiecutter.project_slug }}/config/settings/base.py - 3 = {{ cookiecutter.project_slug }}/)
APPS_DIR = ROOT_DIR.path("backend")

# django-sso-app
DJANGO_SSO_APP_SERVER = False
DJANGO_SSO_BACKEND_ENABLED = env.bool('DJANGO_SSO_BACKEND_ENABLED', default=env.bool('DJANGO_SSO_ENABLED', default={% if cookiecutter.use_django_sso.lower() == 'n' %}False{% else %}True{% endif %}))
DJANGO_SSO_APP_ENABLED = env.bool('DJANGO_SSO_APP_ENABLED', default=(not DJANGO_SSO_BACKEND_ENABLED))

if DJANGO_SSO_BACKEND_ENABLED or DJANGO_SSO_APP_ENABLED:
    from django_sso_app.core.settings import environ, env
else:
    READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
    if READ_DOT_ENV_FILE:
        # OS environment variables take precedence over variables from .env
        env.read_env(str(ROOT_DIR.path(".env")))

if DJANGO_SSO_BACKEND_ENABLED:
    from django_sso_app.core.settings.backend import *
    from django_sso_app.core.settings.app import *
elif DJANGO_SSO_APP_ENABLED:
    from django_sso_app.core.settings.app import *


# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = env("DJANGO_TIME_ZONE", default="{{ cookiecutter.timezone }}") # pai
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = env("DJANGO_LANGUAGE_CODE", default="en-us") # pai
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = env.int("DJANGO_SITE_ID", default=1) # pai
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [ROOT_DIR.path("locale")]

#pai
TESTING_MODE = 'test' in sys.argv or DEBUG
DJANGO_ALLAUTH_ENABLED = env.bool('DJANGO_ALLAUTH_ENABLED', default={% if cookiecutter.use_django_allauth.lower() == 'n' %}False{% else %}True{% endif %})

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
{% if cookiecutter.use_docker == "y" -%}
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
]
THIRD_PARTY_APPS = [
    "crispy_forms",
    # pai
    "corsheaders",
]

THIRD_PARTY_APPS += [
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_swagger",

    "django_filters",
{%- if cookiecutter.use_celery == 'y' %}
    "django_celery_beat",
{%- endif %}
]

if DJANGO_SSO_ENABLED:
    THIRD_PARTY_APPS += [
        "django_sso_app",
    ]


LOCAL_APPS = [
    "backend.users.apps.UsersConfig",
    # Your stuff: custom apps go here

]

# django-sso-app
if DJANGO_SSO_BACKEND_ENABLED:
    LOCAL_APPS += [
        "rest_auth",
        "rest_auth.registration",
    ] + DJANGO_SSO_BACKEND_CORE_APPS
elif DJANGO_SSO_APP_ENABLED:
    LOCAL_APPS += DJANGO_SSO_APP_CORE_APPS

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
# MIGRATION_MODULES = {"sites": "backend.contrib.sites.migrations"} # pai

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
# pai
if DJANGO_ALLAUTH_ENABLED or DJANGO_SSO_BACKEND_ENABLED:
    AUTHENTICATION_BACKENDS += [
        "allauth.account.auth_backends.AuthenticationBackend",
    ]

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "users:redirect"
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
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    # pai
    "backend.middleware.x_forwarded_for.middleware.XForwardedForMiddleware",

    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # pai
    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]
# pai
if DJANGO_SSO_APP_ENABLED:
    MIDDLEWARE.append('django_sso_app.app.middleware.DjangoSsoAppMiddleware')

MIDDLEWARE += [
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR("staticfiles"))
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR.path("static"))]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR("media"))
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

                # pai
                'backend.context_processors.get_repository_rev',
                'backend.context_processors.get_auth_settings',
            ],
        },
    }
]
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
# pai
"""
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
"""
from .logging import LOGGING

{% if cookiecutter.use_celery == 'y' -%}
# Celery
# ------------------------------------------------------------------------------
if USE_TZ:
    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = env("CELERY_TASK_TIME_LIMIT", default=(5 * 60))
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = env("CELERY_TASK_SOFT_TIME_LIMIT", default=60)
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

{%- endif %}

# pai
LANGUAGES = (
    ## Customize this
    ('it', gettext('it')),
    ('en', gettext('en')),
    ('es', gettext('es')),
    ('pt', gettext('pt')),
    ('fr', gettext('fr')),
    ('de', gettext('de')),
)

# pai
if DJANGO_ALLAUTH_ENABLED:
    # django-allauth
    # ------------------------------------------------------------------------------
    ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
    # https://django-allauth.readthedocs.io/en/latest/configuration.html
    ACCOUNT_AUTHENTICATION_METHOD = "username_email"
    # https://django-allauth.readthedocs.io/en/latest/configuration.html
    ACCOUNT_EMAIL_REQUIRED = True
    # https://django-allauth.readthedocs.io/en/latest/configuration.html
    ACCOUNT_EMAIL_VERIFICATION = "mandatory"
    # https://django-allauth.readthedocs.io/en/latest/configuration.html
    ACCOUNT_ADAPTER = "backend.users.adapters.AccountAdapter"
    # https://django-allauth.readthedocs.io/en/latest/configuration.html
    SOCIALACCOUNT_ADAPTER = "backend.users.adapters.SocialAccountAdapter"
    # pai
    ACCOUNT_CONFIRM_EMAIL_ON_GET = True
    ACCOUNT_USERNAME_REQUIRED = True
    ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
    ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGIN_URL
    ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = LOGIN_URL
    ACCOUNT_SESSION_REMEMBER = False

if DJANGO_SSO_BACKEND_ENABLED:
    ACCOUNT_ADAPTER = "django_sso_app.backend.adapters.UserAdapter"
    ACCOUNT_FORMS = {
        'signup': 'django_sso_app.backend.forms.SignupForm'
    }

{% if cookiecutter.use_compressor == 'y' -%}
# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/quickstart/#installation
INSTALLED_APPS += ["compressor"]
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]
{%- endif %}
# Your stuff...

# pai

REPOSITORY_REV = env("REPOSITORY_REV", default=None)

FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

ENABLE_HTTPS = env.bool("ENABLE_HTTPS", False)

ACCOUNT_DEFAULT_HTTP_PROTOCOL = env("ACCOUNT_DEFAULT_HTTP_PROTOCOL", default="https" if ENABLE_HTTPS else "http")
APPEND_SLASH = True

APP_DOMAIN = env("APP_DOMAIN", default="{{cookiecutter.domain_name}}")
APP_DOMAINS = env.list("APP_DOMAINS", default=[APP_DOMAIN, ])
APP_URL = ACCOUNT_DEFAULT_HTTP_PROTOCOL + '://' + APP_DOMAIN

COOKIE_DOMAIN = env("COOKIE_DOMAIN", default=APP_DOMAIN)

# cors
if DEBUG:
    CORS_ORIGIN_ALLOW_ALL = True
else:
    # https://github.com/ottoyiu/django-cors-headers
    # CORS headers defaults to '{{cookiecutter.domain_name}}'
    _CORS_ORIGINS = env("CORS_ORIGINS", default='{0}://{1}'.format(ACCOUNT_DEFAULT_HTTP_PROTOCOL, COOKIE_DOMAIN))
    CORS_ORIGIN_WHITELIST = list(map(lambda x: '{}'.format(x.replace(' ', '')), _CORS_ORIGINS.split(',')))
    #CORS_ORIGIN_WHITELIST = _CORS_ORIGINS.split(',')
    CORS_ALLOW_CREDENTIALS = True

# csrf
# https://docs.djangoproject.com/en/2.0/ref/settings/#csrf-trusted-origins

if DEBUG:
    CSRF_COOKIE_DOMAIN = None
    CORS_ORIGIN_ALLOW_ALL = True
    CSRF_TRUSTED_ORIGINS = []
else:
    CSRF_COOKIE_DOMAIN = APP_DOMAIN
    CSRF_TRUSTED_ORIGINS = ['.{0}'.format(COOKIE_DOMAIN)]

# django-sso-app
if DJANGO_SSO_BACKEND_ENABLED or DJANGO_SSO_APP_ENABLED:
    AUTHENTICATION_BACKENDS = AUTHENTICATION_BACKENDS + [
        'django_sso_app.app.backends.DjangoSsoAppBackend',
    ]

# djangorestframework

DRF_DEFAULT_AUTHENTICATION_CLASSES = [
    # 'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.TokenAuthentication'
]

if DJANGO_SSO_BACKEND_ENABLED:
    DRF_DEFAULT_AUTHENTICATION_CLASSES += [
        'django_sso_app.backend.authentication.JWTAuthentication',
    ]
elif DJANGO_SSO_APP_ENABLED:
    DRF_DEFAULT_AUTHENTICATION_CLASSES += [
        'django_sso_app.app.authentication.DjangoSsoAppAuthentication',
    ]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': DRF_DEFAULT_AUTHENTICATION_CLASSES,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),

    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    # https://www.django-rest-framework.org/community/3.10-announcement/#continuing-to-use-coreapi
}

# rest_auth
if DJANGO_SSO_BACKEND_ENABLED:
    REST_USE_JWT = True
    REST_AUTH_SERIALIZERS = {
        'LOGIN_SERIALIZER': 'django_sso_app.backend.serializers.LoginSerializer',
        'PASSWORD_RESET_SERIALIZER': 'django_sso_app.backend.serializers.PasswordResetSerializer',
        'USER_DETAILS_SERIALIZER' : 'django_sso_app.core.apps.users.serializers.UserSerializer',
    }

    REST_AUTH_REGISTER_SERIALIZERS = {
        'REGISTER_SERIALIZER': 'django_sso_app.backend.serializers.RegisterSerializer',
    }

    JWT_AUTH = {
        'JWT_AUTH_COOKIE': 'jwt',

        'JWT_PAYLOAD_HANDLER': 'django_sso_app.backend.handlers.jwt_payload_handler',
        'JWT_AUTH_HEADER_PREFIX': 'Bearer',
        'JWT_VERIFY': False,
    }


    print('ROOT_DIR', ROOT_DIR, "INSTALLED_APPS", INSTALLED_APPS)


# swagger
SWAGGER_SETTINGS = {
    'LOGIN_URL': '/admin/login/',
    'LOGOUT_URL': '/admin/logout/',
    'SECURITY_DEFINITIONS': {
        'JWT': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Bearer xxx'
        },
        'token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Token xxx'
        }
    }
}


# ------------------------------------------------------------------------------
