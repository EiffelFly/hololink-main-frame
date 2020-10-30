from django.urls import path
from .views import change_list, add, change, delete, article_detail, articles_list, deliver_D3

app_name = 'article'

urlpatterns = [
    path('', articles_list, name='articles_list'),
    path('list-test/', change_list, name='change_list'),
    path('add/', add, name='add'),
    path('<int:id>/change/', change, name='change'),
    path('<int:id>/delete/', delete, name='delete'),   
    path('<slug:articlenameslug>/', article_detail, name='article_detail'),
    path('<slug:articlenameslug>/deliverd3', deliver_D3, name='deliver_D3'),
]
