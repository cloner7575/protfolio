from django.urls import path
from . import views


urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('category/<slug:slug>/', views.blog_category, name='blog_category'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
]
