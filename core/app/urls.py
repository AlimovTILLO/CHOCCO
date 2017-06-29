from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from app.views import ArticlesIndex, ArticleListView, ArticleDetailView, CreatePost, ProfileListView

urlpatterns = [
    url(r'^$', ArticlesIndex.as_view(), name='articles_index'),
    url(r'^page(?P<page>\d+)/$', ArticlesIndex.as_view()),

    url(r'^profile/$', ProfileListView.as_view(), name='profile'),

    url(r'^articles/$', ArticleListView.as_view(), name='articles_all'),
    url(r'^articles/page(?P<page>\d+)/$', ArticleListView.as_view()),

    url(r'^article/(?P<slug>[-_\w]+)-(?P<pk>[0-9]+)/$', ArticleDetailView.as_view()),

    url(r'^article/new/$', CreatePost.as_view(), name='new_article'),

    url(r'^like/(?P<slug>[-_\w]+)/$', views.like, name='like'),

    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
]
