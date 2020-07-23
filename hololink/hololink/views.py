from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from accounts.forms import SignUpWithEmailForm
from django.core.mail import send_mail
from django.conf import settings
from project.models import Project
from accounts.models import Profile
import uuid
from project.forms import ProjectForm
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib import messages
from django.utils.translation import gettext as _


def now():
    return timezone.localtime(timezone.now())

def d3demo(request):
    return render(request, 'd3demo.html')


# a email-sending script, not a view
def send_password_email(subject, message, recipient):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
    except Exception as e:
        print(e)


def index(request):
    if request.method == 'POST':
        form = SignUpWithEmailForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data.get('email')
            username = email[0:email.index('@')]
            user.username = username
            random_uuid_password = uuid.uuid4().hex[0:6]
            user.set_password(random_uuid_password)
            user.save()
            # send a random uuid password email
            recipient = f'{email}'
            subject = "[Hololink] You have created an account."
            try:
                if '_' in username:
                    username_readable = ' '.join([word[0].upper() + word[1:] for word in username.split('_')])
                else:
                    username_readable = username
            except Exception:
                username_readable = username
            message = f'Hi {username_readable},'
            message += '\n\nYou have created a new account on Hololink. Login and learn more!'
            message += f'\n\nYour account: {username}'
            message += f'\nYour password: {random_uuid_password}'
            message += '\n\nSincerely,'
            message += '\nHololink'
            send_password_email(
                subject=subject,
                message=message,
                recipient=recipient,
            )
            return redirect('/accounts/password_reset/done/')
    else:
        form = SignUpWithEmailForm()
    context = {
        'form': form,
    }
    
    return render(request, 'landing_page.html', context)
    

def user_dashboard(request, slug):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    
    
    countArticles = []
    projects = Project.objects.filter(created_by=request.user).order_by('-created_at') #use -created_at to desc()
    projects = projects[:4]
    for project in projects:
        countArticles.append(project.articles.count())


    context = {
        'projects': projects,
        'countArticles' : countArticles
    }

    return render(request, 'user_dashboard.html', context) 

@csrf_exempt
def create_newproject(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    context = {
        'form': None,
        'tips': []
    }

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        context['form'] = form
        if form.is_valid():
            project = Project.objects.create(
                name=form.cleaned_data.get('name'),
                private_project=form.cleaned_data.get('name'),
                created_by=request.user,
                created_at=now(),
            )
            messages.add_message(request, messages.SUCCESS, _('Added successfully.'))
    else:
        form = ProjectForm()
        context['form'] = form
        context['tips'] += [_('Fill in the following form to create a new project.')]
    return render(request, 'create_new_project.html', context)

