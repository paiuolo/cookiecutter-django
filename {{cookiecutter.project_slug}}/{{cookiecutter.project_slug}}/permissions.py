import logging

from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger('django')


class PublicObjectOrOwnerOrStaffPermission(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if obj.is_public:
            return True

        user = request.user

        if user.is_staff:
            return True

        return obj.user == user
