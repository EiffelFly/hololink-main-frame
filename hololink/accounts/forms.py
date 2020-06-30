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

    class Meta:
        model = User
        fields = ['email']

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
