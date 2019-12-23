from django.contrib.auth.models import AbstractUser
# from django.db.models import CharField
# from django.urls import reverse
# from django.utils.translation import ugettext_lazy as _

from django_sso_app.core.apps.users.models import DjangoSsoAppUserModelMixin


class User(AbstractUser, DjangoSsoAppUserModelMixin):
    pass
    # First Name and Last Name do not cover name patterns
    # around the globe.
    # pai
    # name = CharField(_("Name of User"), blank=True, max_length=255)

    #def get_absolute_url(self):
    #    return reverse("users:detail", kwargs={"username": self.username})
