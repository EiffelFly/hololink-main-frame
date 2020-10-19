
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save

from django.dispatch import receiver
from unidecode import unidecode

def get_project_d3_json_default():
    return {"nodes":[],"links":[]}

def get_article_list_default():
    return {"articles":[]}

def get_keyword_list_default():
    return {"total":[],"basestone":[],"stellar":[]}

def now():
    return timezone.localtime(timezone.now())

class Project(models.Model):

    private = 'Private'
    public = 'public'

    PROJECT_VISIBILITY_CHOICES = (
        (private,_('Private')),
        (public, _('Public'))
    )

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=256,
        blank=True,
    )

    description = models.TextField(
        verbose_name=_('Project description'),
        max_length=262144,
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

    last_edited_time = models.DateTimeField(
        verbose_name=_('Last edited time'),
        auto_now=True
    )

    project_basestone_keyword_sum = models.IntegerField(
        verbose_name=_('Basestone Keyword Amount'),
        blank=True,
        null=True,
    )
    
    project_likes = models.IntegerField(
        verbose_name=_('Project Likes'),
        blank=True,
        null=True
    )

    project_stellar_keyword_sum = models.IntegerField(
        verbose_name=_('Stellar Keyword Amount'),
        blank=True,
        null=True,
    )

    project_visibility = models.CharField(
        verbose_name=_('Project Visibility'),
        max_length=100,
        choices=PROJECT_VISIBILITY_CHOICES,
        default='Private',
    )

    project_d3_json = models.JSONField(
        verbose_name=_('D3 data'),
        null=True,
        default=get_project_d3_json_default,
    )

    keyword_list = models.JSONField(
        verbose_name=_('Keyword list'),
        null=True,
        default=get_keyword_list_default,
    )

    keyword = models.ManyToManyField(
        'article.Keyword',
        related_name='owned_by_project',
        verbose_name=_('Keyword')
    )

    ml_is_processing = models.BooleanField(
        default=False,
        verbose_name=_('ML is processing'),
    )

    def __str__(self):
        return self.name

    slug = models.SlugField(null=True, blank=True, max_length=255)


def create_slug(instance, new_slug=None):
    '''
        Recursive function to check whether slug and instance has been created
        Question: whether we need this?

        @receiver(pre_save, sender=Project)
        def slug_generator(sender, instance, *args, **kwargs):
            if not instance.slug:
                instance.slug = create_slug(instance)
    '''
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    querySet = Article.objects.filter(slug=slug).order_by("-id")
    exists = querySet.exists()
    if exists:
        new_slug = f"{slug}-{querySet.first().id}"
        return create_slug(instance, new_slug=new_slug)
    return slug




@receiver(pre_save, sender=Project)
def slug_generator(sender, instance, *args, **kwargs):
    slug = slugify(unidecode(instance.name))
    instance.slug = slug


