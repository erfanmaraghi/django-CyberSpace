from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from content.models import time_since


# Create your models here.

class Chat(models.Model):
    members = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified_at',)

    def last_edited(self):
        return time_since(self.modified_at)

    def __str__(self):
        usernames = [member.username for member in self.members.all()]
        result = " - ".join(usernames)
        return result


class ChatMsg(models.Model):
    sender = models.ForeignKey(User, related_name="messages_sent", on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def message_sent_at(self):
        return time_since(self.created_at)

    def short_content(self):
        if len(self.content) < 40:
            return self.content
        else:
            return self.content[:40] + "..."
