from django_sso_app.backend.settings import DJANGO_SSO_APP_DJANGO_APPS
from .extra import EXTRA_APPS


# DJANGO_SSO_APP_DJANGO_APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'django.contrib.humanize', # Handy template tags
    'django.contrib.admin',
]

LOCAL_APPS = [
    'crispy_forms',
    # pai
    'corsheaders',

    'meta',

    'django_filters',
    'django_celery_beat',

    'rest_framework',
    'rest_framework.authtoken',

    'drf_yasg',
] + DJANGO_SSO_APP_DJANGO_APPS

LOCAL_APPS += [
    'django_sso_app.backend.users.apps.UsersConfig',
    # Your stuff: custom apps go here
] + EXTRA_APPS

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS
