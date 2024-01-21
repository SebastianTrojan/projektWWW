from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('article/<str:pk>/', views.article, name="article"),

    path('create-article/', views.createArticle, name="create-article"),
    path('edit-article/<str:pk>/', views.editArticle, name="edit-article"),
    path('delete-article/<str:pk>/', views.deleteArticle, name="delete-article"),
    
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('update-user/', views.updateUser, name="update-user"),


    # path('profile/<str:pk>/', views.userProfile, name="user-profile"),



    # path('topics/', views.topicsPage, name="topics"),
    # path('activity/', views.activityPage, name="activity"),
]
