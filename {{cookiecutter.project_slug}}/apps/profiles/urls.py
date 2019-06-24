from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import ProfileViewSet


urlpatterns = [
    url(r'^profile/$', ProfileViewSet.as_view({'get': 'list'}), name="list"),
    url(r'^profile/(?P<pk>[0-9A-Fa-f-]+)/$', ProfileViewSet.as_view({'get': 'retrieve'}), name="detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
