from django.contrib.auth.models import User, Group
from article.models import Article
from project.models import Project
from rest_framework import serializers
import hashlib

def sha256_hash(content):
    sha = hashlib.sha256()
    sha.update(content.encode())
    return sha.hexdigest()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        ordering = ['-created_at']
        model = Project
        fields = [
            'id','name', 'created_at', 'created_by', 'articles',
            'project_basestone_keyword_sum', 'project_stellar_keyword_sum'
        ]
        read_only_fields = [
            'id', 'created_at', 'created_by'
        ]
        extra_kwargs = {'books': {'required': False}}

class ProjectSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'name'
        ]

class ArticleSerializer(serializers.ModelSerializer):
    '''
        Because the behavior of nested creates and updates can be ambiguous, and may require 
        complex dependencies between related models, REST framework 3 requires you to always 
        write these methods explicitly.

        https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
    '''
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        ordering = ['-created_at']
        model = Article
        fields = [
            'hash', 'name', 'content', 'from_url',
            'recommendation', 'projects', 'created_by', 'created_at',
            'article_basestone_keyword_sum','article_stellar_keyword_sum','tokenize_output','ner_output',
            'final_output'
        ]
        read_only_fields = [
            'hash', 'created_at', 'created_by'
        ]
        extra_kwargs = {'authors': {'required': False}}

class ArticleSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'name', 'content', 'from_url',
            'recommendation','projects'
        ]

