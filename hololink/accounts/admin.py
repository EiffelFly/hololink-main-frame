from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from .models import Profile, Recommendation, PreAlphaTestToken



'''
    Because model Profile is not in the original django.admin so 
    we need to recreate by ourself.
    more information: https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#extending-the-existing-user-model
'''

# Define an inline admin descriptor for Profile model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    filter_horizontal = ('followings',)
    #verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'article', 'created_at']

class PreAlphaTestTokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'token']

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Recommendation, RecommendationAdmin)
admin.site.register(PreAlphaTestToken, PreAlphaTestTokenAdmin)