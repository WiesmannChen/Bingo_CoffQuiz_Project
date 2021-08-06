from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime
from coffquiz.models import Coffee, Article, UserProfile, Comment
from coffquiz.forms import CoffeeForm, ArticleForm, UserForm, UserProfileForm, CommentForm
from django.contrib.auth.models import User
from coffquiz.bing_search import run_query

def index(request):
    coffee_list = Coffee.objects.order_by('-likes')[:5]
    article_list = Article.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['introduction'] = 'Coffquiz is a coffee exchange website, \
    please feel free to add various coffee products and post reviews on them.'
    context_dict['coffeelist'] = coffee_list
    context_dict['articles'] = article_list

    return render(request, 'coffquiz/index.html', context=context_dict)

def about(request):
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return render(request, 'coffquiz/about.html', context=context_dict)

def show_coffee(request, coffee_name_slug):
    context_dict = {}
    try:
        coffee = Coffee.objects.get(slug=coffee_name_slug)
        articles = Article.objects.filter(coffee=coffee).order_by('-views')

        context_dict['coffee'] = coffee
        context_dict['articles'] = articles
    
    except Coffee.DoesNotExist:
        context_dict['coffee'] = None
        context_dict['articles'] = None

    # Start search functionality code. 
    if request.method == 'POST':
        if request.method == 'POST':
            query = request.POST['query'].strip()
            
            if query:
                context_dict['result_list'] = run_query(query)
                context_dict['query'] = query

    return render(request, 'coffquiz/coffee.html', context=context_dict)

def show_article(request, article_title_slug):
    context_dict = {}
    try:
        article = Article.objects.get(slug=article_title_slug)
        comments = Comment.objects.filter(article=article)

        context_dict['article'] = article
        context_dict['comments'] = comments
    
    except Coffee.DoesNotExist:
        context_dict['article'] = None
        context_dict['comments'] = None
    
    return render(request, 'coffquiz/article.html', context=context_dict)

def all_coffee(request):
    allCoffee = Coffee.objects.all().order_by('-likes')
    context_dict = {}
    context_dict['all_coffee'] = allCoffee

    return render(request, 'coffquiz/all_coffee.html', context=context_dict)

def all_articles(request):
    allArticles = Article.objects.all().order_by('-views')
    context_dict = {}
    context_dict['all_articles'] = allArticles

    return render(request, 'coffquiz/all_Articles.html', context=context_dict)

@login_required
def add_coffee(request):
    user = User.objects.get(username=request.user)
    form = CoffeeForm()

    if request.method == 'POST':
        form = CoffeeForm(request.POST)
        if form.is_valid():
            coffee = form.save(commit=False)
            coffee.user = user
            coffee.save()
            
            return redirect('coffquiz:index')
        else:
            print(form.errors)
    return render(request, 'coffquiz/add_coffee.html', {'form': form})

@login_required
def add_comment(request, article_title_slug):
    try:
        article = Article.objects.get(slug=article_title_slug)
    except:
        article = None
    
    if article is None:
        return redirect(reverse('coffquiz:index'))

    user = User.objects.get(username=request.user)
    
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            if article:
                comment = form.save(commit=False)
                comment.article = article
                comment.user = user
                comment.save()
                return redirect(reverse('coffquiz:show_article', kwargs={'article_title_slug':article_title_slug}))
            else:
                print(form.errors)

    context_dict = {'form': form, 'article': article}
    return render(request, 'coffquiz/add_comment.html', context=context_dict)            


@login_required
def add_article(request, coffee_name_slug):
    user = User.objects.get(username=request.user)
    try:
        coffee = Coffee.objects.get(slug=coffee_name_slug)
    except Coffee.DoesNotExist:
        coffee = None
    
    if coffee is None:
        return redirect(reverse('coffquiz:index'))

    form = ArticleForm()

    if request.method == 'POST':
        form = ArticleForm(request.POST)

        if form.is_valid():
            if coffee:
                article = form.save(commit = False)
                article.coffee = coffee
                article.writer = user
                article.save()

                return redirect(reverse('coffquiz:show_coffee', kwargs={'coffee_name_slug':coffee_name_slug}))

        else:
            print(form.errors)
    context_dict = {'form': form, 'coffee': coffee}
    return render(request, 'coffquiz/add_article.html', context=context_dict)

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
        
    request.session['visits'] = visits

# This is used to record the number of views of the article
def goto_article(request):
    if request.method == 'GET':
        article_id = request.GET.get('article_id')

        try:
            selected_article = Article.objects.get(slug=article_id)
        except Article.DoesNotExist:
            return redirect(reverse('coffquiz:index'))

        selected_article.views = selected_article.views + 1
        selected_article.save()

        return redirect(reverse('coffquiz:show_article', kwargs={'article_title_slug':selected_article.slug}))

    return redirect(reverse('coffquiz:index'))

@login_required 
def register_profile(request):
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False) 
            user_profile.user = request.user 
            user_profile.save()

            return redirect(reverse('coffquiz:index')) 
        else:
            print(form.errors)

    context_dict = {'form': form}
    return render(request, 'coffquiz/profile_registration.html', context_dict)

class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username) 
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'signature': user_profile.signature, 'avatar': user_profile.avatar}) 
        return (user, user_profile, form) 
        
    @method_decorator(login_required) 
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username) 
        except TypeError:
            return redirect(reverse('coffquiz:index')) 
        
        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form} 
        return render(request, 'coffquiz/profile.html', context_dict) 
        
    @method_decorator(login_required) 
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username) 
        except TypeError:
            return redirect(reverse('coffquiz:index')) 
        
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save(commit=True) 
            return redirect('coffquiz:profile', user.username) 
        else:
            print(form.errors)
        
        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form}
        return render(request, 'coffquiz/profile.html', context_dict)

# this class is for add likes
class LikeCategoryView(View):
    @method_decorator(login_required())
    def get(self, request):
        coffee_id = request.GET['coffee_id']

        try:
            coffee = Coffee.objects.get(id=int(coffee_id))
        except Coffee.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        coffee.likes = coffee.likes + 1
        coffee.save()

        return HttpResponse(coffee.likes)


'''
    The following part is for coffee search function in siderbar
'''

def get_coffee_list(max_results=0, starts_with=''):
    # this function is for get the coffee list
    coffee_list = []

    if starts_with:
        coffee_list = Coffee.objects.filter(name__istartswith=starts_with)

    print(coffee_list)

    # if max_results is 0, all result will be returned
    if max_results > 0:
        if len(coffee_list) > max_results:
            coffee_list = coffee_list[:max_results]

    return coffee_list


class CoffeeSuggestionView(View):
    def get(self, request):
        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''

        coffee_list = get_coffee_list(max_results=8,
                                      starts_with=suggestion)

        if len(coffee_list) == 0:
            coffee_list = Coffee.objects.order_by('-likes')

        return render(request,
                      'coffquiz/coffeelist.html',
                      {'coffeelist': coffee_list})
