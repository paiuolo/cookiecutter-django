import logging

from django_sso_app.core.apps.profiles.views import ProfileViewSet as DjangoSSoAppProfileViewSet
from django_sso_app.core.utils import get_profile_model

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
