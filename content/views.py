from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Like, Comment, Follow
from .forms import CommentSendingForm, PostCreationForm


# Create your views here.
@login_required()
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        commentForm = CommentSendingForm(request.POST)
        if commentForm.is_valid():
            commentFormVar = commentForm.save(commit=False)
            commentFormVar.user = request.user
            commentFormVar.post = post
            commentFormVar.save()
            return redirect("content:detail", pk=pk)
    i_liked_it = True if post.likes.filter(user=request.user, post=post) else False
    i_followed_it = True if request.user.followed.filter(follower=request.user, followed=post.created_by) else False
    commentForm = CommentSendingForm()
    try:
        nextPost = post.get_previous_by_created_at()
    except Post.DoesNotExist:
        nextPost = Post.objects.first()

    try:
        previousPost = post.get_next_by_created_at()
    except Post.DoesNotExist:
        previousPost = Post.objects.last()

    args = {
        'post': post,
        'i_liked_it': i_liked_it,
        'i_followed_it': i_followed_it,
        'commentForm': commentForm,
        'nextPost': nextPost,
        'previousPost': previousPost
    }

    return render(request, "content/details.html", args)


@login_required()
def like(request, pk):
    if liked := Like.objects.filter(user__in=[request.user], post__in=[Post.objects.get(pk=pk)]):
        liked.get(user__in=[request.user], post__in=[Post.objects.get(pk=pk)]).delete()
    else:
        likeModel = Like()
        likeModel.user = request.user
        likeModel.post = Post.objects.get(pk=pk)
        likeModel.save()
    nextUrl = request.POST.get('nextUrl', '/')
    return redirect(nextUrl)


@login_required()
def follow(request, pk):
    if followed := Follow.objects.filter(follower__in=[request.user], followed__in=[get_object_or_404(User, pk=pk)]):
        followed.get(follower__in=[request.user], followed__in=[get_object_or_404(User, pk=pk)]).delete()
    else:
        followModel = Follow()
        followModel.follower = request.user
        followModel.followed = get_object_or_404(User, pk=pk)
        followModel.save()
    if request.user == get_object_or_404(User, pk=pk):
        return render(request, 'content/follow_error.html', {'label': get_object_or_404(User, pk=pk).username})
    nextUrl = request.POST.get('nextUrl', '/')
    return redirect(nextUrl)


@login_required()
def delete_com(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user == request.user:
        comment.delete()
        return redirect("content:detail", pk=comment.post.id)
    else:
        return render(request, "content/delete_error.html", {'comment': comment, 'label': 'Comment', 'is_com': True})


@login_required()
def create(request):
    if request.method == "POST":
        form = PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            frm = form.save(commit=False)
            frm.created_by = request.user
            frm.save()
            return redirect("content:detail", pk=frm.id)
    form = PostCreationForm()
    return render(request, 'content/new.html', {'form': form})


@login_required()
def delete_pos(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.created_by == request.user:
        post.delete()
        return redirect("core:index")
    else:
        return render(request, "content/delete_error.html", {'post': post, 'label': 'Post'})


@login_required()
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    posts = Post.objects.filter(created_by=user)
    likes = 0
    i_followed_it = True if request.user.followed.filter(follower=request.user, followed=user) else False
    for post in posts:
        likes += post.likes.count()
    return render(request, 'content/profile.html',
                  {'user': user,
                   'posts': posts,
                   'likes': likes,
                   'i_followed_it': i_followed_it})


@login_required()
def followers_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    followers = user.follower.all()
    return render(request, "content/followers.html",
                  {'label': "Followers",
                   'followers': followers,
                   'is_follower': True})


@login_required()
def followings_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    followings = user.followed.all()
    return render(request, "content/followings.html",
                  {'label': "Followeds",
                   'followers': followings,
                   'is_follower': False})
