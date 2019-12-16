from .common import *

# STATIC
# ------------------------------------------------------------------------------
_ENV_PUBLIC_ROOT = env('DJANGO_PUBLIC_ROOT', default=None)
if _ENV_PUBLIC_ROOT is None:
    PUBLIC_ROOT = ROOT_DIR.path("public")
else:
    PUBLIC_ROOT = environ.Path(_ENV_PUBLIC_ROOT)

# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(PUBLIC_ROOT("static"))
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(BACKEND_DIR.path("static"))]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(PUBLIC_ROOT("media"))
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"
