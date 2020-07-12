from django.urls import path, include
from django.contrib import admin
from .views import index, d3demo, user_dashboard
from rest_framework import routers
from api import views


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('article/', include('article.urls')),
    path('project/', include('project.urls')),
    path('', index, name='index'),
    path('d3demo/', d3demo, name='d3demo'),
    #path('<username>', user_dashboard, name='user_dashboard')
]


router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('groups', views.GroupViewSet)
router.register('articles', views.ArticleViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns += [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api_test/', include('api.urls'))
]
