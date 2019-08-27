import logging
import os

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.schemas import SchemaGenerator
from rest_framework import status

from rest_framework_swagger import renderers

logger = logging.getLogger('django')
CURRENT_DIR = os.getcwd()


class StatsView(APIView):
    """
    Return instance stats
    """

    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            stats = os.statvfs(CURRENT_DIR)
            free_space_mb = int(
                (stats.f_bavail * stats.f_frsize) / (1024 * 1024))

            logger.info(
                'Free space (MB): {}.'.format(free_space_mb))

            if free_space_mb > 200:
                health_status = 'green'
            else:
                if free_space_mb < 100:
                    health_status = 'yellow'
                else:
                    health_status = 'red'

            data = {
                'status': health_status,
            }

            if request.user is not None and request.user.is_staff:
                data['free_space_mb'] = free_space_mb

            return Response(data, status.HTTP_200_OK)

        except Exception as e:
            err_msg = str(e)
            logger.exception('Error getting health {}'.format(err_msg))
            return Response(err_msg, status.HTTP_500_INTERNAL_SERVER_ERROR)


class SSOAPIRoot(APIView):
    """
    SSO API Root
    """
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            return Response({
                'profiles': reverse('profiles:list', request=request, *args, **kwargs),
                'groups': reverse('groups:list', request=request, *args, **kwargs),
            })
        except:
            logger.exception('Error getting sso-api-root')


class APIRoot(APIView):
    """
    API Root
    """
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            return Response({
                'stats': reverse('stats', request=request),
                'auth': reverse('ssoauth', request=request, *args, **kwargs),

                # add here
            })
        except:
            logger.exception('Error getting api-root')


class SwaggerSchemaView(APIView):
    """
    OpenAPI
    """
    permission_classes = (AllowAny,)
    renderer_classes = (
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    )
    title = 'Django Fisherman'
    patterns = []

    def get(self, request):
        generator = SchemaGenerator(title=self.title, patterns=self.patterns)
        schema = generator.get_schema(request=request)

        return Response(schema)
