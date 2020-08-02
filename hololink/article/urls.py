from django.urls import path
from .views import change_list, add, change, delete, article_detail, articles_list

app_name = 'article'

urlpatterns = [
    path('list-test/', change_list, name='change_list'),
    path('add/', add, name='add'),
    path('<int:id>/change/', change, name='change'),
    path('<int:id>/delete/', delete, name='delete'),
    path('list/', articles_list, name='articles_list'),
    path('<slug:slug>/', article_detail, name='article_detail'),
    
]
