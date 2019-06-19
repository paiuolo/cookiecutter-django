from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    score = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        read_only_fields = ('id', 'created_at', 'sso_id', 'sso_rev', 'username', 'email', 'first_name', 'last_name', 'description', 'birthdate', 'picture', 'latitude', 'longitude', 'country', 'address', 'score')
        fields = read_only_fields

    def get_score(self, obj):
        return 100