from django.urls import path
from coffquiz import views

app_name = 'coffquiz'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('coffee/<slug:coffee_name_slug>/', views.show_coffee, name='show_coffee'),
    path('coffee/articles/<slug:article_title_slug>/', views.show_article, name='show_article'),
    path('add_coffee/', views.add_coffee, name='add_coffee'),
    path('coffee/<slug:coffee_name_slug>/add_article/', views.add_article, name='add_article'),

    path('restricted/', views.restricted, name='restricted'),
    #path('login/', views.user_login, name='login'),
    #path('my_account/', views.my_account, name='my_account'),
    #path('logout/', views.user_logout, name='logout'),
    #path('search/', views.search, name='search'),
    path('goto/', views.goto_article, name='goto'),
    path('register_profile/', views.register_profile, name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('like_coffee/',views.LikeCategoryView.as_view(),name='like_coffee'),
    path('suggest/',views.CoffeeSuggestionView.as_view(),name='suggest'),
]