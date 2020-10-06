from django.contrib.auth.models import User, Group
from article.models import Article
from project.models import Project
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.http import Http404
import hashlib
from django.utils import timezone
import requests
from rest_framework import status
from timeit import default_timer as timer
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
import threading
from article.models import Keyword, Domain
from accounts.models import Recommendation

# Notice: tldextract will update the TLD list first time running the module, beware of some limitation.
import tldextract
from urllib.parse import urlparse

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
            'final_output', 'D3_data_format', 'owned_by'
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
            if recommended == True:
                try:
                    recommendation = Recommendation.objects.get(user=user, article=article)
                except Recommendation.DoesNotExist:
                    recommendation = Recommendation.objects.create(
                        user=user,
                        article=article
                    )
                    recommendation.save()
            
            if user not in article.owned_by.all():
                article.ml_is_processing = True
                article.owned_by.add(user)
        except Article.DoesNotExist:
            parse_url = tldextract.extract(from_url)
            scheme = urlparse(from_url).scheme
            site_main_url = scheme + '://' + parse_url.registered_domain + '/'
        
            try:
                domain = Domain.objects.get(main_site=site_main_url, scheme_type=scheme)
            except Domain.DoesNotExist:
                domain = Domain.objects.create(
                    name=parse_url.registered_domain,
                    main_site=site_main_url,
                    created_by=user,
                    scheme_type=scheme,
                )
                domain.save()
                print(domain)

            data = {
                'hash':sha256_hash(content),
                'name':name,
                'from_url':from_url,
                'content':content,
                'recommended':recommended,
                'created_by':user,
                'created_at':timezone.localtime(timezone.now()),
                'ml_is_processing':True,
                'domain':domain,
            }

            try: 
                Domain.objects.get(main_site=site_main_url, scheme_type=scheme, owned_by_user=user.profile)
            except Domain.DoesNotExist:
                user.profile.source.add(domain)

            article = super().create(data)
            article.owned_by.add(user)

        project_name_list = []
            
        for project in projects:
            try:
                print(project, user)
                target_project = Project.objects.get(name=project, created_by=user)
                project_name_list.append(target_project.name)

                try:
                    article = Article.objects.get(projects=target_project, name=name)
                except Article.DoesNotExist:
                    article.projects.add(target_project)

            except Project.DoesNotExist:
                print('204','There is no such project')
        article.owned_by.add(user)

        if recommended == True:
            try:
                recommendation = Recommendation.objects.get(user=user, article=article)
            except Recommendation.DoesNotExist:
                recommendation = Recommendation.objects.create(
                    user=user,
                    article=article
                )
                recommendation.save()


        prepare_data_for_ml = {
            "username":user.username,
            "content":content,
            "projects":project_name_list,
            "article_name":name,
            "from_url":from_url
        }

        t = threading.Thread(target=request_ml_thread, kwargs=prepare_data_for_ml, daemon=True)
        t.start()

        return article


    
def sha256_hash(content):
    sha = hashlib.sha256()
    sha.update(content.encode())
    return sha.hexdigest()

