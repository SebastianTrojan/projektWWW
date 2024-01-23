from django.urls import path
from . import views

urlpatterns = [
    path('',  views.getRoutes),
    path('articles/', views.getArticles),
    path('articles/<str:pk>/', views.getArticle),
    path('messages/', views.getMessages),
    path('messages/<str:pk>/', views.getMessage),
]
