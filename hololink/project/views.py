
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from .models import Project
from .forms import ProjectForm
from article.models import Article
import hashlib

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
    request.session['user_selected_project'] = project.slug
    context = {
        'project' : project, 
        'articles': articles,
    }

    print(articles)
    

    return render(request, 'project_detail.html', context) 

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
                project_visibility=form.cleaned_data.get('project_visibility'),
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