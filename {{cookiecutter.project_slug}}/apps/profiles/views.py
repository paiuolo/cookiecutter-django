from rest_framework import viewsets
from rest_framework import permissions

from .models import Profile
from .serializers import ProfileSerializer, ProfilePublicSerializer


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return ProfileSerializer
        else:
            return ProfilePublicSerializer


    def list(self, request):
        """
        List
        """
        return super(ProfileViewSet, self).list(request)

    def retrieve(self, request, pk=None):
        """
        Detail
        """
        return super(ProfileViewSet, self).retrieve(request, pk)
