from django.contrib.auth.models import User, Group
from article.models import Article
from project.models import Project
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.http import Http404
import hashlib
from django.utils import timezone

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
            'id','name', 'created_at', 'created_by', 'articles_project_owned',
            'project_basestone_keyword_sum', 'project_stellar_keyword_sum', 'keyword_list', 'project_d3_json'
        ]
        read_only_fields = [
            'id', 'created_at', 'created_by', 'keyword_list', 'project_d3_json'
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
            'final_output', 'D3_data_format'
        ]
        read_only_fields = [
            'hash', 'created_at', 'created_by', 'D3_data_format'
        ]
        extra_kwargs = {'authors': {'required': False}}


class ArticleSerializerForNEREngine(serializers.ModelSerializer):

    ner_output = serializers.JSONField()

    class Meta:
        model = Article
        fields = [
            'name', 'from_url', 'D3_data_format', 'ner_output', 'projects', 'owned_by'
        ]
        read_only_fields = [
            'D3_data_format'
        ]

    def create(self, validated_data):
        users = validated_data.get('owned_by', None)
        
        for user in users:
            user = get_object_or_404(User, username=user)

        name = validated_data.get('name', None)
        from_url = validated_data.get('from_url', None)
        ner_output = validated_data.get('ner_output', None)
        projects = validated_data.get('projects', None)

        try:
            article = Article.objects.get(name=name, from_url=from_url)
        except Article.DoesNotExist:
            raise serializers.ValidationError({"ValidationError": "Article doesn't exist, you must post exact the same name and url"})

        d3_data = json_to_d3(ner_output)   

        ner_output.pop('url', None)
        ner_output.pop('title', None)
        ner_output.pop('content', None)
        ner_output.pop('galaxy', None)

        setattr(article, 'ner_output', ner_output)
        setattr(article, 'D3_data_format', d3_data)
        setattr(article, 'ml_is_processing', False)
        article.save()

        data_for_merging = {
            "username":user,
            "name":name,
            "from_url":from_url,
            "projects":projects,
            "d3":d3_data,  
        }

        merge = merge_article_into_galaxy(data_for_merging)
        merge.save()

        return article    

class ArticleSerializerForPost(serializers.ModelSerializer):

    '''
        We use validate() method to check whether an article is duplicated in the galaxy
        then we use create() method to get the existing object and update it or create it.

        *many to many fields will first be removed from fieldlist by DRF.

        修整處：
        1. 不要覆蓋 create() 而是覆蓋 save() 就好
        2. add owned_by 和 peoject 的寫法修整成相同的
    '''

    class Meta:
        model = Article
        fields = [
            'name', 'content', 'from_url',
            'recommended','projects',
        ]

    def validate(self, data):
        duplication_list = []
        username = self.context['request'].user
        user = get_object_or_404(User, username=username)
        for project in data['projects']:  
            try:
                article = get_object_or_404(Article, from_url=data['from_url'], projects=project, owned_by=user) # owned_by=user this can work!
                duplication_list.append(project)
            except Http404:
                pass

        if duplication_list:
            raise serializers.ValidationError({"Duplication Error": duplication_list})
        
        return data

    def create(self, validated_data):
        username = self.context['request'].user
        user = get_object_or_404(User, username=username)
        name = validated_data.get('name', None)
        from_url = validated_data.get('from_url', None)
        content = validated_data.get('content', None)
        recommended = validated_data.get('recommended', None)
        projects = validated_data.get('projects', None)
        
        try:
            article = Article.objects.get(name=name, from_url=from_url)
            for project in projects:
                try:
                    target_project = Project.objects.get(name=project, created_by=username)
                    article.projects.add(target_project)
                except Project.DoesNotExist:
                    print('There is no such project')
            if user not in article.owned_by.all():
                article.owned_by.add(user)
            return article

        except Article.DoesNotExist:

            data = {
                'hash':sha256_hash(content),
                'name':name,
                'from_url':from_url,
                'content':content,
                'recommended':recommended,
                'created_by':user,
                'created_at':timezone.localtime(timezone.now())
            }

            article = super().create(data)
            
            for project in projects:
                try:
                    target_project = Project.objects.get(name=project, created_by=username)
                    article.projects.add(target_project)
                except Project.DoesNotExist:
                    print('There is no such project')
            article.owned_by.add(user)
            return article
    
def sha256_hash(content):
    sha = hashlib.sha256()
    sha.update(content.encode())
    return sha.hexdigest()

