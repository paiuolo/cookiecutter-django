from .common import *


# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(ROOT_DIR, 'db.sqlite3'),
        }
    }
    DATABASES["default"]["ATOMIC_REQUESTS"] = True
else:
    DATABASES = {"default": env.db("DATABASE_URL")}
