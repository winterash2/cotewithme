from django import forms
from chat.models import ChatChannel


class ChatChannelForm(forms.Form):
  chat_channel_name = forms.CharField(label="새로운 채팅방 생성", max_length=50)