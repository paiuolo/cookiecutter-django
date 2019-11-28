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
from django.conf.urls.i18n import i18n_patterns

from backend.views import StatsView, schema_view  # , SwaggerSchemaView

last_modified_date = timezone.now()
js_info_dict = {}

urlpatterns = []
api_urlpatterns = []
_I18N_URLPATTERNS = []

# django-sso-app
if settings.DJANGO_SSO_APP_BACKEND_ENABLED:
    from django_sso_app.backend.settings.base import DJANGO_SSO_APP_BACKEND_I18N_PATH_ENABLED
    from django_sso_app.backend.urls import django_sso_app_urlpatterns, django_sso_app_i18n_urlpatterns, \
                                            django_sso_app_api_urlpatterns
    from django_sso_app.core.views import WebpackBuiltTemplateView
    from django_sso_app.core.apps.profiles.views import ProfileView, ProfileUpdateView

    urlpatterns += django_sso_app_urlpatterns
    api_urlpatterns += django_sso_app_api_urlpatterns
    _I18N_URLPATTERNS += [
        path('profile/', ProfileView.as_view(), name='profile'),
        path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
    ]

elif settings.DJANGO_SSO_APP_ENABLED:
    from django_sso_app.app.urls import django_sso_app_api_urlpatterns

    api_urlpatterns += django_sso_app_api_urlpatterns

elif settings.DJANGO_ALLAUTH_ENABLED:
    urlpatterns += [
        path('accounts/', include('allauth.urls')),
        # ! add social
    ]
else:
    class WebpackBuiltTemplateView(TemplateView):
        pass


urlpatterns += [
    # pai
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', last_modified(lambda req, **kw: last_modified_date)(JavaScriptCatalog.as_view()), js_info_dict,
        name='javascript-catalog'),
]

_I18N_URLPATTERNS += [
    path('', WebpackBuiltTemplateView.as_view(template_name='pages/home.html'), name='home'),
    path('about/', WebpackBuiltTemplateView.as_view(template_name='pages/about.html'), name='about'),

    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
] + django_sso_app_i18n_urlpatterns


if settings.DJANGO_SSO_APP_BACKEND_ENABLED:
    if DJANGO_SSO_APP_BACKEND_I18N_PATH_ENABLED:
        urlpatterns += i18n_patterns(
            *_I18N_URLPATTERNS
        )
    else:
        urlpatterns += _I18N_URLPATTERNS
else:
    urlpatterns += _I18N_URLPATTERNS

# Your stuff: custom urls includes go here
urlpatterns += [
    # path('users/', include('django_sso_app.backend.users.urls', namespace='users')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DJANGO_SSO_APP_BACKEND_ENABLED:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django_sso_app.backend.settings.base import DJANGO_SSO_APP_BACKEND_STANDALONE
    if DJANGO_SSO_APP_BACKEND_STANDALONE:
        urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            '400/',
            default_views.bad_request,
            kwargs={'exception': Exception('Bad Request!')},
        ),
        path(
            '403/',
            default_views.permission_denied,
            kwargs={'exception': Exception('Permission Denied')},
        ),
        path(
            '404/',
            default_views.page_not_found,
            kwargs={'exception': Exception('Page not Found')},
        ),
        path('500/', default_views.server_error),
    ]

    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns


api_urlpatterns += [
    url(r'^api/v1/_stats/$', StatsView.as_view(), name="stats"),

    # your api here
]

urlpatterns += api_urlpatterns

urlpatterns += [
    url(r'^api/v1/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^api/v1/(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # url(r'^api/v1/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

for lang, _name in settings.LANGUAGES:
    urlpatterns.append(url(r'^{}/login/$'.format(lang), RedirectView.as_view(url='/login/', permanent=False)))
    urlpatterns.append(url(r'^{}/signup/$'.format(lang), RedirectView.as_view(url='/signup/', permanent=False)))
