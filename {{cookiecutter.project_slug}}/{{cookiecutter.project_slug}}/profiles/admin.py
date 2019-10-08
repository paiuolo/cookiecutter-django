from django.contrib import admin

from django_sso_app.core.utils import get_profile_model

Profile = get_profile_model()


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('id', 'user__username', 'sso_id')
    list_display = ('sso_id', 'created_at')

admin.site.register(Profile, ProfileAdmin)
