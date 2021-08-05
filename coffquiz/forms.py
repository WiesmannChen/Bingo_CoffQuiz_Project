from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from coffquiz.models import Coffee, Article, UserProfile, Comment

class CoffeeForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the coffee name.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    time = forms.DateTimeField(widget=forms.HiddenInput(), initial=timezone.now)
    picture = forms.ImageField(help_text="Please upload a coffee picture.", required=False)
    description = forms.CharField(help_text="Please enter the coffee introduction.")

    class Meta:
        model = Coffee
        exclude = ('user',)

class ArticleForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the review title.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    time = forms.DateTimeField(widget=forms.HiddenInput(), initial=timezone.now)
    picture = forms.ImageField(help_text="Please upload a coffee picture.", required=False)
    content = forms.CharField(help_text="Please enter the content.") 

    class Meta:
        model = Article
        exclude = ('writer', 'coffee')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'signature')

class CommentForm(forms.ModelForm):
    comments = forms.CharField(max_length=128, help_text="Please ennter the coomment content.")
    time = forms.DateTimeField(widget=forms.HiddenInput(), initial=timezone.now)
    class Meta:
        model = Comment
        exclude = ('article',)