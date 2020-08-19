from django import forms
from .models import Team, JoinedTeam
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

# class JoinedTeam(models.Model):
#     user_no = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     team_no = models.ForeignKey('Team', on_delete=models.CASCADE)
