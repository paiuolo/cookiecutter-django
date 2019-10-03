import logging

from django_sso_app.core.apps.profiles.views import (ProfileViewSet as DjangoSSoAppProfileViewSet,
                                                     ProfileView as DjangoSSoAppProfileView,
                                                     ProfileUpdateView as DjangoSSoAppProfileUpdateView)
from django_sso_app.core.utils import get_profile_model

from .serializers import ProfileSerializer, ProfilePublicSerializer
from backend.permissions import is_staff

logger = logging.getLogger('profiles')
Profile = get_profile_model()


class ProfileViewSet(DjangoSSoAppProfileViewSet):

    def get_queryset(self):
        user = self.request.user
        if is_staff(user):
            return Profile.objects.all()
        else:
            return Profile.objects.filter(user=user)

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return ProfileSerializer
        else:
            return ProfilePublicSerializer


class ProfileView(DjangoSSoAppProfileView):
    pass


class ProfileUpdateView(DjangoSSoAppProfileUpdateView):
    pass
