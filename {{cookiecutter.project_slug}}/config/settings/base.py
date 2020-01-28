"""
Base settings to build other settings files upon.
"""

# common
from .common import *

from .allauth import *
from .databases import *
from .urls import *
from .apps import *
from .authentication import *
from .middleware import *
from .static import *
from .templates import *
from .security import *
from .email import *
from .logging import LOGGING
from .languages import *
from .restframework import *
from .meta import *
from .celery import *
from .extra import *

# ------------------------------------------------------------------------------

"""
print('ROOT_DIR', ROOT_DIR,
      'INSTALLED_APPS', INSTALLED_APPS,
      'MIDDLEWARE', MIDDLEWARE,
      'AUTHENTICATION_BACKENDS', AUTHENTICATION_BACKENDS,
      'LANGUAGES', LANGUAGES,
      'LOGGING', LOGGING.keys())
"""
