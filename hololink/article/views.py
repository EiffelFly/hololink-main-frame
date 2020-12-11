from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
import hashlib
from .models import Article, Keyword, Highlight
from .forms import ArticleForm, ArticleChangeForm
from django.contrib.auth.models import User
from unidecode import unidecode
from django.utils.text import slugify
from django.http import JsonResponse
from accounts.models import Profile
from bs4 import BeautifulSoup



def now():
    return timezone.localtime(timezone.now())


def sha256_hash(content):
    sha = hashlib.sha256()
    sha.update(content.encode())
    return sha.hexdigest()


def change_list(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    #user = get_object_or_404(User, username=username)
    user = User.objects.get(username=request.user.username)
    articles = Article.objects.filter(created_by=request.user)
    for article in articles:
        if len(article.content) > 50:
            article.content = article.content[0:48] + '..'
    context = {
        'articles': articles,
    }
    return render(request, 'article/change_list_test.html', context)


@csrf_exempt
def add(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    context = {
        'form': None,
        'tips': []
    }
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        context['form'] = form
        if form.is_valid():
            article = Article.objects.create(
                hash=sha256_hash(form.cleaned_data.get('content')),
                name=form.cleaned_data.get('name'),
                content=form.cleaned_data.get('content'),
                from_url=form.cleaned_data.get('from_url'),
                recommendation=form.cleaned_data.get('recommendation'),
                #project=form.cleaned_data.get('project'),
                created_by=request.user,
                created_at=now(),
            )
            messages.add_message(request, messages.SUCCESS, _('Added successfully.'))
            return redirect(reverse('article:change_list'))
    else:
        form = ArticleForm()
        context['form'] = form
        context['tips'] += [_('Fill in the following form to create a new article.')]
    return render(request, 'article/add.html', context)


@csrf_exempt
def change(request, id):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    context = {
        'form': None,
        'tips': [],
    }
    instance = get_object_or_404(Article, id=id, created_by=request.user)
    if request.method == 'POST':
        form = ArticleChangeForm(request.POST, instance=instance)
        context['form'] = form
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _('Added successfully.'))
            return redirect(reverse('article:change_list'))
    else:
        form = ArticleChangeForm(instance=instance)
        context['form'] = form
        context['tips'] += [
            _('The following is the current setting. Please fill in the part you want to modify and then submit.')
        ]
    return render(request, 'article/change.html', context)


def delete(request, id):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    instance = get_object_or_404(Article, id=id, created_by=request.user)
    if request.method == 'POST':
        instance.delete()
        messages.add_message(request, messages.SUCCESS, _('Deleted successfully.'))
        return redirect(reverse('article:change_list'))
    return render(request, 'article/delete.html')

def article_detail(request, usernameslug, articlenameslug):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    user = User.objects.get(username=request.user.username)
    article = get_object_or_404(Article, slug=articlenameslug, created_by=request.user)

    user_selected_project = request.session.get('user_selected_project')
    count_basestone = Keyword.objects.filter(keyword_type='basestone', owned_by_article=article).count()
    count_stellar = Keyword.objects.filter(keyword_type='stellar', owned_by_article=article).count()
    highlights = Highlight.objects.filter(highlighted_by=user, highlighted_page=article)

    highlights_json_data = []
    for highlight in highlights:
        highlight_json = {
            "highlighted_by":user.username,
            "created_at":highlight.created_at,
            "text":highlight.text,
            "id_on_page":highlight.id_on_page,
            "range_object":highlight.range_object,
            "highlight_parent_node_text":highlight.highlight_parent_node_text
        }
        highlights_json_data.append(highlight_json)


    context = {
        'article':article,
        'user':user,
        'user_selected_project':user_selected_project,
        'count_basestone':count_basestone,
        'count_stellar':count_stellar,
        'highlights':highlights_json_data,
    }
    return render(request, 'article/article_detail_ver3.html', context)

def is_valid_queryparam(param):
    return param != '' and param is not None

def filter(request):
    '''
        implement articles search bar 
    '''
    qs = Article.objects.filter(owned_by=request.user).order_by('-created_at')
    filterArticlesName = request.GET.get('article_filter')
    

    if is_valid_queryparam(filterArticlesName):
        qs = qs.filter(name__icontains=filterArticlesName)

    return qs


def articles_list(request, usernameslug):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    count_basestone = []
    count_stellar = []

    articles = filter(request)

    profile = get_object_or_404(Profile, user=request.user)
    
    for article in articles:
        print(article)
        count_basestone.append(Keyword.objects.filter(keyword_type='basestone', owned_by_article=article).count())
        count_stellar.append(Keyword.objects.filter(keyword_type='stellar', owned_by_article=article).count())
    

    context = {
        'profile':profile,
        'articles':articles,
        'count_basestone':count_basestone,
        'count_stellar':count_stellar,
        'active_nav':'article',
    }

    return render(request, 'article/articles_list.html', context)   

def deliver_D3(request, articlenameslug, usernameslug):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    
    article = get_object_or_404(Article, slug=articlenameslug, created_by=request.user)

    return JsonResponse(article.D3_data_format, safe=False)