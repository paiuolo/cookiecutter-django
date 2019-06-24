from rest_framework import viewsets
from rest_framework import permissions

from .models import Group
from .serializers import GroupSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    lookup_field = 'pk'

    def list(self, request):
        """
        List
        """
        return super(GroupViewSet, self).list(request)

    def retrieve(self, request, pk=None):
        """
        Detail
        """
        return super(GroupViewSet, self).retrieve(request, pk)
