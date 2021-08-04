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
    path('my_account/', views.my_account, name='my_account'),
    #path('logout/', views.user_logout, name='logout'),
    

]