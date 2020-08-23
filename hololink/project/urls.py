from django.urls import path
from .views import projects_list, project_detail, create_newproject, project_dashboard, project_articles, project_hologram, galaxy_setting, deliver_D3

app_name = 'project'

urlpatterns = [
     path('', projects_list, name='projects_list'),
     path('create/', create_newproject, name='create_newproject'),
     path('<slug:slug>/', project_dashboard, name='project_dashboard'),
     path('<slug:slug>/articles', project_articles, name='project_articles'),
     path('<slug:slug>/hologram', project_hologram, name='project_hologram'),
     path('<slug:slug>/settings', galaxy_setting, name='galaxy_setting'),
     path('<slug:slug>/deliverd3', deliver_D3, name='deliver_D3')
     
]