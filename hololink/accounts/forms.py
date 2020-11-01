from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from accounts.models import PreAlphaTestToken

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

    token = forms.CharField(
        label=_('Token'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Access Token'),
            },
        ),

    )

    password = forms.CharField(
        label=_('Password'),
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
        fields = ['username', 'email', 'token', 'password', 'confirm_password']

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
    
    def clean_token(self):
        token = self.cleaned_data['token']

        if not token.isdigit():
            self.add_error(
                'token',
                ValidationError(
                    _('The token is invalid.'),
                    code='invalid'
                )
            )
        else:
            try:
                target_token = PreAlphaTestToken.objects.get(token=token)
                if target_token.used == True:
                    self.add_error(
                    'token',
                    ValidationError(
                        _('The token has already been used.'),
                        code='invalid'
                    )
                )
            except PreAlphaTestToken.DoesNotExist:
                self.add_error(
                    'token',
                    ValidationError(
                        _('The token is invalid.'),
                        code='invalid'
                    )
                )
                
        return token
        

    def clean(self):
        '''
            If we want to valid field depend on other field
            ref:https://docs.djangoproject.com/en/3.0/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
        '''
        cleaned_data = super().clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error(
                'confirm_password',
                ValidationError(
                    _("Those passwords didn't match. Please try again")
                )
            )
            self.add_error(
                'password',
                ValidationError(
                    ("")
                )
            )
        if password.length < 8:
            self.add_error(
                'password',
                ValidationError(
                    ("Use 8 characters or more for your password")
                )
            )
        
        
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
