from django.db import models
from django.utils import timezone
from django import forms
# Create your models here.


class Team(models.Model):
    team_name = models.CharField(max_length=30)
    created_date = models.DateTimeField(default=timezone.now)


class JoinedTeam(models.Model):
    user_no = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    team_no = models.ForeignKey('Team', on_delete=models.CASCADE)


class Post(models.Model):
    team_no = models.ForeignKey('Team', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_date = timezone.now()
    published_date = models.DateTimeField(default=timezone.now)


class CommentProblem(models.Model):
    problem = models.IntegerField()
    team_no = models.ForeignKey('Team', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    created_date = timezone.now()


class Code(models.Model):
    code_no = models.IntegerField()
    user_no = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    success = models.BooleanField(default=False)
    display = models.BooleanField(default=True)


class CommentCode(models.Model):
    code_no = models.IntegerField()
    team_no = models.ForeignKey('Team', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    created_date = timezone.now()


class ChatChannel(models.Model):
    team_no = models.ForeignKey('Team', on_delete=models.CASCADE)
    problem_no = models.IntegerField()


class Chat(models.Model):
    chat_channel_no = models.ForeignKey('ChatChannel', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    created_date = timezone.now()

