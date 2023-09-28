import datetime as dt
from typing import Any
from django.db.models.query import QuerySet

from django.views.generic import (
    CreateView, 
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
#from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
#from .forms import PostForm, CommentForm, UserForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

from blog.models import Post, Category, Comment
from .forms import PostForm, CommentForm, UserForm


User = get_user_model()
PAGE_PAGINATOR = 10


class IndexHome(ListView):
    model = Post
    ordering = 'id'
    paginate_by = PAGE_PAGINATOR
    template_name = 'blog/index.html'

    def get_queryset(self):
        return (
            Post.objects.select_related(
                'category', 'location', 'author').filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=dt.datetime.now())
        ).order_by('-pub_date')
    

class ProfileView(ListView):
    model = User
    template_name = 'blog/profile.html'
    paginate_by = PAGE_PAGINATOR

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['profile'] = self.request.user
        return context

    def get_queryset(self):
        self.author = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        # Если гость - показываем только посты
        # с флагом "is_published"
        if self.author != self.request.user:
            return Post.objects.select_related(
                    'category', 'location', 'author').filter(
                    is_published=True,
                    author=self.author,
                    ).order_by('-pub_date')
        # Если автор - показываем все посты
        return Post.objects.select_related(
                    'category', 'location', 'author').filter(
                    author=self.author
        ).order_by('-pub_date')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    from_class = UserForm
    template_name = 'blog/user.html'

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект  или вызываем 404 ошибку.
        get_object_or_404(User, username=kwargs['username'])
        # Если объект был найден, то вызываем родительский метод, 
        # чтобы работа CBV продолжилась.
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.get_username()}
        )


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    # При создании поста мы не можем указывать автора вручную, 
    # для этого переопределим метод валидации:
    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.get_username()}
        )


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        # При получении объекта не указываем автора.
        # Результат сохраняем в переменную.
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        # Сверяем автора объекта и пользователя из запроса.
        if instance.author != request.user:
            # Здесь может быть как вызов ошибки, так и редирект на нужную страницу.
            return redirect('blog:detail')
        return super().dispatch(request, *args, **kwargs) 
    
    def get_success_url(self) -> str:
        pass


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:profile')

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Post, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['form'] = CommentForm
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    # Переопределяем dispatch()
    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    # Переопределяем form_valid()
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    success_url = reverse_lazy('blog:detail')


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('blog:detail')


class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category.html'
    paginate_by = PAGE_PAGINATOR

    def get_queryset(self):
        return Post.objects.filter(
            category__slug=self.kwargs['category_slug'],
            is_published=True, 
            pub_date__lte=dt.datetime.now()
        ).order_by('pub_date')

#     def get_context_data(self, **kwargs):
#         # Получаем словарь контекста:
#         context = super().get_context_data(**kwargs)
#         # Добавляем в словарь новый ключ:
#         context['form'] = CommentForm
#         return context



# class PasswordUpdateView(UpdateView):
#     form_class = PasswordForm
#     model = User
#     template_name = 'registration/password_reset_form.html'

