from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class UserSettingsFormForPublicProfile(forms.ModelForm):

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

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username.isspace() is True:
            self.add_error(
                'username',
                ValidationError(
                    _("Username can't be empty nor whitespaces"),
                    code='invalid'
                )
            )
        return username