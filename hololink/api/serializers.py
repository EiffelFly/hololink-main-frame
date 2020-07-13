from django.contrib.auth.models import User, Group
from article.models import Article
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'hash', 'name', 'content', 'from_url',
            'recommendation', 'article_belongto_project', 'created_by', 'created_at',
            'article_basestone_keyword_sum','article_stellar_keyword_sum','tokenize_output','ner_output',
            'final_output'
        ]

'''
    In this case, we don't want any situation that will update this value after object had been created:
    hash, created_at, created_by
'''

class ArticleSerializerForUpdate(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'name', 'content', 'from_url',
            'recommendation', 'article_belongto_project',
            'article_basestone_keyword_sum','article_stellar_keyword_sum','tokenize_output','ner_output',
            'final_output'
        ]

