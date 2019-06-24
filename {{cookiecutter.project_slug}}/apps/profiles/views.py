from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.http import Http404

from .models import Profile
from .serializers import ProfileSerializer, ProfilePublicSerializer, GroupSerializer


User = get_user_model()

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing Profiles.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfilePublicSerializer

    def list(self, request, *args, **kwargs):
        return super(ProfileViewSet, self).list(request, *args, **kwargs)


class UserProfileViewSet( mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):

    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset = Profile.objects.all()
        return queryset

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        try:
            user = User.objects.get(pk=pk)
            self.check_object_permissions(self.request, user)
            return user
        except User.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        profile = request.user.profile

        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = GroupSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Group.objects.all()
