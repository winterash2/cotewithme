from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from .models import *
from board.models import Team
from chat.forms import ChatChannelForm

# Create your views here.


def get_this_team_from_team_id(team_id):
    this_team = Team.objects.get(id=team_id)
    return this_team


def get_chat_channel_list_form_team_id(team_id):
    return ChatChannel.objects.filter(team_no_id__exact=team_id)


def chat_home(request, team_id):
    chat_channel_list = get_chat_channel_list_form_team_id(team_id)
    return redirect('chat_room', team_id, 'home')
    # return render(request, 'chat/index.html', {})


def chat_room(request, team_id, room_name):
    this_team = get_this_team_from_team_id(team_id)
    room_name = this_team.team_name + room_name
    if request.method == "POST":
        chat_channel_form = ChatChannelForm(request.POST)
        if chat_channel_form.is_valid():
            chat_channel_name = chat_channel_form.cleaned_data['chat_channel_name']
            check = ChatChannel.objects.filter(
                team_no__exact=this_team, chat_channel_name__exact=chat_channel_name)
            if check:
                pass
            else:
                chat_channel = ChatChannel()
                chat_channel.chat_channel_name = chat_channel_name
                chat_channel.team_no = this_team
                chat_channel.save()
    chat_channel_form = ChatChannelForm()
    chat_channel_list = ChatChannel.objects.filter(team_no=this_team)
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'this_team': this_team,
        'chat_channel_form': chat_channel_form,
        'chat_channel_list': chat_channel_list,
    })
