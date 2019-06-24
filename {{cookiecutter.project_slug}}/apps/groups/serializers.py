from rest_framework.reverse import reverse

from {{cookiecutter.project_slug}}.serializers import AbsoluteUrlSerializer
from .models import Group


class GroupSerializer(AbsoluteUrlSerializer):
    class Meta:
        model = Group
        read_only_fields = ('url', 'id', 'name')
        fields = read_only_fields

    def get_absolute_url(self, obj):
        if getattr(obj, 'id', None) is not None:
            request = self.context['request']
            reverse_url = reverse('groups:detail', kwargs={'pk': obj.pk})
            return request.build_absolute_uri(reverse_url)
