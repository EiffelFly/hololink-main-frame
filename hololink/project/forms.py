from django import forms
from .models import Project
from article.models import Article
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class DeleteArticleForm(forms.ModelForm):

    name = forms.CharField(
        label=_('Article name'),
        required = False,
        widget=forms.TextInput(
            attrs={
                'style':'',
                'autocomplete':'off',
            },
        ),
    )

    class Meta:
        model = Article
        fields = ['name']


class ProjectForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProjectForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        label=_('Galaxy Name'),
        required = True,
        widget=forms.TextInput(
            attrs={
                'style':'',
                'autocomplete':'off',
            },
        ),
    )

    galaxy_description = forms.CharField(
        label=_('Galaxy Description'),
        required = False,
        widget=forms.Textarea(
            attrs={
                'style':'',
                'autocomplete':'off',
                'rows':3,
            },
        ),
    )

    galaxy_visibility = forms.ChoiceField(
        required=True,
        label=_('Galaxy Visibility'),
        choices=Project.PROJECT_VISIBILITY_CHOICES,
        initial='Private',
        widget=forms.RadioSelect(
            choices=Project.PROJECT_VISIBILITY_CHOICES,
            attrs={
                'class':'custom-radio-list'
            }
            
        )
    )

    

    def clean_name(self):
        name = self.cleaned_data['name']
        if Project.objects.filter(name=name, created_by=self.user).exists():
            self.add_error(
                'name',
                ValidationError(
                    _('The project name has already been used.'),
                    code='invalid'
                )
            )
        return name

    class Meta:
        model = Project
        fields = ['name', 'galaxy_description', 'galaxy_visibility']


class GalaxySettingsForm(forms.ModelForm):
    name = forms.CharField(
        label=_('Galaxy Name'),
        required = False,
        widget=forms.TextInput(
            attrs={
                'style':'',
                'autocomplete':'off',
                'id':'rename_galaxy_input'
            },
        ),
    )

    galaxy_description = forms.CharField(
        label=_('Galaxy Description'),
        required = False,
        widget=forms.Textarea(
            attrs={
                'style':'',
                'autocomplete':'off',
                'rows':3,
                'id':'edit_galaxy_description_input',
            },
        ),
    )

    galaxy_visibility = forms.ChoiceField(
        required=False,
        label=_('Galaxy Visibility'),
        choices=Project.PROJECT_VISIBILITY_CHOICES,
        widget=forms.RadioSelect(
            choices=Project.PROJECT_VISIBILITY_CHOICES,
            attrs={
                'class':'custom-radio-list'
            }
            
        )
    )

    change_galaxy_visibility_confirmation = forms.CharField(
        required=False,
        label=_('Change galaxy visibility confirmation'),
        widget=forms.TextInput(
            attrs={
                'style':'',
                'autocomplete':'off',
            },
        ),

    )

    delete_galaxy_confirmation = forms.CharField(
        required=False,
        label=_('Delete galaxy confirmation'),
        widget=forms.TextInput(
            attrs={
                'style':'',
                'autocomplete':'off',
            },
        ),
    )

    class Meta:
        model = Project
        fields = ['name', 'galaxy_description', 'galaxy_visibility', 'change_galaxy_visibility_confirmation', 'delete_galaxy_confirmation']


