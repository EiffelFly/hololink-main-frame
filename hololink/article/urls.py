from django.urls import path
from .views import change_list, add, change, delete

app_name = 'article'

urlpatterns = [
    path('', change_list, name='change_list'),
    path('add/', add, name='add'),
    path('<int:id>/change/', change, name='change'),
    path('<int:id>/delete/', delete, name='delete'),
]
