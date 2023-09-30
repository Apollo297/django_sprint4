import datetime as dt

from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from blog.models import Post, Category, Comment
from .forms import PostForm, CommentForm, UserForm


User = get_user_model()
PAGE_PAGINATOR = 10


class IndexHome(ListView):
    model = Post
    ordering = '-pub_date'
    paginate_by = PAGE_PAGINATOR
    template_name = 'blog/index.html'

    def get_queryset(self):
        return (
            Post.objects.select_related(
                'category', 'location', 'author'
                ).filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=dt.datetime.now()
                ).annotate(
                    comment_count=Count('comments'))
        ).order_by('-pub_date')


class ProfileView(ListView):
    model = User
    template_name = 'blog/profile.html'
    paginate_by = PAGE_PAGINATOR
    ordering = 'id'

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['profile'] = get_object_or_404(
            User,
            username=self.kwargs['username'])
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
                    'category', 'location', 'author'
                    ).filter(
                    is_published=True,
                    author=self.author
                    ).annotate(
                        comment_count=Count('comments')
                        ).order_by('-pub_date')
        # Если автор - показываем все посты
        return Post.objects.select_related(
                    'category', 'location', 'author'
                    ).filter(
                    author=self.author
                    ).annotate(
                        comment_count=Count('comments')
                               ).order_by('-pub_date')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    from_class = UserForm
    template_name = 'blog/user.html'
    fields = ('username', 'first_name', 'last_name', 'email',)

    def get_object(self, queryset=None):
        get_object_or_404(User, username=self.request.user.get_username())
        return self.request.user

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
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        # При получении объекта не указываем автора.
        # Результат сохраняем в переменную.
        instance = get_object_or_404(Post, pk=kwargs['post_id'])
        # Сверяем автора объекта и пользователя из запроса.
        if instance.author != request.user:
            return redirect('blog:post_detail', self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy('blog:post_detail', args=[self.kwargs['post_id']])


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        autor = get_object_or_404(Post, id=kwargs['post_id']).author
        if autor != request.user:
            return redirect('blog:post_detail', self.kwargs['post_id'])
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['form'] = PostForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse_lazy('blog:profile', args=[self.request.user])


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Post.objects.select_related('location', 'author', 'category')
            .filter(pub_date__lte=dt.datetime.now(),
                    category__is_published=True), pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        if post.author != self.request.user and not post.is_published:
            return redirect('blog:post_detail', self.kwargs['pk'])
        # Добавляем в словарь новый ключ:
        context['form'] = CommentForm
        context['comments'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.comments.select_related('author')
        )
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'post_id'
    blog_post = None

    # Переопределяем dispatch()
    def dispatch(self, request, *args, **kwargs):
        self.blog_post = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    # Переопределяем form_valid()
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.blog_post
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('blog:post_detail',
                       kwargs={'pk': self.kwargs.get('post_id')})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'blog/comment.html'
    fields = ('text',)
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        print(kwargs)
        instance = get_object_or_404(Comment, pk=kwargs['comment_id'])
        # Сверяем автора объекта и пользователя из запроса.
        if instance.author != request.user:
            return redirect('blog:post_detail')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy('blog:post_detail', args=[self.kwargs['post_id']])


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        master = get_object_or_404(Comment, id=kwargs['comment_id']).author
        if master != request.user:
            return redirect('blog:post_detail', self.kwargs['comment_id'])
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['form'] = CommentForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', args=[self.kwargs['post_id']])


class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category.html'
    paginate_by = PAGE_PAGINATOR

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(
            Category,
            slug=kwargs['category_slug'],
            is_published=True,
        )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.select_related(
            'author', 'location', 'category').filter(
            category__slug=self.kwargs['category_slug'],
            is_published=True,
            pub_date__lte=dt.datetime.now()).annotate(
            comment_count=Count('comments')).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['category'] = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'])
        return context
