from django.contrib.auth.models import User, Group
from article.models import Article
from project.models import Project
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer, ArticleSerializer, ArticleSerializerForPost, ProjectSerializer, ProjectSerializerForPost

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import hashlib


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
        '''

        serializer.save(
            hash = sha256_hash(self.request.data['content']),
            created_by = self.request.user,
            created_at = timezone.localtime(timezone.now())
        )

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
        return Project.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        '''
            Because we don't allow user post any sensitive content and some other i
            nformation to our api. We have to create it from server side.
        '''

        serializer.save(
            created_by = self.request.user,
            created_at = timezone.localtime(timezone.now())
        )