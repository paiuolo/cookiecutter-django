from django.conf import settings
from django.urls import include, path
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.contrib.auth.decorators import login_required

# pai
from django.utils import timezone
from django.views.decorators.http import last_modified
from django.views.i18n import JavaScriptCatalog

from backend.views import SwaggerSchemaView, APIRoot, StatsView

# django-sso-app
if settings.DJANGO_SSO_BACKEND_ENABLED:
    from django_sso_app.backend.config.urls.allauth import allauth_urlpatterns
    from django_sso_app.backend.config.urls.rest_auth import rest_auth_urlpatterns
    from django_sso_app.backend.config.urls.sso import sso_app_urlpatterns
elif settings.DJANGO_SSO_APP_ENABLED:
    from django_sso_app.backend.config.urls.sso import sso_app_urlpatterns

# add there

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

# pai
api_urlpatterns = []
if settings.DJANGO_SSO_BACKEND_ENABLED:
    urlpatterns += allauth_urlpatterns
    api_urlpatterns += rest_auth_urlpatterns
elif settings.DJANGO_ALLAUTH_ENABLED:
    urlpatterns += [
        path("accounts/", include("allauth.urls")),
        # ! add social
    ]
if settings.DJANGO_SSO_BACKEND_ENABLED or settings.DJANGO_SSO_APP_ENABLED:
    api_urlpatterns += sso_app_urlpatterns


# Your stuff: custom urls includes go here

urlpatterns += [
    # User management
    path("users/", include("backend.users.urls", namespace="users")),
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

api_urlpatterns += [
    url(r'^api/v1/_stats/$', StatsView.as_view(), name="stats"),

    # your api here
]

if settings.DJANGO_SSO_APP_ENABLED and settings.DJANGO_SSO_APP_HAS_CUSTOM_USER_PROFILE:
    from backend.profiles.urls import urlpatterns as profiles_urls
    api_urlpatterns += [
        url(r'^api/v1/profiles/', include((profiles_urls, 'profiles'), namespace="profile")),
        # your api here
    ]

urlpatterns += api_urlpatterns

urlpatterns += [
    url(r'^api/v1/ui/$', APIRoot.as_view(), name="drf"),
    url(r'^api/v1/$', SwaggerSchemaView.as_view(patterns=api_urlpatterns), name="swagger"),

    # add there
]

-"""
-if settings.DJANGO_SSO_BACKEND_ENABLED:
-    urlpatterns += [
-        url(r'^api/v1/auth/', AuthAPIRoot.as_view(), name='authapi'),
-    ]
-"""
