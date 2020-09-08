from django.contrib import admin
from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by' ,'last_edited_time']
    filter_horizontal = ('articles_project_owned',)

admin.site.register(Project, ProjectAdmin)