def json_to_d3(data):

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
    article_name = data_for_merging['article_name']
    from_url = data_for_merging['from_url']

    article = get_object_or_404(Article, name=article_name, from_url=from_url)
    user = get_object_or_404(User, username=username)

    '''
        Question: 我該如何防止使用者上傳同一篇文章到同一個 project 複數次造成的舊有的 keywords 被無意義的增加 connection 數量
        -> 這個問題應該在使用者 post 該文章時就解決掉，post ner, ner post me，這些都是 lazy 的。

        不需要確認 project 是否擁有該 article 這件事在單純 POST article 就會做完了
                --- 確認 article_keyword 是否存在於 project_keyword
                    --- 不存在：增加該 keyword
                    --- 存在：
                        --- 判斷是否位於同一個 level
                            --- 是：將原有 keyword connection + 1
                            --- 否：新建 keyword
    '''
    
    

    for target_project in projects:
        # Create or Update article info in project_d3_json['nodes']
        project = Project.objects.get(name=target_project, created_by=user)

        flag_for_creating_article_node = True

        for node in project.project_d3_json['nodes']:
            if node['level'] == 'article':
                if node['id'] == article_name:
                    node.update(
                        {
                            "basestoneNum":article_data['basestoneNum'],
                            "stellarNum":article_data['stellarNum']
                        }
                    )
                    flag_for_creating_article_node = False
                    break
                
        if flag_for_creating_article_node == True:
            print('create node')
            project.project_d3_json['nodes'].append(
                {
                    "id":article_name,
                    "url":from_url,
                    "level":"article",
                    "basestoneNum":article_data['basestoneNum'],
                    "stellarNum":article_data['stellarNum'],
                }
            )        

        for article_node in article_data['nodes']:    
            # Append new keyword
            print(project.keyword_list['total'])
            try:
                keyword = Keyword.objects.get(name=article_node['title'], keyword_type=article_node['level'])
                if user.profile not in keyword.owned_by_user.all():
                    keyword.owned_by_user.add(user.profile)
                if keyword not in keyword.owned_by_article.all():
                    keyword.owned_by_article.add(article)
            except Keyword.DoesNotExist:
                keyword = Keyword.objects.create(
                    name = article_node['title'],
                    keyword_type = article_node['level'],
                    created_by = user
                )
                keyword.owned_by_user.add(user.profile)
                keyword.owned_by_article.add(article)
                keyword.save()

            # if article_node['title'] not in project.keyword_list['total']:
            if keyword not in project.keyword.all():
                print("new keywords", article_node['title'])
                project.keyword.add(keyword)
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
                # else: the node exist in this project, but we don't know which type it belonged to (base or stellar) 
                keyword_type = article_node['level']
                # if article_node['title'] not in project.keyword_list[f'{keyword_type}']:
                # if not Project.objects.filter(keyword__keword_type=keyword_type).exists():

                if not Keyword.objects.filter(keyword_type=keyword_type, owned_by_project=project, name=article_node['title']).exists():
                    print("old keywords with new level", article_node['title'])
                    try:
                        keyword_with_correct_type = Keyword.objects.get(name=article_node['title'], keyword_type=article_node['level'])
                    except Keyword.DoesNotExist:
                        keyword_with_correct_type = Keyword.objects.create(
                            name = article_node['title'],
                            keyword_type = article_node['level'],
                            created_by = user
                        )
                        keyword.save()
                    project.keyword.add(keyword_with_correct_type)
                    project.keyword_list[f'{keyword_type}'].append(article_node['title'])
                    project.project_d3_json['nodes'].append(
                        {
                            "id":article_node['title'],
                            "level":article_node['level'],
                            "connection":1,
                        }
                    )
                else:
                    for project_node in project.project_d3_json['nodes']:
                        # 這種放在不同 list, dict 的資料不能用 is 來比較，因為 is 除了比較值之外還會比較其 object 是否相等（不同記憶處的會不同）
                        if project_node['id'] == article_node['title'] and project_node['level'] == article_node['level']:
                            project_node.update({"connection":project_node['connection'] + 1})
                            print(project_node['id'], project_node['connection'])
                    
        project.save()
        return project

def request_ml_thread(**kwargs):

    # prepare request session and using urllib3.Retry to cope with requests.exceptions.ConnectionError
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    url = "http://35.221.178.255:8080/predict"
    start = timer()  
    ml_result = session.post(url, json=[kwargs])
    end = timer()
    print(ml_result.status_code)
    if ml_result.status_code == 200:
        article = Article.objects.get(name=kwargs['article_name'], from_url=kwargs['from_url'])
        print(article)
        setattr(article, 'ml_is_processing', False)
        ner_output = ml_result.json()
        print(ner_output)
        d3_data = json_to_d3(ner_output[0])
        kwargs['d3'] = d3_data
        merge = merge_article_into_galaxy(kwargs)
        print(merge)
        setattr(article, 'ner_output', json.dumps(ner_output[0]))
        setattr(article, 'D3_data_format', d3_data)
        setattr(article, 'D3_data_format', d3_data)
        article.save()
        merge.save()
    
    print(start-end)


        
