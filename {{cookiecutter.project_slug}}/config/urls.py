from django.conf import settings
from django.urls import include, path
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views import defaults as default_views
from django.contrib.auth.decorators import login_required

# pai
from django.utils import timezone
from django.views.decorators.http import last_modified
from django.views.i18n import JavaScriptCatalog

from backend.views import SwaggerSchemaView, APIRoot, StatsView, set_language_from_url
from backend.profiles.views import ProfileView, ProfileUpdateView

from django_sso_app.core.settings.common import DJANGO_SSO_APP_BACKEND_ENABLED, DJANGO_SSO_APP_ENABLED
if DJANGO_SSO_APP_BACKEND_ENABLED:
    from django_sso_app.backend.settings import DJANGO_SSO_APP_BACKEND_STANDALONE
    from django_sso_app.core.urls.django_sso_app import django_sso_app_urlpatterns
    from django_sso_app.core.urls.django_sso_app import django_sso_app_api_urlpatterns
elif DJANGO_SSO_APP_ENABLED:
    from django_sso_app.core.urls.django_sso_app import django_sso_app_urlpatterns

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

    path("profile/", ProfileView.as_view(), name="profile"),
    url(r'^profile/update/$', ProfileUpdateView.as_view(), name='profile_update'),

    # pai
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', last_modified(lambda req, **kw: last_modified_date)(JavaScriptCatalog.as_view()), js_info_dict,
        name='javascript-catalog'),
    url(r'^set_language/(?P<user_language>\w+)/$', set_language_from_url, name="set_language_from_url"),
]

# pai
api_urlpatterns = []

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

# pai
if DJANGO_SSO_APP_BACKEND_ENABLED or DJANGO_SSO_APP_ENABLED:
    urlpatterns += django_sso_app_urlpatterns
    api_urlpatterns += django_sso_app_api_urlpatterns
elif settings.DJANGO_ALLAUTH_ENABLED:
    urlpatterns += [
        path("accounts/", include("allauth.urls")),
        # ! add social
    ]

urlpatterns += api_urlpatterns

urlpatterns += [
    url(r'^api/v1/ui/$', APIRoot.as_view(), name="drf"),
    url(r'^api/v1/$', SwaggerSchemaView.as_view(patterns=api_urlpatterns), name="swagger"),

    # add there
]

for lang, _name in settings.LANGUAGES:
    urlpatterns.append(url(r'^{}/login/$'.format(lang), RedirectView.as_view(url='/login/', permanent=False)))
    urlpatterns.append(url(r'^{}/signup/$'.format(lang), RedirectView.as_view(url='/signup/', permanent=False)))
