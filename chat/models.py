from django.db import models
from django.utils import timezone

# Create your models here.


class ChatChannel(models.Model):
    team_no = models.ForeignKey('board.Team', on_delete=models.CASCADE)
    problem_no = models.IntegerField()


class Chat(models.Model):
    chat_channel_no = models.ForeignKey(
        'ChatChannel', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
