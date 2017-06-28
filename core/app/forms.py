from django import forms
from app.models import Comment, Article, MyUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import FormView


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        widgets = {
        }


class CommentInlineAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
        }


class NewArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('category', 'title', 'slug', 'image', 'description', 'published', 'tags',)


class SignUpForm(UserCreationForm):
    alias = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'alias', 'password1', 'password2', )