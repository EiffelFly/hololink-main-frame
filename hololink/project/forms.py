from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        exclude = ['created_by', 'created_at', 'project_basestone_keyword_sum', 'project_stellar_keyword_sum']