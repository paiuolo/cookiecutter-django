from .common import *

DRF_DEFAULT_AUTHENTICATION_CLASSES = [
    'rest_framework.authentication.TokenAuthentication'
]
if DEBUG:
    DRF_DEFAULT_AUTHENTICATION_CLASSES = [
        # 'rest_framework.authentication.SessionAuthentication',
    ] + DRF_DEFAULT_AUTHENTICATION_CLASSES

# django-sso-app
DRF_DEFAULT_AUTHENTICATION_CLASSES += ['django_sso_app.core.api.authentication.DjangoSsoApiAuthentication']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': DRF_DEFAULT_AUTHENTICATION_CLASSES,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    # 'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),

    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    # https://www.django-rest-framework.org/community/3.10-announcement/#continuing-to-use-coreapi
}
