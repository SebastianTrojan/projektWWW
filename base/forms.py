from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Article, User
from ckeditor.widgets import CKEditorWidget

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'surname','username', 'email', 'password1', 'password2']


class ArticleForm(ModelForm):
    body = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Article
        fields = '__all__'
        exclude = ['author', 'is_published']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name','surname', 'username', 'email', 'bio']