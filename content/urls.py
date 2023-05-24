from django.urls import path
from . import views

app_name = "content"

urlpatterns = [
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('follow/<int:pk>/', views.follow, name='follow'),
    path('like/<int:pk>/', views.like, name='like'),
    path('deleteCom/<int:pk>/', views.delete_com, name='deleteComment'),
    path('deletePos/<int:pk>/', views.delete_pos, name='deletePost'),
    path('new/', views.create, name='new'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('followers/<int:pk>/', views.followers_view, name='followers'),
    path('followings/<int:pk>/', views.followings_view, name='followings'),
]
