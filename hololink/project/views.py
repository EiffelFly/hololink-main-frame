
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from .models import Project
import hashlib

def project_page(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))  
    projects = Project.objects.filter(created_by=request.user)
    print(projects)
    context = {
        'projects': projects,
    }
    return render(request, 'project/project_page.html', context)    
