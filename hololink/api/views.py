from django.contrib.auth.models import User, Group
from article.models import Article
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer, ArticleSerializer, ArticleSerializerForPost

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
        serializer.save(
            hash = sha256_hash(self.request.data['content']),
            created_by = self.request.user,
            created_at = timezone.localtime(timezone.now())
        )
