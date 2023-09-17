import datetime as dt

from django.views.generic import (
    CreateView, 
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from .forms import PostForm, CommentForm, UserForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from blog.models import Post, Category, Comment

User = get_user_model()
PAGE_PAGINATOR = 10


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create_post.html'
    success_url = reverse_lazy() # profile/<username>/


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = PAGE_PAGINATOR


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy() # profile/<username>/


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/create_post.html'
    success_url = reverse_lazy('blog:index')


class PostsDetailView(DetailView):
    model = Post
    form_class = CommentForm


class CommentCreateView(LoginRequiredMixin, CreateView):
    blog_post = None
    model = Comment
    form_class = CommentForm


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_form.html'


class UserDetailView(ListView):
    model = User
    template_name = 'blog/profile.html'
    paginate_by = PAGE_PAGINATOR


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    model = User
    template_name = 'blog/user.html'


class UserPasswordUpdateView(UserUpdateView):
    form_class = PasswordChangeForm
    model = User
    template_name = 'registration/password_reset_form.html'



#def profile_page(request):
#    template = 'blog/profile.html'
#    profile = Post.objects.all()
#    return render(request, template, {'profile': profile})


#def index(request):
#    template = 'blog/index.html'
#    post_list = Post.objects.select_related(
#        'category', 'location', 'author').filter(
#        pub_date__lte=dt.datetime.now(),
#        is_published=True,
#        category__is_published=True
#    ).order_by('-pub_date')[:FIVE_RECENT_PUBLICATIONS]
#    context = {'post_list': post_list}
#   return render(request, template, context)


#def post_detail(request, id):
#    template = 'blog/detail.html'
#    post = get_object_or_404(
#        Post.objects.select_related(
#            'category', 'location', 'author').filter(
#            pub_date__lte=dt.datetime.now(),
#            is_published=True,
#            category__is_published=True,
#           pk=id
#        )
#    )
#    context = {'post': post}
#    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.filter(
            is_published=True),
        slug=category_slug
    )
    post_list = Post.objects.select_related(
        'category', 'location', 'author').filter(
        category__slug=category_slug,
        is_published=True,
        pub_date__lte=dt.datetime.now()
    )
    context = {'category': category, 'post_list': post_list}
    return render(request, template, context)
