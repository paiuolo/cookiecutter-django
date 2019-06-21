from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone

from django_sso_app.models import AbstractDjangoSsoProfileModel


class Profile(AbstractDjangoSsoProfileModel):
    pass
