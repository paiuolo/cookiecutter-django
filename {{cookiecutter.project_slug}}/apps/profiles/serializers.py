from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        read_only_fields = (
        'id', 'created_at', 'sso_id', 'sso_rev', 'username', 'email',
        'first_name', 'last_name', 'description', 'birthdate', 'picture',
        'latitude', 'longitude', 'country', 'address')
        fields = read_only_fields


class ProfilePublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        read_only_fields = (
        'created_at', 'sso_id', 'username',
        'first_name', 'last_name', 'description', 'birthdate', 'picture',
        'latitude', 'longitude', 'country')
        fields = read_only_fields

