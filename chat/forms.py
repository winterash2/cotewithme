from django import forms
from chat.models import ChatChannel


class ChatChannelForm(forms.Form):
  chat_channel_name = forms.CharField(
      label=False, 
      max_length=20,
      widget=forms.Textarea(
        attrs={
          'rows': 1,
          'cols': 20,
          'placeholder':'생성할 채팅방 이름',
        })
    )
