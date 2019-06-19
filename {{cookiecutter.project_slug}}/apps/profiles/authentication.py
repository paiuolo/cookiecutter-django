from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.conf import settings
import logging


logger = logging.getLogger('profiles.authentication')

username_header = getattr(settings, 'SSO_HEADER', 'HTTP_X_CONSUMER_USERNAME')
anonymous_username = getattr(settings, 'SSO_ANONYMOUS_USERNAME', 'anonymous')

class ProfilesAuthentication(JSONWebTokenAuthentication):
    def authenticate(self, request):
        username = request.META.get(username_header, None)

        if username == anonymous_username:
            logger.info('Anonymous username header set, can not authenticate')
            return None
        else:
            return super(ProfilesAuthentication, self).authenticate(request)
