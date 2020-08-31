from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from ast import literal_eval
from django.http import HttpResponse
import requests
import math
from bs4 import BeautifulSoup
from .views_function import *


def main_page(request):
    if request.user.is_authenticated == True:
        return redirect('team_select')
    else:
        return redirect('login')


@login_required
def team_select(request):
    joined_teams = get_joined_teams(request)
    return render(request, 'board/team_select.html', {
        'joined_teams': joined_teams
    })


@login_required
def team_create(request):
    if request.method == 'POST':
        create_team_form = CreateTeamForm(request.POST)
        if create_team_form.is_valid():
            team = Team.objects.create(
                team_name=create_team_form.cleaned_data['team_name'], created_date=timezone.now())
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
        if len(selected_team) == 1:
            selected_team = selected_team[0]
            check_joined = JoinedTeam.objects.filter(
                team_no__exact=selected_team, user_no__exact=request.user)
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
def team_leave(request, team_id):
    joined_team = JoinedTeam.objects.filter(
        user_no__exact=request.user, team_no__exact=team_id)
    joined_team.delete()
    return redirect('main_page')


def team_delete(request, team_id):
    team = Team.objects.filter(id=team_id)
    team.delete()
    return redirect('main_page')


@login_required
def team_home(request, team_id):
    check_user_is_joined = JoinedTeam.objects.filter(
        user_no__exact=request.user, team_no__exact=team_id)
    this_team = check_user_is_joined[0].team_no
    teammates = get_teammates(team_id)

    posts = Post.objects.filter(team_no__exact=this_team)
    if len(check_user_is_joined) == 1:
        joined_teams = get_joined_teams(request)
        return render(request, 'board/team_home.html', {
            'this_team': this_team,
            'posts': posts,
            'joined_teams': joined_teams,
            'teammates': teammates,
        })
    else:
        return redirect('main_page')


def post_new(request, team_id):
    this_team = get_this_team_from_team_id(team_id)
    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            check_user_is_joined = JoinedTeam.objects.filter(
                user_no__exact=request.user, team_no__exact=team_id)
            this_team = check_user_is_joined[0].team_no
            post = post_form.save(commit=False)
            post.team_no = this_team
            post.author = request.user
            post.created_date = timezone.now()
            post.published_date = timezone.now()
            post.save()
            return redirect('team_home', this_team.id)
        else:
            return render(request, 'board/post_new.html', {
                'post_form': post_form,
                'this_team': this_team,
            })
    else:
        post_form = PostForm()
    return render(request, 'board/post_new.html', {
        'post_form': post_form,
        'this_team': this_team,
    })


def redirect_problem_home(request, team_id):
    problem_number = request.GET['problem_number']
    return redirect('problem_home', team_id, problem_number)


def problem_home(request, team_id, problem_number):
    problem = get_problem_from_boj(problem_number)
    joined_teams = get_joined_teams(request)
    this_team = get_this_team_from_team_id(team_id)

    # comment
    comment_problem_form = CommentProblemForm()
    comments_problem = CommentProblem.objects.filter(
        team_no__exact=this_team, problem__exact=problem_number)
    teammates = get_teammates(team_id)
    codes_teammate = Code.objects.filter(
        problem_no__exact=problem_number, user_no__in=teammates, display__exact=True).order_by('-created_date')

    # code
    codes = Code.objects.filter(
        problem_no__exact=problem_number, user_no__exact=request.user).order_by('-created_date')
    if not codes:
        print("plz in")
        code_form = CodeForm()
    else:
        code = codes[0]
        code_form = CodeForm(instance=code)
    if request.method == "GET":
        pass

    elif request.method == 'POST' and 'comment' in request.POST:  # submit의 name에 따라 분류
        comment_problem_form = CommentProblemForm(request.POST)
        if comment_problem_form.is_valid():
            comment_problem = comment_problem_form.save(commit=False)
            comment_problem.problem = problem_number
            comment_problem.team_no = this_team
            comment_problem.author = request.user
            comment_problem.created_date = timezone.now()
            comment_problem.save()

    elif request.method == 'POST' and 'my_code' in request.POST:
        code_form = CodeForm(request.POST)
        if code_form.is_valid():
            code = code_form.save(commit=False)
            code.problem_no = problem_number
            code.created_date = timezone.now()
            code.user_no = request.user
            code.success = False
            code.display = True
            code.save()


    return render(request, 'board/problem_home.html', {
        'this_team': this_team,
        'joined_teams': joined_teams,
        'problem': problem,
        'comment_problem_form': comment_problem_form,
        'comments_problem': comments_problem,
        'codes_teammate': codes_teammate,
        'code_form': code_form,
        'codes': codes
    })


def problem_with_code(request, team_id, problem_number, codes_string):
    # 지금 팀 가져오기
    this_team = get_this_team_from_team_id(team_id)
    # 참여해 있는 팀들 가져오기
    joined_teams = get_joined_teams(request)
    # 백준에서 문제 가져오기
    problem = get_problem_from_boj(problem_number)
    # 화면에 띄울 코드들 가져오기
    codes_wanted = get_codes_wanted(codes_string)
    # 문제 댓글들 가져오기
    comments_problem = CommentProblem.objects.filter(
        team_no__exact=this_team, problem__exact=problem_number)
    # 팀원들 가져오기
    teammates = get_teammates(team_id)
    # 팀원들 코드들 가져오기
    codes_teammate = Code.objects.filter(
        problem_no__exact=problem_number, user_no__in=teammates, display__exact=True).order_by('-created_date')

    if request.method == 'POST':
        comment_problem_form = CommentProblemForm(request.POST)
        if comment_problem_form.is_valid():
            comment_problem = comment_problem_form.save(commit=False)
            comment_problem.problem = problem_number
            comment_problem.team_no = this_team
            comment_problem.author = request.user
            comment_problem.created_date = timezone.now()
            comment_problem.save()
    else:
        # 문제 댓글 입력할 때 쓸 댓글폼 가져오기
        comment_problem_form = CommentProblemForm()
    return render(request, 'board/problem_with_code.html', {
        'this_team': this_team,
        'joined_teams': joined_teams,
        'problem': problem,
        'codes_wanted': codes_wanted,
        'comment_problem_form': comment_problem_form,
        'comments_problem': comments_problem,
        'codes_teammate': codes_teammate,
    })


def code_view(request, team_id, problem_number):
    this_team = get_this_team_from_team_id(team_id)
    joined_teams = get_joined_teams(request)
    if request.method == 'POST':
        code_form = CodeForm(request.POST)
        if code_form.is_valid():
            code = code_form.save(commit=False)
            code.code_no = problem_number
            code.user_no = request.user
            code.save()
        codes = Code.objects.filter(
            code_no__exact=problem_number, user_no__exact=request.user).order_by('-created_date')
    else:
        codes = Code.objects.filter(
            code_no__exact=problem_number, user_no__exact=request.user).order_by('-created_date')
        if not codes:
            code_form = CodeForm()
        else:
            code = codes[0]
            code_form = CodeForm(instance=code)
    return render(request, 'board/code_view.html', {
        'this_team': this_team,
        'joined_teams': joined_teams,
        'code_form': code_form,
        'codes': codes,
    })


def tab(request):
    this_team = get_this_team_from_team_id(1)
    joined_teams = get_joined_teams(request)

    return render(request, 'board/tab.html', {
        'joined_teams': joined_teams,
        'this_team': this_team,
    })
