# encoding: utf-8
import json as simplejson

from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, FormView

from app.forms import NewArticleForm, SignUpForm, CommentForm
from app.models import Article, Comment, Like


class ArticleListView(ListView):
    template_name = 'post_list.html'
    model = Article
    paginate_by = 5

    # context_object_name = 'articles_index'

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(published=True).order_by('created_at')
        return context


class ArticlesIndex(ArticleListView):
    template_name = 'index.html'

    # context_object_name = 'articles_all'

    def get_context_data(self, **kwargs):
        context = super(ArticlesIndex, self).get_context_data(**kwargs)
        context['top_articles'] = Like.objects.exclude(total_likes__lt=5)
        # context['top_articles'] = Article.objects.filter(published=True).order_by('created_at')
        return context


class ProfileListView(ArticleListView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileListView, self).get_context_data(**kwargs)
        context['my_articles'] = Article.objects.filter(author=self.request.user.my_user).order_by('created_at')
        return context


class ArticleDetailView(DetailView):
    model = Article
    # context_object_name = 'article'
    template_name = 'article_detail.html'

    def get_object(self):
        obj = get_object_or_404(Article, slug=self.kwargs['slug'], pk=self.kwargs['pk'])
        return obj

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['article'] = Article.objects.get(pk=self.kwargs['pk'])
        context['likes'] = Like.objects.filter(article=self.object.id)
        context['comments'] = Comment.objects.filter(article=self.object.id).select_related().order_by('-created_at')
        context['slug'] = self.kwargs['slug']
        return context

    def post(self, request, *args, **kwargs):
        self.object = article = self.get_object()
        if request.user.is_authenticated():
            form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            if request.user.is_authenticated():
                comment.author = self.request.user.my_user
            comment.save()
            return redirect('/article/%s' % article.get_absolute_url())

        context = self.get_context_data(object=article)
        context['comment_form'] = form
        return self.render_to_response(context)


class CreatePost(FormView):
    form_class = NewArticleForm
    template_name = 'article_edit.html'
    success_url = '/articles/'
    context_object_name = 'new_article'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user.my_user
        instance.save()
        return redirect(self.get_success_url())


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.my_user.alias = form.cleaned_data.get('alias')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def like(request, *args, **kwargs):
    vars = {}
    if request.method == 'POST':
        user = request.user.my_user
        slug = request.POST.get('slug', None)
        article = get_object_or_404(Article, slug=slug)

        liked, created = Like.objects.create(Article=article)

        try:
            user_liked = Like.objects.get(Article=article, user=user)
        except:
            user_liked = None

        if user_liked:
            user_liked.total_likes -= 1
            liked.user.remove(request.user)
            user_liked.save()
        else:
            liked.user.add(request.user)
            liked.total_likes += 1
            liked.save()

    return HttpResponse(simplejson.dumps(vars), content_type='application/javascript')
