# coding=utf-8
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from redactor.fields import RedactorField
from taggit.managers import TaggableManager


class MyUser(models.Model):
    myuser = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='my_user')
    alias = models.CharField(verbose_name='Псевдоним', max_length=25)
    karma = models.IntegerField(verbose_name='Карма', blank=True, null=True)
    image = models.ImageField(verbose_name='Изображение')

    def __str__(self):
        return self.alias

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=80)
    slug = models.SlugField(verbose_name='Ярлык')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='category_article')
    title = models.CharField(verbose_name='Заголовок', max_length=120)
    slug = models.SlugField(verbose_name='Ярлык')
    image = models.ImageField(verbose_name='Изображение', max_length=450)
    description = RedactorField(verbose_name='Статья')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    edited_at = models.DateTimeField(verbose_name='Дата редактирования', auto_now=True)
    published = models.BooleanField(verbose_name='Опубликовано', default=True)
    rating = models.IntegerField(verbose_name='Рейтинг', blank=True, null=True)
    tags = TaggableManager(verbose_name='Теги', blank=True)
    author = models.ForeignKey(MyUser, verbose_name='Автор', related_name='user_article')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article-detail', args=[self.slug, self.pk])

    def get_related(self):
        return News.objects.filter(tags__in=self.tags.all()).exclude(pk=self.pk).distinct().order_by('-created_at')

    def get_related_video(self):
        return Video.objects.filter(tags__in=self.tags.all()).distinct()

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статии'


class Comment(models.Model):
    article = models.ForeignKey(Article, verbose_name='Статья', related_name='news')
    title = models.CharField(verbose_name='Комменрарий', max_length=120)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    edited_at = models.DateTimeField(verbose_name='Дата редактирования', auto_now=True)
    published = models.BooleanField(verbose_name='Опубликовано', default=True)
    author = models.ForeignKey(MyUser, verbose_name='Автор', related_name='user_comment')



