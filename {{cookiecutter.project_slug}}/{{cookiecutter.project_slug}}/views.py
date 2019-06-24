from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView

from rest_framework_swagger import renderers


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
