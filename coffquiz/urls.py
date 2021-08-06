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
    path('coffee/articles/<slug:article_title_slug>/add_comment/', views.add_comment, name='add_comment'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('goto/', views.goto_article, name='goto'),
    path('register_profile/', views.register_profile, name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('like_coffee/',views.LikeCategoryView.as_view(),name='like_coffee'),
    path('suggest/',views.CoffeeSuggestionView.as_view(),name='suggest'),
    path('coffee/', views.all_coffee, name='all_coffee'),
    path('articles/', views.all_articles, name='all_articles'),
]