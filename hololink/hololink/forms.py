from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class UserSettingsForm(forms.ModelForm):

    username = forms.CharField(
        label=_('Username'),
        required = False,
        widget=forms.TextInput(
            attrs={
                'style':'',
                'autocomplete':'off',
            },
        ),
    )

    bio = forms.CharField(
        label=_('Bio'),
        required = False,
        widget=forms.Textarea(
            attrs={
                'style':'',
                'autocomplete':'off',
                'rows':3,
            },
        ),
    )

    avatar = forms.ImageField(
        label=_('Avatar'),
        required = False,
        widget = forms.FileInput(
            attrs={
                'class':'imageInput'
            }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'bio', 'avatar']