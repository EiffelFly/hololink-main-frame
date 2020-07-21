
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from .models import Project
from article.models import Article
import hashlib

def is_valid_queryparam(param):
    return param != '' and param is not None

def filter(request):
    qs = Project.objects.filter(created_by=request.user).order_by('-created_at')
    filterProjectsName = request.GET.get('project-filter')

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
    context = {
        'project' : project, 
        'articles': articles,
    }

    print(articles)
    

    return render(request, 'project_detail.html', context) 