from django import forms
from .models import Project
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class ProjectForm(forms.ModelForm):

    name = forms.CharField(
        label=_('Galaxy name'),
        required = True,
        widget=forms.TextInput(
            attrs={
                'style':''
            },
        ),
    )

    def clean_name(self):
        name = self.cleaned_data['name']
        if Project.objects.filter(name=name).exists():
            self.add_error(
                'name',
                ValidationError(
                    _('The project name has already been used.'),
                    code='invalid'
                )
            )
        return name

    private = forms.BooleanField(
        label=_('Private')
    )

    public = forms.BooleanField(
        label=_('Public')
    )

    class Meta:
        model = Project
        exclude = ['created_by', 'created_at', 'project_basestone_keyword_sum', 'project_stellar_keyword_sum', 'slug']