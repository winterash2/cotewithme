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


def get_joined_teams(request):
    joined_team_list = JoinedTeam.objects.filter(user_no__exact=request.user)
    joined_teams = [t.team_no for t in joined_team_list]
    return joined_teams


def get_problem_from_boj(problem_number):
    url = 'http://boj.kr/' + str(problem_number)
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    problem = {}
    similar_problem = []
    info_key = []
    info_value = []
    problem['문제번호'] = problem_number
    for tag in soup.select('.col-md-12'):
        for title in tag.select('#problem_title'):
            problem['문제제목'] = title.text
        for prob in tag.select('#problem_description p'):
            problem['문제'] = prob.text
        for in_put in tag.select('#input p'):
            problem['입력'] = in_put.text
        for output in tag.select('#output p'):
            problem['출력'] = output.text
        for key in soup.select('.col-md-12 .table th'):
            info_key.append(key.text.replace(' ', ''))
        for value in soup.select('.col-md-12 .table td'):
            info_value.append(value.text.replace(' ', ''))
        for similar_prob in tag.select('#problem_association li'):
            similar_problem.append(similar_prob.text)
    for key, value in zip(info_key, info_value):
        problem[key] = value
    input_list = []
    output_list = []
    for idx, ex in enumerate(soup.select('.sampledata')):
        cnt = math.floor(idx / 2) + 1
        if idx % 2 == 0:
            input_list.append(ex.text)
        else:
            output_list.append(ex.text)
    problem['입력예시'] = input_list
    problem['출력예시'] = output_list
    if len(similar_problem) != 0:
        problem['비슷한문제'] = similar_problem
    return problem


def get_teammates(request, team_id):
    joined_team = JoinedTeam.objects.filter(team_no__exact=team_id)
    teammates = [joined.user_no for joined in joined_team if not joined.user_no == request.user]
    return teammates


def get_this_team_from_team_id(team_id):
    this_team = Team.objects.get(id=team_id)
    return this_team


def get_codes_wanted(codes_string):
    codes_number_list = codes_string.split('&')
    for code_number in codes_number_list:
        if code_number == '0':
            codes_number_list.remove('0')
    if codes_number_list:
        codes_wanted = Code.objects.filter(id__in=codes_number_list)
        return codes_wanted
    else:
        return None


def get_my_code_form(request, problem_number):
    codes = Code.objects.filter(
        problem_no__exact=problem_number, user_no__exact=request.user).order_by('-created_date')
    if not codes:
        code_form = CodeForm()
    else:
        code = codes[0]
        code_form = CodeForm(instance=code)
    return code_form


def get_code_my(request, problem_number):
    code_my = Code.objects.get(problem_no=problem_number, user_no=request.user)
    if code_my:
        return code_my
    else:
        return None