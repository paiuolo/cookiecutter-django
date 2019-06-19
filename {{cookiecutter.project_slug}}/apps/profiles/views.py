from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.response import Response

from .models import Profile
from .serializers import ProfileSerializer


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing Profiles.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


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

