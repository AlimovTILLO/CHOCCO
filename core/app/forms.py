from django import forms
from app.models import Comment, Article, MyUser
from django.contrib.auth.forms import UserCreationForm


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
