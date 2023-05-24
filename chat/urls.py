from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("", views.chats_view, name="chat_list"),
    path("detaill/<int:pk>/", views.chat_view, name="chat_detail"),
    path("delchat/<int:pk>/", views.del_chat, name="delete_chat")
]
