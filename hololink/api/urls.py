from django.urls import path
from .views import ArticleAPIView, ArticleDetaiAPIView

urlpatterns = [
    path('article', ArticleAPIView.as_view(), name='api_article_view'),
    path('article_detail/<int:id>', ArticleDetaiAPIView.as_view(), name='api_article_detail')
]