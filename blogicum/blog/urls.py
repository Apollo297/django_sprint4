from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
    path('', views.PostCreateView.as_view(), name='create'),
    path('profile/<int:id>/', views.profile_page, name='profile')
]

app_name = 'blog'
