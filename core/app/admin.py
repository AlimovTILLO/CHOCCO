from django.contrib import admin
from app import forms
from app.models import Comment, Article, Category, MyUser, Like


class CommentInlineAdmin(admin.TabularInline):
    model = Comment
    extra = 1
    classes = ['collapse']
    form = forms.CommentInlineAdminForm


class ArticleAdmin(admin.ModelAdmin):
    inlines = [CommentInlineAdmin]
    form = forms.ArticleForm
    readonly_fields = ['author', 'created_at', 'edited_at']
    list_display = ['title', 'published', 'created_at', 'edited_at', 'author']
    list_filter = ['category', 'published', 'created_at', 'author']
    search_fields = ['title', 'slug', 'description', 'tags__name']
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        obj.author = request.user.my_user
        obj.save()


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name', 'slug']


class MyUserAdmin(admin.ModelAdmin):
    search_fields = ['alias']

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Like)

