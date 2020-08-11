from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
import uuid
from .forms import SignUpWithEmailForm
from django.contrib.auth.views import LoginView
from smtplib import SMTPException

from .emailverification import verifyToken
from .errors import NotAllFieldCompiled






class CustomLoginView(LoginView):
    '''
    Inherit Login View to redirect to custom url
    ''' 
    #template_name = 'login.html' 
    redirect_field_name = None
    
    def get_success_url(self):
        url = self.get_redirect_url() #method essential
        return url or reverse('user_dashboard', kwargs={'slug': self.request.user.username})

def sign_up(request):
    """
    A lobby view of sign-up view.
    """
    context = {}
    return render(request, 'registration/sign_up.html', context)


def sign_up_with_account_password(request):
    """
    A standard sign-up view.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/sign_up_with_account_password.html', context)


def sign_up_with_email(request):
    """
    A sign-up view for user.
    An user provides a Email and we use its prefix as username
    and generate a random uuid string as password.
    We then send a Email containing these info to users.
    """
    if request.method == 'POST': 
        form = SignUpWithEmailForm(request.POST) 
        if form.is_valid():
            # Create a user and save it to DB.
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            user = form.save(commit=False)
            user.username = username
            random_uuid_password = uuid.uuid4().hex[0:6]
            user.set_password(random_uuid_password)
            
            user.save()
            # Send a login info Email.
            subject = "[Hololink] You have created an account."
            message = (
                f'Hi {username},\n'
                '\n'
                'You have created a new account on Hololink. You could login and change it on Hololink later.\n'
                '\n'
                f'Your account: {email}\n'
                f'Your password: {random_uuid_password}\n'
                '\n'
                'Sincerely,\n'
                'Hololink\n'
            )
            #using sendgrid as SMTP server
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except SMTPException as e:
                print('There was an error sending an email: ', e) 

            print(email)
            return redirect(reverse('password_reset_done'))
    else: 
        form = SignUpWithEmailForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/sign_up_with_email.html', context)

def verify(request, email, emailToken):
    try:
        template = settings.EMAIL_PAGE_TEMPLATE
        return render(request, template, {'success': verifyToken(email, emailToken)})
    except AttributeError:
        raise NotAllFieldCompiled('EMAIL_PAGE_TEMPLATE field not found')
