
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Project(models.Model):

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=256,
        blank=True,
    )
