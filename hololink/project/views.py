
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from .models import Project
from .forms import ProjectForm, GalaxySettingsForm
from article.models import Article
from django.db.models import Sum
import hashlib
from django.http import HttpResponseRedirect

def now():
    return timezone.localtime(timezone.now())

def is_valid_queryparam(param):
    return param != '' and param is not None

def filter(request):
    qs = Project.objects.filter(created_by=request.user).order_by('-created_at')
    filterProjectsName = request.GET.get('project_filter')
    print(filterProjectsName)

    if is_valid_queryparam(filterProjectsName):
        qs = qs.filter(name__icontains=filterProjectsName)

    return qs

def projects_list(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))  

    countArticles = []
    projects = filter(request)
    for project in projects:
        countArticles.append(project.articles.count())
    
    context = {
        'projects': projects,
        'countArticles' : countArticles
    }

    return render(request, 'projects_list.html', context)    

def project_detail(request, slug):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))  
    
    project = get_object_or_404(Project, slug=slug, created_by=request.user)
    articles = Article.objects.filter(projects=project)

    #send message to article.views.article_detail
    request.session['user_selected_project'] = project.name
    context = {
        'project' : project, 
        'articles': articles,
    }

    return render(request, 'project_detail.html', context)

def project_articles(request, slug):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))  

    
    project = get_object_or_404(Project, slug=slug, created_by=request.user)
    articles = Article.objects.filter(projects=project).order_by('-created_at')
    basestone = articles.aggregate(Sum('article_basestone_keyword_sum')).get('article_basestone_keyword_sum__sum', 0)
    stellar = articles.aggregate(Sum('article_stellar_keyword_sum')).get('article_stellar_keyword_sum__sum', 0)
    
    countArticles = project.articles.count()

    context = {
        'project' : project, 
        'articles': articles,
        'countArticles':countArticles,
        'data':{'basestone':basestone, 'stellar':stellar}
    }  

    return render(request, 'project_dashboard_articles.html', context)

def project_dashboard(request, slug):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))  
    
    project = get_object_or_404(Project, slug=slug, created_by=request.user)
    articles = Article.objects.filter(projects=project)
    countArticles = project.articles.count()

    context = {
        'project' : project, 
        'articles': articles,
        'countArticles':countArticles,
    }

    return render(request, 'project_dashboard.html', context) 

def project_hologram(request, slug):
    if not request.user.is_authenticated:
        return redirect(reverse('login')) 

    project = get_object_or_404(Project, slug=slug, created_by=request.user)
    articles = Article.objects.filter(projects=project)
    countArticles = project.articles.count()

    context = {
        'project' : project, 
        'articles': articles,
        'countArticles':countArticles,
    }

    return render(request, 'project_dashboard_hologram.html', context) 

@csrf_exempt
def galaxy_setting(request, slug):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    project = get_object_or_404(Project, slug=slug, created_by=request.user)
    confirmation_code = f'{request.user}/{project.name}'
    print(project.project_visibility)

    context = {
        'form': None,
        'tips': [],
        'project':project,
        'confirmation_code':confirmation_code
    }

    if request.method == 'POST':
        form = GalaxySettingsForm(request.POST)
        context['form'] = form
        if form.is_valid():
            if request.POST['action'] == "rename_galaxy":
                project.name = form.cleaned_data.get('name')
                project.save()
                messages.add_message(request, messages.SUCCESS, _('Edited successfully.'))
                return render(request, 'project_dashboard_settings.html', context)

            elif request.POST['action'] == "edit_description":
                project.description = form.cleaned_data.get('galaxy_description')
                project.save()
                messages.add_message(request, messages.SUCCESS, _('Edited successfully.'))
                return render(request, 'project_dashboard_settings.html', context)

            elif request.POST['action'] == "change_galaxy_visibility":
                if form.cleaned_data.get('change_galaxy_visibility_confirmation') == confirmation_code:
                    project.project_visibility = form.cleaned_data.get('galaxy_visibility')
                    project.save()
                    messages.add_message(request, messages.SUCCESS, _('Edited successfully.'))
                    context['form'] = GalaxySettingsForm()
                    return HttpResponseRedirect(reverse('project:galaxy_setting', args=(project.slug,)))
                else:
                    messages.error(request, messages.ERROR, _('Confirmation input not correct'))
                    return render(request, 'project_dashboard_settings.html', context)
            


        
    else:
        form = GalaxySettingsForm()
        form.fields['name'].widget.attrs['placeholder'] = project.name #added placeholder
        form.fields['galaxy_description'].initial = project.description 
        form.fields['galaxy_visibility'].initial = project.project_visibility
        context['form'] = form
        print('i am here')

        return render(request, 'project_dashboard_settings.html', context)


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
                project_visibility=form.cleaned_data.get('galaxy_visibility'),
                created_by=request.user,
                created_at=now(),
            )
            messages.add_message(request, messages.SUCCESS, _('Added successfully.'))
            return redirect(reverse('user_dashboard', kwargs={'slug': request.user.username}))
    else:
        form = ProjectForm()
        context['form'] = form
        context['tips'] += [_('Fill in the following form to create a new project.')]
    return render(request, 'create_new_project_test.html', context)