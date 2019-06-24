from rest_framework.reverse import reverse

from {{cookiecutter.project_slug}}.serializers import AbsoluteUrlSerializer
from .models import Profile


class ProfileSerializer(AbsoluteUrlSerializer):

    class Meta:
        model = Profile
        read_only_fields = (
            'id', 'created_at', 'sso_id', 'sso_rev', 'username', 'email',
            'first_name', 'last_name', 'description', 'birthdate', 'picture',
            'latitude', 'longitude', 'country', 'address')
        fields = read_only_fields

    def get_absolute_url(self, obj):
        if getattr(obj, 'id', None) is not None:
            request = self.context['request']
            reverse_url = reverse('profile:detail', kwargs={'id': obj.id})
            return request.build_absolute_uri(reverse_url)


class ProfilePublicSerializer(ProfileSerializer):

    class Meta:
        model = Profile
        read_only_fields = (
            'url',
            'created_at', 'username', 'picture',
            'latitude', 'longitude', 'country')
        fields = read_only_fields
