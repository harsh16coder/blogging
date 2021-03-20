from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DetailView
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from .models import Article
from  django.http import HttpResponseRedirect
from monkeylearn import MonkeyLearn
import re

def LikeView(request, pk):
    post = get_object_or_404(Article, id=request.POST.get('article_id'))
    print(post)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('article_detail', args=[str(pk)]))

class ArticleListView(LoginRequiredMixin,ListView):
    model = Article
    template_name = 'article_list.html'
    login_url = 'login'

class ArticleDetailView(LoginRequiredMixin,DetailView):
    model = Article
    template_name = 'article_detail.html'
    login_url = 'login'
    def get_context_data(self, **kwargs):
        cleanr = re.compile('<.*?>')
        ml = MonkeyLearn('3f5c2d1c62cfd67d36c38b31500b6d3f93fa9d9c')
        model_id = 'cl_pi3C7JiL'
        data = super().get_context_data(**kwargs)
        likes_connected = get_object_or_404(Article, id=self.kwargs['pk'])
        body = [re.sub(cleanr, '', likes_connected.body)]
        response = ml.classifiers.classify(model_id, body)
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        data['sentimentalAnanlysis'] = response.body[0]['classifications'][0]['tag_name']
        return data

class ArticleUpdateView(LoginRequiredMixin,UpdateView):
    model = Article
    fields = ('title','body','category',)
    template_name = 'article_edit.html'
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs): # new
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ArticleDeleteView(LoginRequiredMixin,DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs): # new
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ArticleCreateView(LoginRequiredMixin,CreateView):
    model = Article
    template_name='article_new.html'
    fields = ('title','body','category',)
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)