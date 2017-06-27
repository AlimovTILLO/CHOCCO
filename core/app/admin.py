from django.contrib import admin
from app import forms
from app.models import Comment, Article, Category, MyUser


class CommentInlineAdmin(admin.TabularInline):
    model = Comment
    extra = 1
    classes = ['collapse']
    form = forms.CommentInlineAdminForm


class ArticleAdmin(admin.ModelAdmin):
    inlines = [CommentInlineAdmin]
    form = forms.ArticleForm


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name', 'slug']


class MyUserAdmin(admin.ModelAdmin):
    search_fields = ['alias']

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(MyUser, MyUserAdmin)

