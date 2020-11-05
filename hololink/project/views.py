
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from .models import Project
from .forms import ProjectForm, GalaxySettingsForm, DeleteArticleForm
from article.models import Article, Keyword
from django.db.models import Sum
import hashlib
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from accounts.models import Profile
from django.contrib.auth.models import User


def now():
    return timezone.localtime(timezone.now())

def is_valid_queryparam(param):
    return param != '' and param is not None

def filter(request):
    qs = Project.objects.filter(created_by=request.user).order_by('-created_at')
    filterProjectsName = request.GET.get('project_filter')
    print(filterProjectsName)

    if is_valid_queryparam(filterProjectsName):
        qs = qs.filter(name__icontains=filterProjectsName)

    return qs

def projects_list(request, **kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))  

    count_article = []
    count_basestone = []
    count_stellar = []

    profile = get_object_or_404(Profile, user=request.user)

    projects = filter(request)
    for project in projects:
        articles = Article.objects.filter(projects=project).order_by('-created_at')
        count_article.append(project.articles_project_owned.all().count())
        count_basestone.append(Keyword.objects.filter(keyword_type='basestone', owned_by_project=project).count())
        count_stellar.append(Keyword.objects.filter(keyword_type='stellar', owned_by_project=project).count())
    
    context = {
        'profile' : profile,
        'projects' : projects,
        'countArticles' : count_article,
        'countBasestoneKeywords' : count_basestone,
        'countStellarKeywords' : count_stellar,
        'active_nav':'project',
    }

    return render(request, 'projects_list.html', context)    

def project_detail(request, projectnameslug, **kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))  
    
    project = get_object_or_404(Project, slug=projectnameslug, created_by=request.user)
    articles = Article.objects.filter(projects=project)


    #send message to article.views.article_detail
    request.session['user_selected_project'] = project.name
    context = {
        'project' : project, 
        'articles': articles,
    }

    return render(request, 'project_detail.html', context)

def project_articles(request, projectnameslug, **kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))  

    user = get_object_or_404(User, username=request.user)
    project = get_object_or_404(Project, slug=projectnameslug, created_by=request.user)
    articles = Article.objects.filter(projects=project).order_by('-created_at')
    count_project_basestone = Keyword.objects.filter(keyword_type='basestone', owned_by_project=project).count()
    count_project_stellar = Keyword.objects.filter(keyword_type='stellar', owned_by_project=project).count()

    count_article_basestone = []
    count_article_stellar = []
    
    for article in articles:
        print(article)
        count_article_basestone.append(Keyword.objects.filter(keyword_type='basestone', owned_by_article=article).count())
        count_article_stellar.append(Keyword.objects.filter(keyword_type='stellar', owned_by_article=article).count())
    
    countArticles = project.articles_project_owned.all().count()
    
    '''
    if request.method == 'POST':
        form = DeleteArticleForm(request.POST)
        if request.POST['action'].split("_delete_",1)[0] == "deleteArticle":
            target_article_name = request.POST['action'].split("_delete_",1)[1]
            target_article = get_object_or_404(Article, name=target_article_name)
            project.articles_project_owned.remove(target_article)
            target_article.owned_by.remove(user)
            
            print(range(0, len(project.project_d3_json['nodes'])))
            for i in range(len(project.project_d3_json['nodes'])):
                print(i)
                print(project.project_d3_json['nodes'][i]['id'])
                if project.project_d3_json['nodes'][i]['id'] in project.keyword_list['total']:
                    if project.project_d3_json['nodes'][i]['connection'] == 1:
                        del project.project_d3_json['nodes'][i]
                    elif project.project_d3_json['nodes'][i]['connection'] > 1:
                        project.project_d3_json['nodes'][i].update({"connection":project.project_d3_json['nodes'][i]['connection']-1})
            
            for link in range(len(project.project_d3_json['links'])):
                if project.project_d3_json['links'][i]['source'] == target_article_name:
                    del project.project_d3_json['links'][i]

            project.save()
            target_article.save()

            return HttpResponseRedirect(reverse('project:project_articles', args=(project.slug,)))
        '''
    
    print(project.ml_is_processing)

    context = {
        'profile':user.profile,
        'project' : project, 
        'articles': articles,
        'countArticles':countArticles,
        'data':{'basestone':count_project_basestone, 'stellar':count_project_stellar},
        'count_article_basestone':count_article_basestone,
        'count_article_stellar':count_article_stellar,
    }  

    return render(request, 'project_dashboard_articles_2.html', context)

def project_dashboard(request, projectnameslug, **kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))  

    profile = get_object_or_404(Profile, user=request.user)
    
    project = get_object_or_404(Project, slug=projectnameslug, created_by=request.user)
    articles = Article.objects.filter(projects=project)
    # basestone = articles.aggregate(Sum('article_basestone_keyword_sum')).get('article_basestone_keyword_sum__sum', 0)
    # stellar = articles.aggregate(Sum('article_stellar_keyword_sum')).get('article_stellar_keyword_sum__sum', 0)
    countArticles = project.articles_project_owned.all().count()
    count_basestone = Keyword.objects.filter(keyword_type='basestone', owned_by_project=project).count()
    count_stellar = Keyword.objects.filter(keyword_type='stellar', owned_by_project=project).count()

    context = {
        'profile':profile,
        'project' : project, 
        'articles': articles,
        'countArticles':countArticles,
        'data':{'basestone':count_basestone, 'stellar':count_stellar},
    }

    return render(request, 'project_dashboard_hologram.html', context) 

