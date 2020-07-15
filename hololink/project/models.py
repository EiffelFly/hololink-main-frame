
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

def now():
    return timezone.localtime(timezone.now())

class Project(models.Model):

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=256,
        blank=True,
    )

    created_at = models.DateTimeField(
        verbose_name=_('Created at'),
        auto_now_add=True
    )

    created_by = models.ForeignKey(
        verbose_name=_('Created by'),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=None
    )

    project_articles_sum = models.IntegerField(
        verbose_name=_("Amount of Project's articles"),
        blank=True,
        null=True,
    )


    project_basestone_keyword_sum = models.IntegerField(
        verbose_name=_('Basestone Keyword Amount'),
        blank=True,
        null=True,
    )
    

    project_stellar_keyword_sum = models.IntegerField(
        verbose_name=_('Stellar Keyword Amount'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name