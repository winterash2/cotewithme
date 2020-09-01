from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_main_page, name='chat_main_page'),
    path('team/<int:team_id>/chat/', views.chat_home, name='chat_home'),
    path('team/<int:team_id>/chat/<str:room_name>/', views.chat_room, name='chat_room'),
    path('team/<int:team_id>/chat/<str:room_name>/delete', views.chat_room_delete, name='chat_room_delete'),
]