from django.urls import path, include
from django.contrib import admin
from .views import index, d3demo, user_dashboard, user_public_profile, explore, explore_users, user_settings, user_settings_account, user_source
from rest_framework import routers
from api import views
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('@<slug:usernameslug>/articles/', include('article.urls')),
    path('@<slug:usernameslug>/projects/', include('project.urls')),
    path('', index, name='index'),
    path('d3demo/', d3demo, name='d3demo'),
    path('@<slug:slug>/', user_public_profile, name='user_public_profile'),
    path('@<slug:slug>/dashboard', user_dashboard, name='user_dashboard'),
    path('@<slug:usernameslug>/source', user_source, name='user_source'),
    path('@<slug:slug>/settings', user_settings, name='user_settings'),
    path('@<slug:slug>/settings/account', user_settings_account, name='user_settings_account'),
    path('explore/', explore, name='explore'),
    path('explore/users', explore_users, name='explore_users'),
    #path('<username>/', user_dashboard, name='user_dashboard')
    path('__debug__/', include(debug_toolbar.urls)),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('groups', views.GroupViewSet)
router.register('articles', views.ArticleViewSet, basename='articles')
router.register('projects', views.ProjectViewSet, basename='projects')
router.register('ner-result', views.ArticleViewSetForNerResult, basename='nerResult')
router.register('broswer-extension-data', views.DataViewforBrowser, basename='broswer_extension_data')
router.register('highlight', views.HighlightViewSetForBrowserExtension, basename='article-highlight')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns += [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
