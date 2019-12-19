import logging

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from django_sso_app.core.apps.users.models import DjangoSsoAppUserModelMixin

logger = logging.getLogger('backend.users')


class User(AbstractUser, DjangoSsoAppUserModelMixin):

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
