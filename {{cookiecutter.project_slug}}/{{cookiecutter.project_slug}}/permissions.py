import logging

from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger('django')


def is_staff(user):
    return user and (user.is_staff or user.groups.filter(name='staff').count() > 0)


class PublicObjectOrOwnerOrStaffPermission(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        user = request.user
        user_is_staff = is_staff(user)

        if user_is_staff:
            return True

        is_public = getattr(obj, 'is_public', False)
        has_owner = getattr(obj, 'user', False)

        if (is_public and not has_owner) and not user_is_staff:
            return False

        if is_public:
            return True

        obj_user = getattr(obj, 'user', None)

        return obj_user == user
