from django.db import models
from django.contrib.auth.models import User
from article.models import Article
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry
from django.urls import reverse
import random

'''
    We want to store extra information in existing User model 
    which is not related to authentication process so we use
    OnetoOneField to connect to user model.
    further information: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
'''

def random_num():
    return User.objects.make_random_password(length=8, allowed_chars='123456789')


class PreAlphaTestToken(models.Model):

    id = models.AutoField(
        verbose_name='Serial Number', primary_key=True,
    )

    token = models.IntegerField(
        verbose_name=_('token'),
        default=random_num,
    )

    used = models.BooleanField(
        verbose_name=_('Used'),
        default=False,
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    user_stellar_keyword_sum = models.IntegerField(
        verbose_name=_('Stellar Keyword Sum'),
        default=0,
        blank=True
    )
    user_basestone_keyword_sum = models.IntegerField(
        verbose_name=_('Stellar Keyword Sum'),
        default=0,
        blank=True
    )

    followings = models.ManyToManyField(
        User,
        related_name='followers',
        verbose_name=_('Followings'),
        blank=True,
    )

    user_stars = models.IntegerField(
        verbose_name=_('User Stars'),
        default=0,
        blank=True
    )

    bio = models.TextField(
        verbose_name=_('Bio'),
        max_length=262144,
        blank=True,
    )

    user_avatar = models.ImageField(
        upload_to='user_avatar',
        blank = True,
    )

    keyword = models.ManyToManyField(
        'article.Keyword',
        related_name='owned_by_user',
        verbose_name=_('Keyword')
    )

    source = models.ManyToManyField(
        'article.Domain',
        related_name='owned_by_user',
        verbose_name=_('Source')
    )

    def get_absolute_url(self):
        return reverse('user_dashboard', args=(self.slug,))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)

   
class Recommendation(models.Model):

    id = models.AutoField(
        verbose_name='Serial Number', primary_key=True,
    )

    user = models.ForeignKey(
        to=User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
    )

    article = models.ForeignKey(
        to=Article,
        verbose_name=_('Article'),
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(
        verbose_name=_('Created at'),
        auto_now_add= True,
    )



'''
    In order to use this kind of method, we are going to define
    "signal" to make model-Profile created/updated when model-User
    created/updated.
'''

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if not getattr(instance, "profile", None):
            Profile.objects.create(user=instance)
        

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()