from django.urls import path
from .views import article_list

urlpatterns = [
    path('article', article_list, name='article_api_view')
]