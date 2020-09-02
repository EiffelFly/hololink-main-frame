from django.contrib.auth.models import User, Group
from article.models import Article
from project.models import Project
from rest_framework import serializers
from django.shortcuts import get_object_or_404
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
            'recommended', 'projects', 'created_by', 'created_at',
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
            'recommended','projects'
        ]
    
    def validate(self, data):
        duplication_list = []
        for project in data['projects']:
            try:
                article = get_object_or_404(Article, from_url=data['from_url'], projects=project)
                duplication_list.append(project)
                print('duplicate')
            except Exception as e:
                print(e)

        if duplication_list:
            raise serializers.ValidationError({"Duplication Error": duplication_list})
        
        return data

    def create(self, validated_data):
        name = validated_data.get('name', None)
        from_url = validated_data.get('from_url', None)
        content = validated_data.get('content', None)
        recommended = validated_data.get('recommended', None)
        projects = validated_data.get('projects', None)

        try:
            article = Article.objects.get(name=name, from_url=from_url)
            for project in projects:
                article.projects.set(project)

        except Article.DoesNotExist:
            article = Article.objects.create(name=name, from_url=from_url, content=content, recommended=recommended, projects=projects)

        ''' 
            We are using django create_or_update method to make sure every article only have one object in database
            https://docs.djangoproject.com/en/3.1/ref/models/querysets/#update-or-create
        
        print('iamhere', validated_data)
        article, created = Article.objects.get_or_create(
            
            content = validated_data.get('content', None),
            
            recommended = validated_data.get('recommended', None),
            created_by = validated_data.get('User', None),
        )
        article.projects.add(validated_data.get('projects', None))
        return article
        '''
    
