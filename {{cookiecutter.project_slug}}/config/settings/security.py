from .common import *

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Luca Bertuol""", "paiuolo@gmail.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

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

ENABLE_HTTPS = env.bool("ENABLE_HTTPS", default=False)
ACCOUNT_DEFAULT_HTTP_PROTOCOL = env("ACCOUNT_DEFAULT_HTTP_PROTOCOL", default="https" if ENABLE_HTTPS else "http")

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

# csrf
# https://docs.djangoproject.com/en/2.0/ref/settings/#csrf-trusted-origins

if DEBUG:
    CSRF_COOKIE_DOMAIN = None
    CORS_ORIGIN_ALLOW_ALL = True
    CSRF_TRUSTED_ORIGINS = []
else:
    CSRF_COOKIE_DOMAIN = APP_DOMAIN
    CSRF_TRUSTED_ORIGINS = ['.{0}'.format(COOKIE_DOMAIN)]
