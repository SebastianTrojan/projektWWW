from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Article, User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        exclude = ['author']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name', 'username', 'email', 'bio']