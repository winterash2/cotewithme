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


def get_teammates(team_id):
    joined_team = JoinedTeam.objects.filter(team_no__exact=team_id)
    teammates = [joined.user_no for joined in joined_team]
    return teammates

