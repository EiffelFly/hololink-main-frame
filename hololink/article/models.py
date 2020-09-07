from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from project.models import Project
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, pre_delete, post_save
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from unidecode import unidecode
import time

def now():
    return timezone.localtime(timezone.now())


class Article(models.Model):

    hash = models.CharField(
        verbose_name=_('Hash'),
        max_length=128,
        blank=True,
    )

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=256,
        blank=True,
    )
    content = models.TextField(
        verbose_name=_('Content'),
        max_length=262144,
        blank=True,
    )
    from_url = models.URLField(
        verbose_name=_('URL'),
        max_length=1024,
        blank=True,
    )
    recommended = models.BooleanField(
        verbose_name=_('Recommended'),
        default=False,
    )

    created_by = models.ForeignKey(
        verbose_name=_('Created by'),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
    )

    owned_by = models.ManyToManyField(
        User,
        related_name='articles',
        verbose_name='Owned by',
        blank=True,
    )

    created_at = models.DateTimeField(
        verbose_name=_('Created at'),
        null=True,
    )

    tokenize_output = models.JSONField(
        verbose_name=_('Tokenize Output'),
        null=True
    )

    ner_output = models.JSONField(
        verbose_name=_('NER Output'),
        blank=True,
        null=True
    )

    projects = models.ManyToManyField(
        Project,
        related_name='articles',
        verbose_name=_('Projects'),
        blank=True,
    )

    article_basestone_keyword_sum = models.IntegerField(
        verbose_name=_('Basestone Keyword Amount'),
        blank=True,
        default=0
    )

    article_stellar_keyword_sum = models.IntegerField(
        verbose_name=_('Stellar Keyword Amount'),
        blank=True,
        default=0
    )


    final_output = models.JSONField(
        verbose_name=_('Final Output'),
        null=True
    )

    D3_data_format = models.JSONField(
        verbose_name=_('D3 data'),
        null=True
    )

    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)

    def __str__(self):
        return self.name


def slug_generator(sender, instance, *args, **kwargs):
    slug = slugify(instance.name)
    slug = f"{slug}-{instance.hash[:30]}"
    article = Article.objects.filter(slug=slug)
    
    if article.exists():
        slug = f"{slug}-{instance.hash[:30]}-{instance.id}"
    
    instance.slug = slug
    
pre_save.connect(slug_generator, sender=Article, dispatch_uid='generate slug')