def project_hologram(request, projectnameslug, **kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login')) 
    
    profile = get_object_or_404(Profile, user=request.user)

    project = get_object_or_404(Project, slug=projectnameslug, created_by=request.user)
    articles = Article.objects.filter(projects=project)
    countArticles = project.articles_project_owned.all().count()
    count_basestone = Keyword.objects.filter(keyword_type='basestone', owned_by_project=project).count()
    count_stellar = Keyword.objects.filter(keyword_type='stellar', owned_by_project=project).count()

    print(project.project_visibility)

    context = {
        'profile':profile,
        'project' : project, 
        'articles': articles,
        'countArticles':countArticles,
        'data':{'basestone':count_basestone, 'stellar':count_stellar},
    }

    return render(request, 'project_dashboard_hologram.html', context) 

@csrf_exempt
def galaxy_setting(request, projectnameslug, **kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    profile = get_object_or_404(Profile, user=request.user)

    project = get_object_or_404(Project, slug=projectnameslug, created_by=request.user)
    articles = Article.objects.filter(projects=project)
    confirmation_code = f'{request.user}/{project.name}'
    countArticles = project.articles_project_owned.all().count()
    count_basestone = Keyword.objects.filter(keyword_type='basestone', owned_by_project=project).count()
    count_stellar = Keyword.objects.filter(keyword_type='stellar', owned_by_project=project).count()

    context = {
        'profile':profile,
        'form': None,
        'tips': [],
        'project':project,
        'confirmation_code':confirmation_code,
        'countArticles':countArticles,
        'data':{'basestone':count_basestone, 'stellar':count_stellar},
    }

    if request.method == 'POST':
        form = GalaxySettingsForm(request.POST)
        context['form'] = form
        if form.is_valid():
            if request.POST['action'] == "rename_galaxy":
                project.name = form.cleaned_data.get('name')
                project.save()
                messages.add_message(request, messages.SUCCESS, _('Edited successfully.'))
                return HttpResponseRedirect(reverse('project:galaxy_setting',kwargs={'usernameslug':profile.slug, 'projectnameslug':project.slug} ))

            elif request.POST['action'] == "edit_description":
                project.description = form.cleaned_data.get('galaxy_description')
                project.save()
                messages.add_message(request, messages.SUCCESS, _('Edited successfully.'))
                return HttpResponseRedirect(reverse('project:galaxy_setting',kwargs={'usernameslug':profile.slug, 'projectnameslug':project.slug}))

            elif request.POST['action'] == "change_galaxy_visibility":
                if form.cleaned_data.get('change_galaxy_visibility_confirmation') == confirmation_code:
                    project.project_visibility = form.cleaned_data.get('galaxy_visibility')
                    project.save()
                    messages.add_message(request, messages.SUCCESS, _('Edited successfully.'))
                    context['form'] = GalaxySettingsForm()
                    return HttpResponseRedirect(reverse('project:galaxy_setting',kwargs={'usernameslug':profile.slug, 'projectnameslug':project.slug}))
                else:
                    messages.error(request, messages.ERROR, _('Confirmation input is not correct'))
                    return HttpResponseRedirect(reverse('project:galaxy_setting',kwargs={'usernameslug':profile.slug, 'projectnameslug':project.slug}))
            elif request.POST['action'] == 'delete_galaxy':
                if form.cleaned_data.get('delete_galaxy_confirmation') == confirmation_code:
                    project_name = project.name
                    project.delete()
                    messages.add_message(request, messages.SUCCESS, _(f'Successfully delete galaxy {project_name}'))
                    return HttpResponseRedirect(reverse('project:projects_list',kwargs={'usernameslug':profile.slug}))
                else:
                    messages.add_message(request, messages.ERROR, _('Confirmation input is not correct'))
                    return HttpResponseRedirect(reverse('project:galaxy_setting',kwargs={'usernameslug':profile.slug, 'projectnameslug':project.slug}))
        
    else:
        form = GalaxySettingsForm()
        form.fields['name'].widget.attrs['placeholder'] = project.name #added placeholder
        form.fields['galaxy_description'].initial = project.description 
        form.fields['galaxy_visibility'].initial = project.project_visibility
        context['form'] = form
        print('i am here')
        

        return render(request, 'project_dashboard_settings.html', context)


@csrf_exempt
def create_newproject(request, **kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    context = {
        'form': None,
        'tips': []
    }

    if request.method == 'POST':
        form = ProjectForm(request.POST, user=request.user)
        context['form'] = form
        if form.is_valid():
            project = Project.objects.create(
                name=form.cleaned_data.get('name'),
                project_visibility=form.cleaned_data.get('galaxy_visibility'),
                created_by=request.user,
                created_at=now(),
            )
            messages.add_message(request, messages.SUCCESS, _('Added successfully.'))
            return redirect(reverse('user_dashboard', kwargs={'slug': request.user.username}))
    else:
        form = ProjectForm(user=request.user)
        context['form'] = form
        context['tips'] += [_('Fill in the following form to create a new galaxy.')]
    return render(request, 'create_new_project_test.html', context)

def deliver_D3(request, projectnameslug, **kwargs):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    
    project = get_object_or_404(Project, slug=projectnameslug, created_by=request.user)
    count_basestone = Keyword.objects.filter(keyword_type='basestone', owned_by_project=project).count()
    count_stellar = Keyword.objects.filter(keyword_type='stellar', owned_by_project=project).count()
    amount_of_keywords = count_basestone + count_stellar
    amount_of_articles = Article.objects.filter(owned_by=request.user, projects=project).count()

    return JsonResponse({"graph":project.project_d3_json, "amount_of_keywords":amount_of_keywords, "amount_of_articles":amount_of_articles}, safe=False)

def galaxy_telescope(request, projectnameslug, usernameslug):
    user = get_object_or_404(User, username=usernameslug)
    project = get_object_or_404(Project, slug=projectnameslug, created_by=request.user)

    context = {
        'user':user,
        'project':project,
    }

    return render(request, 'galaxy_telescope.html', context)