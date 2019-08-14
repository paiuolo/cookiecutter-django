from rest_framework import viewsets
from rest_framework import permissions

from .models import Group
from .serializers import GroupSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    lookup_field = 'pk'

    def list(self, request, *args, **kwargs):
        """
        List groups
        """
        return super(GroupViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Group detail
        """
        return super(GroupViewSet, self).retrieve(request, pk, *args, **kwargs)
