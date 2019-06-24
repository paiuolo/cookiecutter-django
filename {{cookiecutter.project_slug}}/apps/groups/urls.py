from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import GroupViewSet


urlpatterns = [
    url(r'^group/$', GroupViewSet.as_view({'get': 'list'}), name="list"),
    url(r'^group/(?P<pk>[0-9A-Fa-f-]+)/$', GroupViewSet.as_view({'get': 'retrieve'}), name="detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
