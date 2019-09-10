from django.conf import settings
from django.urls import include, path
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

# pai
from django.utils import timezone
from django.views.decorators.http import last_modified
from django.views.i18n import JavaScriptCatalog

from backend.views import SwaggerSchemaView, APIRoot, StatsView, AuthAPIRoot

from django_sso_app.core.apps.profiles.urls import urlpatterns as profiles_urls
from django_sso_app.core.apps.groups.urls import urlpatterns as groups_urls


last_modified_date = timezone.now()
js_info_dict = {}


urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% raw %}{% url 'admin:index' %}{% endraw %}
    path(settings.ADMIN_URL, admin.site.urls),

    # pai
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', last_modified(lambda req, **kw: last_modified_date)(JavaScriptCatalog.as_view()), js_info_dict,
        name='javascript-catalog'),
]

urlpatterns += [
    # User management
    path("users/", include("backend.users.urls", namespace="users")),
]

if settings.DJANGO_ALLAUTH_ENABLED:
    urlpatterns += [
        path("accounts/", include("allauth.urls")),
    ]

# Your stuff: custom urls includes go here
urlpatterns += []

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

# pai
sso_auth_urlpatterns = [
    url(r'^api/v1/auth/profiles/', include((profiles_urls, 'profiles'), namespace="profile")),
    url(r'^api/v1/auth/groups/', include((groups_urls, 'groups'), namespace="group")),
]

api_urlpatterns = sso_auth_urlpatterns + [
    url(r'^api/v1/_stats/$', StatsView.as_view(), name="stats"),

    # your api here
]

urlpatterns += api_urlpatterns

urlpatterns += [
    url(r'^api/v1/auth/', AuthAPIRoot.as_view(), name='authapi'),

    url(r'^api/v1/ui/$', APIRoot.as_view(), name="drf"),
    url(r'^api/v1/$', SwaggerSchemaView.as_view(patterns=api_urlpatterns), name="swagger")
]

