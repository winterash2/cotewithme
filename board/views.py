from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from ast import literal_eval
# Create your views here.


def main_page(request):
    if request.user.is_authenticated == True:
        return redirect('team_select')
    else:
        return redirect('login')


@login_required
def team_select(request):
    joined_team_list = JoinedTeam.objects.filter(user_no__exact=request.user)
    print('joined_teams len=', len(joined_team_list))
    joined_teams = [t.team_no for t in joined_team_list]
    return render(request, 'board/team_select.html', {'joined_teams': joined_teams})


@login_required
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


@login_required
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

@login_required
def team_leave(request, team_name_delete):
    joined_team = JoinedTeam.objects.filter(user_no__exact=request.user, team_no__team_name=team_name_delete)
    joined_team.delete()
    return redirect('main_page')


@login_required
def team_home(request, team_name):
    check_user_is_joined = JoinedTeam.objects.filter(user_no__exact=request.user,
                                                     team_no__team_name__exact=team_name)
    this_team = check_user_is_joined[0].team_no
    posts = Post.objects.filter(team_no__exact=this_team)
    if len(check_user_is_joined) == 1:
        return render(request, 'board/team_home.html', {'this_team': this_team, 'posts': posts})
    else:
        return redirect('main_page')


def post_new(request, team_name):
    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            check_user_is_joined = JoinedTeam.objects.filter(user_no__exact=request.user,
                                                             team_no__team_name__exact=team_name)
            this_team = check_user_is_joined[0].team_no
            post = post_form.save(commit=False)
            print("title=", post.title, " content=", post.content)
            post.team_no = this_team
            post.author = request.user
            post.created_date = timezone.now()
            post.published_date = timezone.now()
            post.save()
            return redirect('team_home', this_team.team_name)
        else:
            return render(request, 'board/post_new.html', {'post_form': post_form})
    else:
        post_form = PostForm()
    return render(request, 'board/post_new.html', {'post_form': post_form})