def json_to_d3(data):

    
    article_title = data['title']
    article_galaxy = data['galaxy']
    article_url = data['url']

    nodejson = []
    basestoneNum = 0
    stellarNum = 0
    nodevalidator = []

    for key,value in data['Final'].items():
        title = value['Title']
        frequency = value['Frequency']
        keyword_type = value['POS']

        if keyword_type == 'Na' or keyword_type == 'Nb' or keyword_type == 'Nc':            
            nodejson.append({"title":title, "frequency":frequency, "level":"stellar", "type":keyword_type})
            stellarNum += 1
            nodevalidator.append(title)
        else:
            if keyword_type == 'DATE' or keyword_type == 'ORDINAL' or keyword_type == 'CARDINAL':
                pass
            else:
                nodejson.append({"title":title, "frequency":frequency, "level":"basestone", "type":keyword_type})
                basestoneNum += 1
                nodevalidator.append(title)


    processed_data = {
        "nodes":nodejson,
        "nodes_validator": nodevalidator,
        "basestoneNum":basestoneNum,
        "stellarNum":stellarNum,
    }

    return processed_data

def merge_article_into_galaxy(data_for_merging):

    username = data_for_merging['username']
    article_data = data_for_merging['d3']
    projects = data_for_merging['projects']
    article_url = data_for_merging['from_url']
    article_name = data_for_merging['name']

    user = get_object_or_404(User, username=username)
    try:
        article = Article.objects.get(name=article_name, from_url=article_url)
    except Article.DoesNotExist:
        pass

    '''
        --- 確認該 article 是否存在 project
            --- 不存在：將 article 加入 node
                --- 確認 article_keyword 是否存在於 project_keyword
                    --- 不存在：增加該 keyword
                    --- 存在：將原有 keyword connection + 1
            --- 存在
                --- 確認 article_keyword 是否存在於 project_keyword
                    --- 不存在：增加該 keyword (check)
                    --- 存在
                        --- 確認該 article_keyword_level 是否存在於 project_keyword_level
                            --- 是：pass
                            --- 否：增加該 keyword 於相對應的 group
    '''

    for target_project in projects:
        project = Project.objects.get(name=target_project, created_by=user)
        # Nodes
        # Append new article node
        if article not in project.articles_project_owned.all():
            project.project_d3_json['nodes'].append(
                {
                    "id":article_name,
                    "url":article_url,
                    "level":"article",
                    "basestoneNum":article_data['basestoneNum'],
                    "stellarNum":article_data['stellarNum'],
                }
            )
            for article_node in article_data['nodes']:        
                # Append new keyword
                if article_node['title'] not in project.keyword_list['total']:
                    print('new article, new keywords', article_node, project.keyword_list['total'])
                    project.keyword_list['total'].append(article_node['title'])
                    if article_node['level'] == 'basestone':
                        project.keyword_list['basestone'].append(article_node['title'])
                    else:
                        project.keyword_list['stellar'].append(article_node['title'])
                    project.project_d3_json['nodes'].append(
                        {
                            "id":article_node['title'],
                            "level":article_node['level'],
                            "connection":1,
                        }
                    )
                # Make existed node's connection plus 1
                else:
                    print('new article, old keywords', article_node, project.keyword_list['total'])
                    for project_node in project.project_d3_json['nodes']:
                        # 這種放在不同 list, dict 的資料不能用 is 來比較，因為 is 除了比較值之外還會比較其 object 是否相等（不同記憶處的會不同）
                        if project_node['id'] == article_node['title'] and project_node['level'] == article_node['level']:
                            project_node.update({"connection":project_node['connection'] + 1})
            project.save()
            return project
        else:
            # else: article already exist in the project
            for article_node in article_data['nodes']:    
                # Append new keyword
                print(project.keyword_list['total'])
                if article_node['title'] not in project.keyword_list['total']:
                    print("old article, new keywords", article_node['title'])
                    project.keyword_list['total'].append(article_node['title'])
                    if article_node['level'] is 'basestone':
                        project.keyword_list['basestone'].append(article_node['title'])
                    else:
                        project.keyword_list['stellar'].append(article_node['title'])
                    project.project_d3_json['nodes'].append(
                        {
                            "id":article_node['title'],
                            "level":article_node['level'],
                            "connection":1,
                        }
                    )
                else:
                    # else: the node exist in this project, but we don't know which grout it belonged to (base or stellar) 
                    keyword_type = article_node['level']
                    if article_node['title'] not in project.keyword_list[f'{keyword_type}']:
                        print("old article, old keywords", article_node['title'])
                        project.keyword_list[f'{keyword_type}'].append(article_node['title'])
                        project.project_d3_json['nodes'].append(
                        {
                            "id":article_node['title'],
                            "level":article_node['level'],
                            "connection":1,
                        }
                    )
            project.save()
            return project



        
