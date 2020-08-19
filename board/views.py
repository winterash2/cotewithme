from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.utils import timezone
# Create your views here.


def main_page(request):
    if( request.user.is_authenticated == True):
        return redirect('team_select')
    else:
        return redirect('login')


def team_select(request):
    return render(request, 'board/team_select.html', {})


def team_create(request):
    if request.method == 'POST':
        create_team_form = CreateTeamForm(request.POST)
        if create_team_form.is_valid():
            team = Team.objects.create(team_name=create_team_form.cleaned_data['team_name'], created_date=timezone.now())
            print("Create Team Name=", team.team_name, " Created_Date= ", team.created_date)

            join = JoinedTeam()
            join.team_no = team
            join.user_no = request.user
            join.save()
            return redirect('team_select')
    else:
        create_team_form = CreateTeamForm()
    return render(request, 'board/team_create.html', {'create_team_form': create_team_form})


def team_join(request):
    if request.method == 'POST':
        team_form = TeamForm(request.POST)
        team = team_form.save(commit=False)
        selected_team = Team.objects.filter(team_name__exact=team.team_name)
        print("type=", type(selected_team), "len=", len(selected_team))
        if len(selected_team) == 1:
            selected_team = selected_team[0]
            check_joined = JoinedTeam.objects.filter(team_no__exact=selected_team, user_no__exact=request.user)
            if len(check_joined) == 0:
                join = JoinedTeam()
                join.team_no = selected_team
                join.user_no = request.user
                join.save()
        return redirect('team_select')
    else:
        team_form = TeamForm()
    return render(request, 'board/team_join.html', {'team_form': team_form})


