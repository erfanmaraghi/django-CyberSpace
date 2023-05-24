from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


def time_since(timestamp):
    now = timezone.now()
    if now > timestamp:
        diff = now - timestamp
        if diff.days == 0:
            if diff.seconds < 60:
                return 'just now'
            elif diff.seconds < 120:
                return '1 minute ago'
            elif diff.seconds < 3600:
                return f'{diff.seconds // 60} minutes ago'
            elif diff.seconds < 7200:
                return '1 hour ago'
            else:
                return f'{diff.seconds // 3600} hours ago'
        elif diff.days == 1:
            return 'yesterday'
        else:
            return f'{diff.days} days ago'
    else:
        return 'in the future'


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=60)
    caption = models.TextField(null=True)
    content = models.ImageField()
    created_by = models.ForeignKey(User, related_name="contents", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def added_time(self):
        return time_since(self.created_at)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="followed", on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def added_time(self):
        return time_since(self.created_at)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.content[:10] + "..."
