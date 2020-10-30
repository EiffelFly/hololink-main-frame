from django.contrib.auth.models import User, Group
from article.models import Article
from project.models import Project
from accounts.models import Recommendation
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer, ArticleSerializer, ArticleSerializerForPost, ProjectSerializer, ProjectSerializerForPost, ArticleSerializerForNerResult, ProjectSerializerForBrowserExtension, RecommendationSerializerForBrowserExtension

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import hashlib
from rest_framework_api_key.permissions import HasAPIKey



def requestNEREngine(serializer):
    pass

def sha256_hash(content):
    sha = hashlib.sha256()
    sha.update(content.encode())
    return sha.hexdigest()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'POST':
            serializer_class = ArticleSerializerForPost
        else:
            serializer_class = ArticleSerializer

        return serializer_class

    def get_queryset(self):
        return Article.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        '''
            Because we don't allow user post any sensitive content and some other i
            nformation to our api. We have to create it from server side.

            perform_create will init serializer with this additional data.
        '''

        serializer.save(
            hash = sha256_hash(self.request.data['content']),
            created_by = self.request.user,
            created_at = timezone.localtime(timezone.now())
        )

class ArticleViewSetForNerResult(viewsets.ModelViewSet):
    authentication_classes = [HasAPIKey] #Django REST Framework API Key
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return ArticleSerializerForNerResult

    def get_queryset(self):
        return Article.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save()
    
    
class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'POST':
            serializer_class = ProjectSerializerForPost
        else:
            serializer_class = ProjectSerializer

        return serializer_class

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(created_by=user)
        

    
    def perform_create(self, serializer):
        '''
            Because we don't allow user post any sensitive content and some other i
            nformation to our api. We have to create it from server side.
        '''

        serializer.save(
            created_by = self.request.user,
            created_at = timezone.localtime(timezone.now())
        )
    

class DataViewforBrowser(viewsets.ViewSet):
    '''
        This endpoint is especially for chrome extension 
    '''

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = self.request.user
        recommendations = Recommendation.objects.filter(user=user, created_at__range=(timezone.localtime().replace(hour=0, minute=0, second=0), timezone.localtime().replace(hour=23, minute=59, second=59)))
        projects = Project.objects.filter(created_by=user)
        recommendations_serializer = RecommendationSerializerForBrowserExtension(recommendations, many=True)
        projects_serializer = ProjectSerializerForBrowserExtension(projects, many=True)

        return Response(
            {
                "recommendations": recommendations_serializer.data,
                "projects" : projects_serializer.data,
                "user": user.username
            }
        )
        

