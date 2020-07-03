from django.urls import path
from .views import project_page

app_name = 'project'

urlpatterns = [
     path('', project_page, name='project_page'),
]