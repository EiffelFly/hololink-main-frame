from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class UserSettingsForm(forms.ModelForm):

    name = forms.CharField(
        label=_('User Name'),
        required = False,
        widget=forms.TextInput(
            attrs={
                'style':'',
                'autocomplete':'off',
            },
        ),
    )

    bio = forms.CharField(
        label=_('User Bio'),
        required = False,
        widget=forms.Textarea(
            attrs={
                'style':'',
                'autocomplete':'off',
                'rows':3,
            },
        ),
    )

    avatar = forms.imagefield(
        upolads_to='user_avatar'
        required = False,
        widget = forms.FileInput(
            attrs={
                'style'='',
            }
        )
    )

    class Meta:
        model = User
        fields = ['name', 'bio', 'avatar']