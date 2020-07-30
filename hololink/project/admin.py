from django.contrib import admin
from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_edited_time']
    filter_horizontal = ('articles',)

admin.site.register(Project, ProjectAdmin)
