from django.urls import path
from .views import change_list, add, change, delete, articel_detail

app_name = 'article'

urlpatterns = [
    path('list/', change_list, name='change_list'),
    path('add/', add, name='add'),
    path('<int:id>/change/', change, name='change'),
    path('<int:id>/delete/', delete, name='delete'),
    path('<slug:slug>/', articel_detail, name='article-detail')
]
