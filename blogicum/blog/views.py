import datetime as dt

from django.shortcuts import get_object_or_404, render

from blog.models import Post, Category

FIVE_RECENT_PUBLICATIONS = 5


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.select_related(
        'category', 'location', 'author').filter(
        pub_date__lte=dt.datetime.now(),
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:FIVE_RECENT_PUBLICATIONS]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related(
            'category', 'location', 'author').filter(
            pub_date__lte=dt.datetime.now(),
            is_published=True,
            category__is_published=True,
            pk=id
        )
    )
    context = {'post': post}
    return render(request, template, context)


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
