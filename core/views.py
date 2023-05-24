from django.shortcuts import render
from content.models import Post, Like, Comment


# Create your views here.
def index(request):
    posts = Post.objects.all()[:24]
    return render(request, "core/index.html", {'posts': posts})
