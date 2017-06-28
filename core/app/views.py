from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from app.forms import NewArticleForm, SignUpForm
from app.models import MyUser, Article, Comment, Category
from django.views.generic import ListView, DetailView, FormView
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils import timezone


class ArticleListView(ListView):
    template_name = 'post_list.html'
    model = Article
    paginate_by = 5
    context_object_name = 'articles_index'

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(published=True).order_by('created_at')
        return context


class ArticlesIndex(ArticleListView):
    template_name = 'index.html'
    context_object_name = 'articles_all'

    def get_context_data(self, **kwargs):
        context = super(ArticlesIndex, self).get_context_data(**kwargs)
        context['top_articles'] = Article.objects.filter(published=True).order_by('created_at').exclude(rating__lt=10)
        return context


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'article_detail.html'

    def get_object(self):
        obj = get_object_or_404(Article, slug=self.kwargs['slug'], pk=self.kwargs['pk'])
        return obj

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['article'] = Article.objects.get(pk=self.kwargs['pk'])
        context['comments'] = Comment.objects.filter(published=True).order_by('-created_at')
        return context


# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return HttpResponseRedirect('/')
#     else:
#         form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            alias = form.cleaned_data.get('alias')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user, alias)
            return HttpResponseRedirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


class CreatePost(FormView):
    form_class = NewArticleForm
    template_name = 'article_edit.html'
    success_url = '/articles/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user.my_user
        instance.save()
        return redirect(self.get_success_url())


