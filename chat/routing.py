from . import consumers
from django.urls import path


websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer),
]