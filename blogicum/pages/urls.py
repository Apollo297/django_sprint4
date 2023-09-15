from django.urls import path

from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('rules/', views.rules, name='rules'),
]

app_name = 'pages'
