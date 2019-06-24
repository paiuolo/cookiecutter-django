from rest_framework import serializers


class PartialObjectSerializer(serializers.Serializer):
    _partial = serializers.SerializerMethodField(method_name='get_partial')

    def get_partial(self, obj):
        return True


class AbsoluteUrlSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(method_name='get_absolute_url')

    def get_absolute_url(self, obj):
        if getattr(obj, 'pk', None) is not None:
            get_absolute_url = getattr(obj, 'get_absolute_url', None)
            if get_absolute_url is None:
                raise NotImplementedError('Model must provide "get_absolute_url" method.')
            else:
                request = self.context['request']
                return request.build_absolute_uri(get_absolute_url())

