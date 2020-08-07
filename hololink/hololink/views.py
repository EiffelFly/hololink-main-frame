from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from accounts.forms import SignUpWithEmailForm
from django.core.mail import send_mail
from django.conf import settings
from project.models import Project
from accounts.models import Profile
from django.contrib.auth.models import User
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db.models import Sum


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
    
    profile = get_object_or_404(Profile, user=request.user)
    user = get_object_or_404(User, username=request.user)

    countArticles = []
    projects = Project.objects.filter(created_by=request.user).order_by('-last_edited_time') #use -created_at to desc()
    projects = projects[:4]
    for project in projects:
        countArticles.append(project.articles.count())

    countFollowings = profile.followings.count()
    countFollowers = user.followers.count()
    countlikes = projects.aggregate(Sum('project_likes')).get('project_likes__sum', 0)

    context = {
        'profile' : profile,
        'projects' : projects,
        'countArticles' : countArticles,
        'countFollowings' : countFollowings,
        'countFollowers' : countFollowers,
        'countlikes' : countlikes,
    }

    return render(request, 'user_dashboard.html', context) 

def user_public_profile(request, slug):
    
    '''
        BE CAREFUL!! This section is user public area, can't let any not aloowed info leak out.
    '''
    countArticles = []
    projects = Project.objects.filter(created_by=request.user).filter(project_visibility='Public').order_by('-last_edited_time') #use -created_at to desc()
    projects = projects[:4]
    for project in projects:
        countArticles.append(project.articles.count())


    context = {
        'projects': projects,
        'countArticles' : countArticles
    }

    return render(request, 'user_dashboard.html', context) 


def explore(request):
    projects = Project.objects.filter(project_visibility='Public')
    project_sortby_likes = projects.order_by('-project_likes')
    


    context = {
        'project_sortby_likes':project_sortby_likes,
        'projects':projects
    }

    return render(request, 'explore.html', context) 

def explore_users(request):
    '''
        BE CAREFUL! This will demo some user public info.
    '''
    #profiles = Profile.objects.all()

    profile = Profile.objects.all().order_by('-followers')

    context = {
        'profile':profile,
    }
    
    return render(request, 'explore_users.html', context)

def user_settings(request, slug):
    profile = get_object_or_404(Profile, user=request.user)

    context = {
        'profile' : profile,
    }

    return render(request, 'user_settings.html', context)
