from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import ProfileViewSet, UserProfileViewSet


urlpatterns = [
    url(r'user/$', UserProfileViewSet.as_view({'get': 'get'})),

    url(r'^$', ProfileViewSet.as_view({'get': 'list'})),
]

urlpatterns = format_suffix_patterns(urlpatterns)

