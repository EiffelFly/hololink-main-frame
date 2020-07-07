
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
    )

    project_have_article = models.ManyToManyField(
        to='article.Article',
        verbose_name=_('Articles'),
        blank=True,
    )

    project_basestone_keyword_sum = models.IntegerField(
        verbose_name=_('Basestone Keyword Amount'),
        blank=True,
    )

    project_stellar_keyword_sum = models.IntegerField(
        verbose_name=_('Stellar Keyword Amount'),
        blank=True,
    )

    def __str__(self):
        return self.name