
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from .models import Project
from article.models import Article
import hashlib


def projects_list(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))  
    projects = Project.objects.filter(created_by=request.user).order_by('-created_at')
    context = {
        'projects': projects,
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