from django.conf.urls import url
from . import views
from app.views import ArticlesIndex, ArticleListView, ArticleDetailView, CreatePost

urlpatterns = [
    url(r'^$', ArticlesIndex.as_view()),
    url(r'^page(?P<page>\d+)/$', ArticlesIndex.as_view()),

    url(r'^articles/$', ArticleListView.as_view()),
    url(r'^articles/page(?P<page>\d+)/$', ArticleListView.as_view()),

    url(r'^article/(?P<slug>[-_\w]+)-(?P<pk>[0-9]+)/$', ArticleDetailView.as_view()),

    url(r'^signup/$', views.signup, name='signup'),

    url(r'^article/new/$', CreatePost.as_view()),
]