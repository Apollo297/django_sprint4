from django.urls import path

from . import views


urlpatterns = [
    path('posts/<int:id>/', views.PostsDetailView.as_view(), name='post_detail'),
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
    path('posts/create/', views.PostCreateView.as_view(), name='create'),
    path('list/', views.PostListView.as_view(), name='index'),
    path('profile/<str:username>/', views.PostsDetailView, name='profile')
]

app_name = 'blog'
