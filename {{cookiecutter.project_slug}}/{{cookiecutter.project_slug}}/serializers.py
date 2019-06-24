from rest_framework import serializers


class PartialObjectSerializer(serializers.Serializer):
    _partial = serializers.SerializerMethodField(method_name='get_partial')

    def get_partial(self, obj):
        return True


class AbsoluteUrlSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(method_name='get_absolute_url')

    def get_absolute_url(self, obj):
        raise NotImplementedError()
