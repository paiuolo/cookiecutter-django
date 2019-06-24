import logging
import os

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from rest_framework.permissions import AllowAny
from rest_framework.schemas import SchemaGenerator

from rest_framework_swagger import renderers

logger = logging.getLogger('django')
CURRENT_DIR = os.getcwd()


class HealthView(APIView):
    """
    Return instance stats.
    """

    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        try:
            stats = os.statvfs(CURRENT_DIR)
            free_space_mb = int(
                (stats.f_bavail * stats.f_frsize) / (1024 * 1024))

            logger.info(
                'Free space (MB): {}.'.format(free_space_mb))

            status = 'red'
            if free_space_mb > 100:
                status = 'green'
            else:
                status = 'yellow'

            data = {
                'status': status,
            }

            if request.user.is_staff:
                data['free_space_mb'] = free_space_mb

            return Response(data, status.HTTP_200_OK)
        except:
            logger.exception('Error getting health')


class APIRoot(APIView):
    """
    API Root.
    """

    # permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        try:
            return Response({
                'health': reverse('health', request=request, format=format),

                'profiles': reverse('consumer-list', request=request,
                                     format=format),
                'groups': reverse('group-list', request=request, format=format)
            })
        except:
            logger.exception('Error getting api-root')


class SwaggerSchemaView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]
    title = '{{cookiecutter.project_name}}'
    patterns = []

    def get(self, request):
        generator = SchemaGenerator(title=self.title, patterns=self.patterns)
        schema = generator.get_schema(request=request)

        return Response(schema)
