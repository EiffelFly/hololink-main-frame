from django.contrib.auth.models import User, Group
from article.models import Article, Highlight
from project.models import Project
from accounts.models import Recommendation
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer, ArticleSerializer, ArticleSerializerForPost, ProjectSerializer, ProjectSerializerForPost, ArticleSerializerForNerResult, ProjectSerializerForBrowserExtension, RecommendationSerializerForBrowserExtension, HighlightSerializerForPost, HighlightSerializer, HighlightSerializerForRetrieve

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
    permission_classes = [HasAPIKey | IsAuthenticated] #Django REST Framework API Key

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


class HighlightViewSetForBrowserExtension(viewsets.ModelViewSet):

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'RETRIEVE':
            serializer_class = HighlightSerializerForRetrieve
        elif self.request.method == 'POST':
            serializer_class = HighlightSerializerForPost
        else:
            serializer_class = HighlightSerializer
        return serializer_class
    
    def get_queryset(self):
        user = self.request.user
        return Highlight.objects.filter(highlighted_by=user)
    
    def perform_create(self, serializer):
        serializer.save()

class DataViewSetforBrowserExtension(viewsets.ViewSet):
    '''
        This endpoint is sending necessary data back to chrome extension: with multiple model.
    '''

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


    # This is the temp compromise for browser data endpoint
    def create(self, request):

        target_page_title = request.data.get('page_title')
        target_page_url = request.data.get('page_url')

        user = self.request.user
        recommendations = Recommendation.objects.filter(user=user, created_at__range=(timezone.localtime().replace(hour=0, minute=0, second=0), timezone.localtime().replace(hour=23, minute=59, second=59)))
        projects = Project.objects.filter(created_by=user)
        recommendations_serializer = RecommendationSerializerForBrowserExtension(recommendations, many=True)
        projects_serializer = ProjectSerializerForBrowserExtension(projects, many=True)

        # target_page_title = self.request.META.get("HTTP_PAGE_TITLE", None)
        # target_page_url = self.request.META.get("HTTP_PAGE_URL", None)

        print(type(target_page_title), target_page_url)

        if target_page_url != None and target_page_title != None:
            try:
                article = Article.objects.get(name=target_page_title, from_url=target_page_url)
                highlights = Highlight.objects.filter(highlighted_page=article)
                highlight_serializer = HighlightSerializer(highlights, many=True)
                highlight_serializer = highlight_serializer.data
                print(highlight_serializer)
            except Article.DoesNotExist:
                highlight_serializer = [{"message":"Hololink doesn't have this article"}]
        

        return Response(
            {
                "recommendations": recommendations_serializer.data,
                "projects" : projects_serializer.data,
                "user": user.username,
                "highlight":highlight_serializer
            }
        )
        

