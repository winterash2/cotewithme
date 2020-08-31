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
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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
# TODO ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
def team_home(request, team_id):
    check_user_is_joined = JoinedTeam.objects.filter(
        user_no__exact=request.user, team_no__exact=team_id)
    if len(check_user_is_joined) == 1:
        this_team = check_user_is_joined[0].team_no
        teammates = get_teammates(request, team_id)
        joined_teams = get_joined_teams(request)

        # 게시판 pagination
        posts = Post.objects.filter(
            team_no__exact=this_team, created_date__lte=timezone.now()).order_by('created_date')
        paginator = Paginator(posts, 2)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        # 내가 푼 코드 pagination
        codes_my = Code.objects.filter(
            user_no__exact=request.user).order_by('-created_date')
        codes_my_paginator = Paginator(codes_my, 2)
        codes_my_page = request.GET.get('codes_my_page')
        try:
            codes_my = codes_my_paginator.page(codes_my_page)
        except PageNotAnInteger:
            codes_my = codes_my_paginator.page(1)
        except EmptyPage:
            codes_my = codes_my_paginator.page(codes_my_paginator.num_pages)

        # 팀원이 푼 코드 pagination
        codes_teammates = Code.objects.filter(
            user_no__in=teammates).order_by('-created_date')
        codes_teammates_paginator = Paginator(codes_teammates, 2)
        codes_teammates_page = request.GET.get('codes_teammates_page')
        try:
            codes_teammates = codes_teammates_paginator.page(
                codes_teammates_page)
        except PageNotAnInteger:
            codes_teammates = codes_teammates_paginator.page(1)
        except EmptyPage:
            codes_teammates = codes_teammates_paginator.page(
                codes_teammates_paginator.num_pages)

        return render(request, 'board/team_home.html', {
            'this_team': this_team,
            'posts': posts,
            'joined_teams': joined_teams,
            'teammates': teammates,
            'codes_my': codes_my,
            'codes_teammates': codes_teammates,

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
    return redirect('problem_with_code', team_id, problem_number, '0')


def problem_with_code(request, team_id, problem_number, codes_string):
    # 지금 팀 가져오기
    this_team = get_this_team_from_team_id(team_id)
    # 참여해 있는 팀들 가져오기
    joined_teams = get_joined_teams(request)
    # 백준에서 문제 가져오기
    problem = get_problem_from_boj(problem_number)
    # 문제 댓글들 가져오기
    comments_problem = CommentProblem.objects.filter(
        team_no__exact=this_team, problem__exact=problem_number)
    # 내가 작성했던 혹은 새 코드폼 가져오기
    code_form = get_my_code_form(request, problem_number)
    if not code_form:
        code_form = CodeForm()
    # 화면에 띄울 코드들 가져오기
    codes_wanted = get_codes_wanted(codes_string)
    # 팀원들 가져오기
    teammates = get_teammates(request, team_id)
    # 팀원들 코드들 가져오기
    codes_teammate = Code.objects.filter(
        problem_no__exact=problem_number, user_no__in=teammates, display__exact=True).order_by('-created_date')
    if request.method == 'GET':
        # 내가 작성했던 혹은 새 코드폼 가져오기
        code_form = get_my_code_form(request, problem_number)
    elif request.method == 'POST' and 'comment' in request.POST:
        comment_problem_form = CommentProblemForm(request.POST)
        if comment_problem_form.is_valid():
            comment_problem = comment_problem_form.save(commit=False)
            comment_problem.problem = problem_number
            comment_problem.team_no = this_team
            comment_problem.author = request.user
            comment_problem.created_date = timezone.now()
            comment_problem.save()
    elif request.method == 'POST' and 'code' in request.POST:
        code_form = CodeForm(request.POST)
        if code_form.is_valid():
            code = code_form.save(commit=False)
            try:
                code_my = Code.objects.get(
                    problem_no=problem_number, user_no=request.user)
            except:
                code.problem_no = problem_number
                code.created_date = timezone.now()
                code.user_no = request.user
                code.save()
            else:
                code_my.one_line_comment = code.one_line_comment
                code_my.content = code.content
                code_my.success = code.success
                code_my.display = code.display
                code_my.created_date = code.created_date
                code_my.save()
        # 문제 댓글 입력할 때 쓸 댓글폼 가져오기
    comment_problem_form = CommentProblemForm()
    return render(request, 'board/problem_with_code.html', {
        'this_team': this_team,
        'joined_teams': joined_teams,
        'problem': problem,
        'comments_problem': comments_problem,
        'comment_problem_form': comment_problem_form,
        'code_form': code_form,
        'codes_teammate': codes_teammate,
        'codes_wanted': codes_wanted,
        'codes_string': codes_string,
    })


def problem_with_code_add(request, team_id, problem_number, codes_string, code_number_add):
    codes_number_list = codes_string.split('&')
    if len(codes_number_list) >= 9:
        return redirect('problem_with_code', team_id, problem_number, codes_string)
    else:
        codes_number_list.append(str(code_number_add))
        codes_number_list = set(codes_number_list)
        codes_number_list = list(codes_number_list)
        print("codes_number_list = ", codes_number_list)
        codes_string = '' + codes_number_list[0]
        codes_number_list = codes_number_list[1:]
        for code_number in codes_number_list:
            codes_string = codes_string + "&" + str(code_number)
        return redirect('problem_with_code', team_id, problem_number, codes_string)
