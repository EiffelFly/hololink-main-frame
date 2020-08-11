from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class SignUpWithEmailForm(forms.ModelForm):

    email = forms.EmailField(
        label=_('Email'),
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': _('Email'),
            },
        ),
    )

    username = forms.CharField(
        label=_('Username'),
        required = True,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Username'),
            },
        ),
    )

    password = forms.CharField(
        label=_('Password1'),
        required = True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':_('Password')
            }
        )
    )

    confirm_password = forms.CharField(
        label=_('Confirm password'),
        required = True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':_('Confirm')
            }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError(
                    _('The Email has already been used.'),
                    code='invalid'
                )
            )
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            self.add_error(
                'username',
                ValidationError(
                    _('The Username has already been used.'),
                    code='invalid'
                )
            )
        return username

class EmailValidationOnForgotPassword(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError(
                    _('There is no user registered with this Email.'),
                    code='invalid'
                )
            )
        return email
