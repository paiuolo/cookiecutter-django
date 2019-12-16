from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils import timezone
from django.views import defaults as default_views
from django.views.decorators.http import last_modified
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.views.generic.base import RedirectView

# django-sso-app
from django_sso_app.urls import (urlpatterns as django_sso_app__urlpatterns,
                                 api_urlpatterns as django_sso_app__api_urlpatterns,
                                 i18n_urlpatterns as django_sso_app_i18n_urlpatterns)
from django_sso_app.core.mixins import WebpackBuiltTemplateViewMixin

from backend.views import set_language_from_url, StatsView, schema_view  # , SwaggerSchemaView


last_modified_date = timezone.now()
js_info_dict = {}

urlpatterns = []
api_urlpatterns = []
_I18N_URLPATTERNS = []

urlpatterns += django_sso_app__urlpatterns
api_urlpatterns += django_sso_app__api_urlpatterns
_I18N_URLPATTERNS += django_sso_app_i18n_urlpatterns

urlpatterns += [
    # pai
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', last_modified(lambda req, **kw: last_modified_date)(JavaScriptCatalog.as_view()), js_info_dict,
        name='javascript-catalog'),
]

_I18N_URLPATTERNS += [
    path('', WebpackBuiltTemplateViewMixin.as_view(template_name='pages/home.html'), name='home'),
    path('about/', WebpackBuiltTemplateViewMixin.as_view(template_name='pages/about.html'), name='about'),

    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
]

if settings.I18N_PATH_ENABLED:
    urlpatterns += [url(r'^set_language/(?P<user_language>\w+)/$', set_language_from_url, name="set_language_from_url")]
    urlpatterns += i18n_patterns(
        *_I18N_URLPATTERNS
    )
else:
    urlpatterns += _I18N_URLPATTERNS


# Your stuff: custom urls includes go here
urlpatterns += [
    # path('users/', include('django_sso_app.backend.users.urls', namespace='users')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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
    url(r'^api/v1/_stats/$', StatsView.as_view(), name='stats'),

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
