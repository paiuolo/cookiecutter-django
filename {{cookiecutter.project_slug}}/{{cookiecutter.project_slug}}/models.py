from django.db import models
from django.utils.translation import ugettext_lazy as _


class UpdatableModel(models.Model):
    class Meta:
        abstract = True

    updated_at = models.DateTimeField(_("created at"), auto_now=True)


class UserRelatedModel(models.Model):
    class Meta:
        abstract = True

    is_public = models.BooleanField(default=False)


class TimespanModel(models.Model):
    class Meta:
        abstract = True

    started_at = models.DateTimeField(_("started at"))

    ended_at = models.DateTimeField(_("ended at"))
