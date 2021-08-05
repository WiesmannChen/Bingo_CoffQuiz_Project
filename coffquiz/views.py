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

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            
            if 'avatar' in request.FILES:
                profile.picture = request.FILES['avatar']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
    return render(request, 'coffquiz/register.html', context=context_dict)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('coffquiz:index'))
            else:
                return HttpResponse("Your CoffQuiz account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'coffquiz/login.html')

@login_required
def my_account(request):

    return render(request, 'coffquiz/my_account.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('coffquiz:index'))

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

@login_required
def restricted(request):
    return render(request, 'coffquiz/restricted.html')

# def search(request):
#     result_list = []

#     if request.method == 'POST':
#         query = request.POST['query'].strip()

#         if query:
#             result_list = run_query(query)

#     return render(request, 'coffquiz/search.html', {'result_list': result_list})

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