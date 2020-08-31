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


def min_length_5_validator(value):
    if len(value) < 3:
        raise forms.ValidationError("5글자 이상 입력해주세요.")


class Post(models.Model):
    team_no = models.ForeignKey('Team', on_delete=models.CASCADE)
    title = models.CharField(max_length=150, validators=[
                             min_length_5_validator])
    content = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(default=timezone.now)


class CommentProblem(models.Model):
    problem = models.IntegerField()
    team_no = models.ForeignKey('Team', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField(max_length=300, default="")
    created_date = models.DateTimeField(default=timezone.now)
    # one_line_comment = models.TextField(max_length=50)

    def __str__(self):
        return self.content

class Code(models.Model):
    problem_no = models.IntegerField()
    user_no = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    one_line_comment = models.TextField(max_length=50)
    content = models.TextField()
    success = models.BooleanField(default=False)
    display = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
