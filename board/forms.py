from django import forms
from .models import *
from django.utils import timezone


# class Team(models.Model):
#     team_name = models.CharField(max_length=30)
#     created_date = models.DateTimeField(default=timezone.now)
def check_same_team(name):
    date = timezone.now()
    # teams = Team.objects.filter( team_name__exact=name, created_date__exact=date)
    teams = Team.objects.filter(team_name__exact=name)
    if len(teams) != 0:
        raise forms.ValidationError("중복되는 팀이 있습니다.")


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('team_name', 'created_date')


class CreateTeamForm(forms.Form):
    team_name = forms.CharField(validators=[check_same_team])


class PostForm(forms.ModelForm):
    title = forms.CharField(
        label=False,
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'id':'post-title',
                'placeholder': '제목을 입력해 주세요.',
            }
        )
    )
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(
            attrs={
                'id':'post-content',
                'placeholder':'내용을 입력하세요.'
            }
        )
    )
    class Meta:
        model = Post
        fields = ('title', 'content', )


class CommentPostForm(forms.ModelForm):
    class Meta:
        model = CommentPost
        fields = ('content', )


class CommentProblemForm(forms.ModelForm):
    class Meta:
        model = CommentProblem
        fields = ('content', )


class CodeForm(forms.ModelForm):
    one_line_comment = forms.CharField(
        label=False,
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'id': 'code-one-line-comment',
                'placeholder': '한 줄 코멘트를 입력해주세요.',
            }
        )
    )
    content = forms.CharField(
        label=False,
        widget=forms.Textarea(
            attrs={
                'id': 'code-content',
                'placeholder': '내용을 입력하세요.'
            }
        )
    )
    class Meta:
        model = Code
        fields = ("one_line_comment", "content", "success", "display", )

        # widgets = {
        #
        # }
        # def __init__(self, *args, **kwargs):
        #     super(CodeForm, self).__init__( *args, **kwargs)
        #     self.field['codeform_field'].widgets.attrs.update({
        #         one_line_comment = models.CharField(max_length=50)
        #         content = models.TextField()
        #         success = models.BooleanField(default=False)
        #         display = models.BooleanField(default=True)
        #     })