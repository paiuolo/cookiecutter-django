from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import ProfileViewSet, UserProfileViewSet


urlpatterns = [
    url(r'profiles/$', ProfileViewSet.as_view({'get': 'list'}), name="profiles-list"),
    url(r'profiles/(?P<user_id>[0-9A-Fa-f-]+)/$', UserProfileViewSet.as_view({'get': 'get'}), name="profiles-detail"),

    url(r'^groups/$', GroupViewSet.as_view({'get': 'list'}), name="group-list"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
