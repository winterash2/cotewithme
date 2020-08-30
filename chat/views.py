from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from .models import *
from board.models import Team

# Create your views here.


def get_chat_channel_list_form_team_id(team_id):
    return ChatChannel.objects.filter(team_no_id__exact=team_id)


def chat_home(request, team_id):
    chat_channel_list = get_chat_channel_list_form_team_id(team_id)
    return redirect('chat_room', team_id, 'home')
    # return render(request, 'chat/index.html', {})


def get_this_team_from_team_id(team_id):
    this_team = Team.objects.get(id=team_id)
    return this_team


def chat_room(request, team_id, room_name):
    this_team = get_this_team_from_team_id(team_id)
    room_name = this_team.team_name + room_name
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'this_team': this_team,
    })
