from django.urls import path
from .views import projects_list, project_detail, create_newproject

app_name = 'project'

urlpatterns = [
     path('', projects_list, name='projects_list'),
     path('create/', create_newproject, name='create_newproject'),
     path('<slug:slug>/', project_detail, name='project_detail'),
     
]