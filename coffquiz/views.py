from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from coffquiz.models import Coffee, Article
from coffquiz.forms import CoffeeForm, ArticleForm, UserForm, UserProfileForm
from django.contrib.auth.models import User

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
        articles = Article.objects.filter(coffee=coffee)

        context_dict['coffee'] = coffee
        context_dict['articles'] = articles
    
    except Coffee.DoesNotExist:
        context_dict['coffee'] = None
        context_dict['articles'] = None
    
    return render(request, 'coffquiz/coffee.html', context=context_dict)

def show_article(request, article_title_slug):
    context_dict = {}
    try:
        article = Article.objects.get(slug=article_title_slug)
        context_dict['article'] = article
    
    except Coffee.DoesNotExist:
        context_dict['article'] = None
    
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