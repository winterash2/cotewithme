from django.urls import path
from . import views

urlpatterns = [
    path('team/<int:team_id>/chat/', views.chat_home, name='chat_home'),
    path('team/<int:team_id>/chat/<str:room_name>/', views.chat_room, name='chat_room'),
]