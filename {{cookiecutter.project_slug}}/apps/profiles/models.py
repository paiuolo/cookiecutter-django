from django.urls import reverse

from django_sso_app.models import AbstractDjangoSsoProfileModel


class Profile(AbstractDjangoSsoProfileModel):
    def get_absolute_url(self):
        return reverse("profiles:detail", args=[self.sso_id])
